from PIL import Image, ImageDraw
from PIL.ImageTk import PhotoImage

SUPERSAMPLING = 4  # images are drawn bigger then reduced to get smooth corners
TAB_SIZE = (24, 24)
DISABLED_TEXT_COLOR = '#adb5bd'

# tk images must be kept referenced or they are garbage collected
_images = []


def _tabImage(fill, border, radius):
    width, height = TAB_SIZE
    scale = SUPERSAMPLING
    image = Image.new('RGBA', (width * scale, height * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    # shapes go below the image bottom: only the top corners are rounded and the bottom is left open
    bottom = (height + radius) * scale
    draw.rounded_rectangle((0, 0, width * scale - 1, bottom), radius * scale, fill=border)
    draw.rounded_rectangle((scale, scale, width * scale - 1 - scale, bottom), (radius - 1) * scale, fill=fill)
    photo = PhotoImage(image.resize(TAB_SIZE, Image.LANCZOS))
    _images.append(photo)
    return photo


def roundTabs(style, radius=8, padding=(10, 5)):
    """Gives rounded top corners to the tabs of ttk notebooks and some room on each side of their title"""
    border = style.colors.border
    selected = style.lookup('TFrame', 'background')
    normal = style.colors.light
    hover = style.colors.inputbg if style.colors.inputbg != selected else '#f8f9fa'
    disabled = '#f8f9fa'

    margin = radius + 1
    style.element_create('RoundedTab.tab', 'image', _tabImage(normal, border, radius),
                         ('disabled', _tabImage(disabled, border, radius)),
                         ('selected', _tabImage(selected, border, radius)),
                         ('active', _tabImage(hover, border, radius)),
                         border=(margin, margin, margin, 2), padding=padding + padding, sticky='nswe')
    style.layout('TNotebook.Tab', [('RoundedTab.tab', {'sticky': 'nswe', 'children': [
        ('Notebook.label', {'sticky': 'nswe'})]})])
    style.map('TNotebook.Tab', foreground=[('disabled', DISABLED_TEXT_COLOR)])
