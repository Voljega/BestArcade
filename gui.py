import tkinter as Tk
import tkinter.font as Font
from tkinter import ttk
import ttkbootstrap
import tabstyle
import conf
import wckToolTips
import os
import utils
from retroarchgui import RetroarchGUI
from arcadegui import ArcadeGUI
from settingsgui import SettingsGUI
import platform
import subprocess


class GUI:
    MACOS_DEFAULT_FONT_SIZE = 7
    DEFAULT_FONT_SIZE = 9
    THEMES = {'Light': 'flatly', 'Dark': 'darkly'}
    SETTINGS_FILE = 'conf-settings.conf'
    TABS = [('retroarch', 'Retroarch'), ('arcade', 'Arcade'), ('neogeoaes', 'Neo Geo AES'),
            ('model2', 'Sega Model 2'), ('model3', 'Sega Model 3'), ('atomiswave', 'Atomiswave'),
            ('naomi', 'Naomi'), ('naomi2', 'Naomi 2'), ('namco2x6', 'Namco 2x6'), ('handheld', 'Handhelds'),
            ('tvgames', 'TV Games')]

    def __init__(self, scriptDir, logger, title):
        self.scriptDir = scriptDir

        self.window = Tk.Tk()
        self.settingsButton = None
        self.settingsOpen = None
        self.notebook = None
        self.logTest = None
        self.theme = self.__loadTheme()
        self.style = ttkbootstrap.Style(theme=self.theme)
        # section titles in bold
        self.sectionFont = Font.Font(font=Font.nametofont('TkDefaultFont'))
        self.sectionFont.configure(weight='bold')
        self.__customizeStyle()
        # a closed readonly combobox keeps the chosen text highlighted otherwise
        self.window.bind_class('TCombobox', '<<ComboboxSelected>>', lambda event: event.widget.selection_clear(), add='+')
        self.window.resizable(False, False)
        self.window.geometry('+50+25')
        self.startFontSize = self.DEFAULT_FONT_SIZE

        if platform.system() == 'Windows':
            self.window.iconbitmap('bestarcade.ico')
        elif platform.system() == 'Darwin':
            # Handle tkinter font size bug on MacOS
            self.startFontSize = self.MACOS_DEFAULT_FONT_SIZE

        self.__setFontSize(self.startFontSize)
        self.window.title(title)
        self.logger = logger
        self.root = None

    def __settingsPath(self):
        return os.path.join(self.scriptDir, utils.confDir, self.SETTINGS_FILE)

    @staticmethod
    def __osTheme():
        """The theme matching the dark or light mode of the OS, light when it can't be told"""
        dark = False
        try:
            if platform.system() == 'Windows':
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                     r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize')
                dark = winreg.QueryValueEx(key, 'AppsUseLightTheme')[0] == 0
            elif platform.system() == 'Darwin':
                dark = 'dark' in subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'],
                                                capture_output=True, text=True).stdout.lower()
            else:
                dark = 'dark' in subprocess.run(['gsettings', 'get', 'org.gnome.desktop.interface', 'color-scheme'],
                                                capture_output=True, text=True).stdout.lower()
        except Exception:
            pass
        return GUI.THEMES['Dark'] if dark else GUI.THEMES['Light']

    def __loadTheme(self):
        """The saved theme, the one of the OS as long as none was chosen"""
        theme = conf.loadConf(self.__settingsPath(), dict(), self.scriptDir).get('theme')
        return theme if theme in self.THEMES.values() else self.__osTheme()

    def __customizeStyle(self):
        """What is added to the theme, to be done again each time the theme is changed"""
        style = self.style
        tabstyle.roundTabs(style, noSelection=self.settingsOpen.get() if self.settingsOpen else False)
        style.configure('TLabelframe.Label', font=self.sectionFont)
        style.configure('TNotebook', lightcolor=style.colors.border, bordercolor=style.colors.border)
        # the theme doesn't render disabled checkbuttons differently from enabled ones
        disabledColor = tabstyle.mix(style.colors.fg, style.colors.bg, 0.6)
        disabledBackground = tabstyle.mix(style.colors.bg, style.colors.border, 0.4)
        # some room between the box and its label
        # (set through Tk directly, ttkbootstrap would restyle the checkbuttons entirely)
        style.master.tk.call('ttk::style', 'configure', 'TCheckbutton', '-indicatormargin', [0, 0, 5, 0])
        style.map('TCheckbutton', foreground=[('disabled', disabledColor)],
                  indicatorforeground=[('disabled', disabledColor)],
                  indicatorbackground=[('disabled', disabledBackground)])
        self.gearImage = tabstyle.gearIcon(style.colors.fg)
        if self.settingsButton:
            self.settingsButton.configure(image=self.gearImage)
        if self.logTest:
            self.__colorConsole()
        self.__colorComboboxLists()
        tabstyle.tabTextColors(style, self.settingsOpen.get() if self.settingsOpen else False)
        tabstyle.gearButtonColors(style)

    def __colorComboboxLists(self):
        """The lists of the comboboxes are plain Tk listboxes the theme doesn't color"""
        colors = self.style.colors
        options = {'background': colors.inputbg, 'foreground': colors.inputfg,
                   'selectbackground': colors.selectbg, 'selectforeground': colors.selectfg}
        # for the lists not yet created, which take their colors from the option database
        for option, color in options.items():
            self.window.option_add('*TCombobox*Listbox.' + option, color)

        def recolor(widget):
            if isinstance(widget, ttk.Combobox):
                popdownList = str(self.window.tk.call('ttk::combobox::PopdownWindow', str(widget))) + '.f.l'
                for option, color in options.items():
                    self.window.tk.call(popdownList, 'configure', '-' + option, color)
            for child in widget.winfo_children():
                recolor(child)

        recolor(self.window)

    def changeTheme(self, theme):
        self.style.theme_use(theme)
        # the theme finishes its own styling when events are processed, it would replace what is added to it
        self.window.update()
        self.__customizeStyle()
        self.theme = theme
        conf.saveSettings(self.__settingsPath(), {'theme': theme})

    def draw(self):
        self.root = ttk.Frame(self.window, padding=(10, 5))
        self.root.grid(column=0, row=0)
        self.__drawMainframe()
        self.window.mainloop()

    def __setFontSize(self, value):
        default_font = Font.nametofont("TkDefaultFont")
        default_font.configure(size=value)
        text_font = Font.nametofont("TkTextFont")
        text_font.configure(size=value)
        fixed_font = Font.nametofont("TkFixedFont")
        fixed_font.configure(size=value)
        self.sectionFont.configure(size=value)

    # MAINFRAME, NOTEBOOK & TABS

    def __drawMainframe(self):
        self.mainFrame = ttk.Frame(self.root, padding=(10, 0))
        self.mainFrame.grid(column=0, row=1, sticky="EW", pady=5)
        self.mainFrame.grid_columnconfigure(0, weight=1)
        self.notebook = ttk.Notebook(self.mainFrame)
        self.notebook.grid(column=0, row=0, sticky="EW", pady=5)
        self.notebook.grid_columnconfigure(0, weight=1)

        self.tabFrames = dict()
        for setKey, title in self.TABS:
            self.__drawTab(setKey, title)
        self.__drawSettings()

        self.notebook.select(self.tabFrames['retroarch'])
        self.notebook.bind('<<NotebookTabChanged>>', lambda event: self.window.after_idle(self.__clearTabFocus))
        self.__drawConsole()
        self.__alignSettingsButton()

    def __drawTab(self, setKey, title):
        frame = ttk.Frame(self.notebook, padding=(10, 5))
        frame.grid(column=0, row=0, sticky="EWN", pady=5)
        frame.grid_columnconfigure(0, weight=1)
        self.notebook.add(frame, text=title, sticky="EWNS")
        self.notebook.select(frame)
        self.tabFrames[setKey] = frame
        if setKey == 'retroarch':
            RetroarchGUI(frame, self.scriptDir, self.logger, self).draw()
        else:
            ArcadeGUI(frame, setKey, self.scriptDir, self.logger, self).draw()

    # a notebook gives the focus to the first widget of the tab it opens, which selects the text of an entry
    def __clearTabFocus(self):
        self.notebook.focus_set()

        def clearSelection(widget):
            if isinstance(widget, ttk.Entry):
                widget.selection_clear()
            for child in widget.winfo_children():
                clearSelection(child)

        clearSelection(self.notebook.nametowidget(self.notebook.select()))

    # gear button at the right end of the tab strip, a notebook cannot align one of its tabs to the right
    # the settings page is laid over the pages of the notebook and the tabs are drawn without a selected one
    def __drawSettings(self):
        self.settingsOpen = Tk.BooleanVar(value=False)
        self.settingsButton = ttk.Checkbutton(self.notebook, image=self.gearImage, style='Toolbutton',
                                              variable=self.settingsOpen, command=self.__toggleSettings)
        self.settingsButton.place(relx=1.0, x=-2, y=0, anchor='ne')
        wckToolTips.register(self.settingsButton, 'Settings')
        self.settingsFrame = ttk.Frame(self.notebook, padding=(10, 5))
        self.settingsFrame.grid_columnconfigure(0, weight=1)
        SettingsGUI(self.settingsFrame, self).draw()
        self.notebook.bind('<ButtonPress-1>', self.__tabClicked)

    # the button is as high as the tabs, whatever the height the theme gives it, so its icon is centered on them
    # and it stays above the border line of the pages
    def __alignSettingsButton(self):
        self.window.update_idletasks()
        page = self.notebook.nametowidget(self.notebook.select())
        self.settingsButton.place_configure(y=1, height=page.winfo_y() - 3)

    def __toggleSettings(self):
        if self.settingsOpen.get():
            self.notebook.update_idletasks()
            page = self.notebook.nametowidget(self.notebook.select())
            self.settingsFrame.place(x=page.winfo_x(), y=page.winfo_y(), width=page.winfo_width(),
                                     height=page.winfo_height())
            self.settingsFrame.lift()
        else:
            self.settingsFrame.place_forget()
        tabstyle.roundTabs(self.style, noSelection=self.settingsOpen.get())
        tabstyle.tabTextColors(self.style, self.settingsOpen.get())

    def __tabClicked(self, event):
        # clicking a tab, even the selected one, leaves the settings
        if self.settingsOpen.get() and self.notebook.identify(event.x, event.y):
            self.settingsOpen.set(False)
            self.__toggleSettings()

    def disableOtherTabs(self, setKey, disable=True):
        state = 'disabled' if disable else 'normal'
        for key, frame in self.tabFrames.items():
            if key != setKey:
                self.notebook.tab(frame, state=state)

    # CONSOLE STUFF

    # Console Frame
    def __drawConsole(self):
        self.consoleFrame = ttk.Frame(self.root, padding=(10, 0))
        self.consoleFrame.grid(column=0, row=5, sticky="EW", pady=5)
        self.consoleFrame.grid_columnconfigure(0, weight=1)
        self.logTest = Tk.Text(self.consoleFrame, height=16, state='disabled', wrap='word')
        self.logTest.grid(column=0, row=0, sticky="EW")
        self.__colorConsole()
        self.logTest.tag_config('ERROR', background='black', foreground='red')
        self.logTest.tag_config('WARNING', background='black', foreground='orange')
        self.logTest.tag_config('INFO', background='black', foreground='yellow')
        self.logTest.tag_config('SUCCESS', background='black', foreground='green2')
        self.logTest.tag_config('UNKNOWN', background='black', foreground='deep sky blue')
        self.scrollbar = ttk.Scrollbar(self.consoleFrame, orient=Tk.VERTICAL, command=self.logTest.yview)
        self.scrollbar.grid(column=1, row=0, sticky=(Tk.N, Tk.S))
        self.logTest['yscrollcommand'] = self.scrollbar.set
        self.logTest.after(10, self.updateConsoleFromQueue)

    # The theme gives its own colors to text widgets each time it is changed, the console is always black
    def __colorConsole(self):
        self.logTest.configure(background='black', foreground='yellow')

    # Grabs messages from logger queue
    def updateConsoleFromQueue(self):
        while not self.logger.log_queue.empty():
            line = self.logger.log_queue.get()
            self.__writeToConsole(line)
            self.root.update_idletasks()
        self.logTest.after(10, self.updateConsoleFromQueue)

    def __writeToConsole(self, msg):
        numlines = self.logTest.index('end - 1 line').split('.')[0]
        self.logTest['state'] = 'normal'
        if numlines == 24:
            self.logTest.delete(1.0, 2.0)
        # previousLine = self.logTest.get('end-1c linestart', 'end-1c')
        # # handle progress bar
        # if msg[1] and previousLine.startswith('    [') and previousLine.endswith(']'):
        #     self.logTest.delete('end-1c linestart', 'end')

        if self.logTest.index('end-1c') != '1.0':
            self.logTest.insert('end', '\n')
        self.logTest.insert('end', msg[2], msg[0])
        self.logTest.see(Tk.END)
        self.logTest['state'] = 'disabled'
