import math
from PIL import Image, ImageDraw
from PIL.ImageTk import PhotoImage

SUPERSAMPLING = 4  # images are drawn bigger then reduced to get smooth corners
TAB_SIZE = (24, 24)

# tk images must be kept referenced or they are garbage collected
_images = []
# element names are per theme and cannot be created twice, a new one is needed each time the theme is changed
_elementCount = 0


def mix(color, other, ratio):
    """Color between two '#rrggbb' colors, ratio 0 gives color and 1 gives other"""
    channels = [round(int(color[i:i + 2], 16) * (1 - ratio) + int(other[i:i + 2], 16) * ratio) for i in (1, 3, 5)]
    return '#%02x%02x%02x' % tuple(channels)


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


def roundTabs(style, radius=8, padding=(10, 5), noSelection=False):
    """Gives rounded top corners to the tabs of ttk notebooks and some room on each side of their title,
    with noSelection the selected tab looks like the others"""
    global _elementCount
    border = style.colors.border
    selected = style.lookup('TFrame', 'background')
    normal = mix(selected, border, 0.4)
    hover = mix(selected, border, 0.15)
    disabled = selected

    margin = radius + 1
    _elementCount += 1
    element = 'RoundedTab%d.tab' % _elementCount
    style.element_create(element, 'image', _tabImage(normal, border, radius),
                         ('disabled', _tabImage(disabled, border, radius)),
                         ('selected', _tabImage(normal if noSelection else selected, border, radius)),
                         ('active', _tabImage(hover, border, radius)),
                         border=(margin, margin, margin, 2), padding=padding + padding, sticky='nswe')
    style.layout('TNotebook.Tab', [(element, {'sticky': 'nswe', 'children': [
        ('Notebook.label', {'sticky': 'nswe'})]})])


def tabTextColors(style, noSelection=False):
    """Text colors of the tabs, to be set last because the theme puts its own back when other styles are changed"""
    disabledText = mix(style.colors.fg, style.lookup('TFrame', 'background'), 0.6)
    # the tabs that are not selected have a greyed text in the dark themes
    isDark = sum(int(style.colors.bg[i:i + 2], 16) for i in (1, 3, 5)) < 384
    unselected = mix(style.colors.fg, style.colors.bg, 0.4) if isDark else style.colors.fg
    selected = unselected if noSelection else style.colors.fg
    foreground = [('disabled', disabledText), ('selected', selected), ('!selected', unselected)]
    style.master.tk.call('ttk::style', 'map', 'TNotebook.Tab', '-foreground', [item for pair in foreground for item in pair])


def gearButtonColors(style):
    """Background of the gear button while the settings are open, the theme draws it like any other flat button"""
    selected = mix(style.colors.bg, style.colors.border, 0.5)
    style.master.tk.call('ttk::style', 'map', 'Toolbutton', '-background', ['selected', selected])
    # the themes don't give the same padding around the icon, which would not be centered the same way
    style.master.tk.call('ttk::style', 'configure', 'Toolbutton', '-padding', [6, 0])


def gearIcon(color, size=14, teeth=8):
    """Gear in the style of the Material Design settings icon, drawn in the given '#rrggbb' color"""
    scale = 8 * SUPERSAMPLING
    side = size * scale
    center = side / 2
    image = Image.new('RGBA', (side, side), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    body, tip, hole = 0.70 * center, 0.98 * center, 0.30 * center
    draw.ellipse((center - body, center - body, center + body, center + body), fill=color)
    for index in range(teeth):
        angle = 2 * math.pi * index / teeth
        points = []
        # each tooth is a trapezoid, wider at its root inside the body than at its tip
        for radius, halfWidth in ((body * 0.8, 0.20), (tip, 0.12), (tip, -0.12), (body * 0.8, -0.20)):
            offset = angle + halfWidth
            points.append((center + radius * math.cos(offset), center + radius * math.sin(offset)))
        draw.polygon(points, fill=color)
    draw.ellipse((center - hole, center - hole, center + hole, center + hole), fill=(0, 0, 0, 0))
    return PhotoImage(image.resize((size, size), Image.LANCZOS))
