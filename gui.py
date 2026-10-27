import tkinter as Tk
import tkinter.font as Font
from tkinter import ttk
import ttkbootstrap
import tabstyle
from retroarchgui import RetroarchGUI
from customgui import CustomGUI
import platform


class GUI:
    MACOS_DEFAULT_FONT_SIZE = 7
    DEFAULT_FONT_SIZE = 9
    THEME = 'flatly'
    TABS = [('retroarch', 'Retroarch'), ('custom', 'Custom'), ('neogeoaes', 'Neo Geo AES'),
            ('model2', 'Sega Model 2'), ('model3', 'Sega Model 3'), ('atomiswave', 'Atomiswave'),
            ('naomi', 'Naomi'), ('naomi2', 'Naomi 2'), ('namco2x6', 'Namco 2x6'), ('handheld', 'Handhelds'),
            ('tvgames', 'TV Games')]
    DISABLED_COLOR = '#adb5bd'
    DISABLED_BACKGROUND = '#e9ecef'

    def __init__(self, scriptDir, logger, title):
        self.scriptDir = scriptDir

        self.window = Tk.Tk()
        style = ttkbootstrap.Style(theme=self.THEME)
        tabstyle.roundTabs(style)
        # section titles in bold
        self.sectionFont = Font.Font(font=Font.nametofont('TkDefaultFont'))
        self.sectionFont.configure(weight='bold')
        style.configure('TLabelframe.Label', font=self.sectionFont)
        # the theme doesn't render disabled checkbuttons differently from enabled ones
        style.map('TCheckbutton', foreground=[('disabled', self.DISABLED_COLOR)],
                  indicatorforeground=[('disabled', self.DISABLED_COLOR)],
                  indicatorcolor=[('disabled', self.DISABLED_BACKGROUND)])
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

        self.notebook.select(self.tabFrames['retroarch'])
        self.__drawConsole()

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
            CustomGUI(frame, setKey, self.scriptDir, self.logger, self).draw()

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
        self.logTest = Tk.Text(self.consoleFrame, height=16, state='disabled', wrap='word', background='black',
                               foreground='yellow')
        self.logTest.grid(column=0, row=0, sticky="EW")
        self.logTest.tag_config('ERROR', background='black', foreground='red')
        self.logTest.tag_config('WARNING', background='black', foreground='orange')
        self.logTest.tag_config('INFO', background='black', foreground='yellow')
        self.logTest.tag_config('SUCCESS', background='black', foreground='green2')
        self.logTest.tag_config('UNKNOWN', background='black', foreground='deep sky blue')
        self.scrollbar = ttk.Scrollbar(self.consoleFrame, orient=Tk.VERTICAL, command=self.logTest.yview)
        self.scrollbar.grid(column=1, row=0, sticky=(Tk.N, Tk.S))
        self.logTest['yscrollcommand'] = self.scrollbar.set
        self.logTest.after(10, self.updateConsoleFromQueue)

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
