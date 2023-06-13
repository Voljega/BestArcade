import tkinter as Tk
import tkinter.font as Font
from retroarchgui import RetroarchGUI
from customgui import CustomGUI
import platform
import wckToolTips


class GUI:
    MACOS_DEFAULT_FONT_SIZE = 7
    DEFAULT_FONT_SIZE = 9

    def __init__(self, scriptDir, logger, title):
        self.scriptDir = scriptDir

        self.window = Tk.Tk()
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
        self.root = Tk.Frame(self.window, padx=10, pady=5)
        self.root.grid(column=0, row=0)
        self.__drawSliderFrame()
        self.__drawMainframe()
        self.window.mainloop()

    def __setFontSize(self, value):
        default_font = Font.nametofont("TkDefaultFont")
        default_font.configure(size=value)
        text_font = Font.nametofont("TkTextFont")
        text_font.configure(size=value)
        fixed_font = Font.nametofont("TkFixedFont")
        fixed_font.configure(size=value)

    def __drawSliderFrame(self):
        self.sliderFrame = Tk.Frame(self.root, padx=10, pady=0)
        self.sliderFrame.grid(column=0, row=0, sticky="EW", pady=0)
        self.sliderFrame.grid_columnconfigure(0, weight=1)
        self.slider = Tk.Scale(self.sliderFrame, from_=4, to=12, orient=Tk.HORIZONTAL, showvalue=0,
                               command=self.__setFontSize)
        wckToolTips.register(self.slider, 'Window Size')  # TODO internationalization
        self.slider.grid(column=0, row=0, sticky="W", pady=0)
        self.slider.set(self.startFontSize)

    # MAINFRAME, NOTEBOOK & TABS

    def __drawMainframe(self):
        self.mainFrame = Tk.Frame(self.root, padx=10, pady=0)
        self.mainFrame.grid(column=0, row=1, sticky="EW", pady=5)
        self.mainFrame.grid_columnconfigure(0, weight=1)
        self.notebook = Tk.ttk.Notebook(self.mainFrame)
        self.notebook.grid(column=0, row=0, sticky="EW", pady=5)
        self.notebook.grid_columnconfigure(0, weight=1)

        # PI3 RETROARCH TAB
        self.pi3RetroarchFrame = Tk.Frame(self.notebook, padx=10, pady=5)
        self.pi3RetroarchFrame.grid(column=0, row=0, sticky="EW", pady=5)
        self.pi3RetroarchFrame.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.pi3RetroarchFrame, text='Retroarch-Pi3', sticky="EW")
        self.notebook.select(self.pi3RetroarchFrame)
        pi3RetroarchGUI = RetroarchGUI(self.pi3RetroarchFrame, self.scriptDir, self.logger, self, 'pi3')
        pi3RetroarchGUI.draw()

        # N2 RETROARCH TAB
        self.n2RetroarchFrame = Tk.Frame(self.notebook, padx=10, pady=5)
        self.n2RetroarchFrame.grid(column=0, row=0, sticky="EWN", pady=5)
        self.n2RetroarchFrame.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.n2RetroarchFrame, text='Retroarch-N2', sticky="EWNS")
        self.notebook.select(self.n2RetroarchFrame)
        n2RetroarchGUI = RetroarchGUI(self.n2RetroarchFrame, self.scriptDir, self.logger, self, 'n2')
        n2RetroarchGUI.draw()

        # N2 RETROARCH TAB
        self.n100RetroarchFrame = Tk.Frame(self.notebook, padx=10, pady=5)
        self.n100RetroarchFrame.grid(column=0, row=0, sticky="EWN", pady=5)
        self.n100RetroarchFrame.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.n100RetroarchFrame, text='Retroarch-N100', sticky="EWNS")
        self.notebook.select(self.n100RetroarchFrame)
        n100RetroarchGUI = RetroarchGUI(self.n100RetroarchFrame, self.scriptDir, self.logger, self, 'n100')
        n100RetroarchGUI.draw()

        # CUSTOM TAB
        self.customFrame = Tk.Frame(self.notebook, padx=10, pady=5)
        self.customFrame.grid(column=0, row=0, sticky="EWN", pady=5)
        self.customFrame.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.customFrame, text='Custom', sticky="EWNS")
        self.notebook.select(self.customFrame)
        customGUI = CustomGUI(self.customFrame, 'custom', self.scriptDir, self.logger, self)
        customGUI.draw()

        # NEOGEOAES TAB
        self.neogeoaesFrame = Tk.Frame(self.notebook, padx=10, pady=5)
        self.neogeoaesFrame.grid(column=0, row=0, sticky="EWN", pady=5)
        self.neogeoaesFrame.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.neogeoaesFrame, text='Neo Geo AES', sticky="EWNS")
        self.notebook.select(self.neogeoaesFrame)
        neogeoaesGUI = CustomGUI(self.neogeoaesFrame, 'neogeoaes', self.scriptDir, self.logger, self)
        neogeoaesGUI.draw()

        # MODEL2 TAB
        self.model2Frame = Tk.Frame(self.notebook, padx=10, pady=5)
        self.model2Frame.grid(column=0, row=0, sticky="EWN", pady=5)
        self.model2Frame.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.model2Frame, text='Sega Model 2', sticky="EWNS")
        self.notebook.select(self.model2Frame)
        model2GUI = CustomGUI(self.model2Frame, 'model2', self.scriptDir, self.logger, self)
        model2GUI.draw()

        # MODEL3 TAB
        self.model3Frame = Tk.Frame(self.notebook, padx=10, pady=5)
        self.model3Frame.grid(column=0, row=0, sticky="EWN", pady=5)
        self.model3Frame.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.model3Frame, text='Sega Model 3', sticky="EWNS")
        self.notebook.select(self.model3Frame)
        model3GUI = CustomGUI(self.model3Frame, 'model3', self.scriptDir, self.logger, self)
        model3GUI.draw()

        # ATOMISWAVE TAB
        self.atomiswaveFrame = Tk.Frame(self.notebook, padx=10, pady=5)
        self.atomiswaveFrame.grid(column=0, row=0, sticky="EWN", pady=5)
        self.atomiswaveFrame.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.atomiswaveFrame, text='Atomiswave', sticky="EWNS")
        self.notebook.select(self.atomiswaveFrame)
        atomiswaveGUI = CustomGUI(self.atomiswaveFrame, 'atomiswave', self.scriptDir, self.logger, self)
        atomiswaveGUI.draw()

        # NAOMI TAB
        self.naomiFrame = Tk.Frame(self.notebook, padx=10, pady=5)
        self.naomiFrame.grid(column=0, row=0, sticky="EWN", pady=5)
        self.naomiFrame.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.naomiFrame, text='Naomi', sticky="EWNS")
        self.notebook.select(self.naomiFrame)
        naomiGUI = CustomGUI(self.naomiFrame, 'naomi', self.scriptDir, self.logger, self)
        naomiGUI.draw()

        # NAOMI2 TAB
        self.naomi2Frame = Tk.Frame(self.notebook, padx=10, pady=5)
        self.naomi2Frame.grid(column=0, row=0, sticky="EWN", pady=5)
        self.naomi2Frame.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.naomi2Frame, text='Naomi 2', sticky="EWNS")
        self.notebook.select(self.naomi2Frame)
        naomi2GUI = CustomGUI(self.naomi2Frame, 'naomi2', self.scriptDir, self.logger, self)
        naomi2GUI.draw()

        # HANDHELD TAB
        self.handheldFrame = Tk.Frame(self.notebook, padx=10, pady=5)
        self.handheldFrame.grid(column=0, row=0, sticky="EWN", pady=5)
        self.handheldFrame.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.handheldFrame, text='Handhelds', sticky="EWNS")
        self.notebook.select(self.handheldFrame)
        handheldGUI = CustomGUI(self.handheldFrame, 'handheld', self.scriptDir, self.logger, self)
        handheldGUI.draw()

        # TVGAMES TAB
        self.tvgamesFrame = Tk.Frame(self.notebook, padx=10, pady=5)
        self.tvgamesFrame.grid(column=0, row=0, sticky="EWN", pady=5)
        self.tvgamesFrame.grid_columnconfigure(0, weight=1)
        self.notebook.add(self.tvgamesFrame, text='TV Games', sticky="EWNS")
        self.notebook.select(self.tvgamesFrame)
        tvgamesGUI = CustomGUI(self.tvgamesFrame, 'tvgames', self.scriptDir, self.logger, self)
        tvgamesGUI.draw()

        self.notebook.select(self.pi3RetroarchFrame)
        self.__drawConsole()

    def disableOtherTabs(self, setKey, hardware, disable=True):
        state = 'disabled' if disable else 'normal'
        if setKey == 'retroarch' and hardware == 'pi3':
            self.notebook.tab(self.n2RetroarchFrame, state=state)
            self.notebook.tab(self.n100RetroarchFrame, state=state)
            self.notebook.tab(self.customFrame, state=state)
            self.notebook.tab(self.neogeoaesFrame, state=state)
            self.notebook.tab(self.model2Frame, state=state)
            self.notebook.tab(self.model3Frame, state=state)
            self.notebook.tab(self.atomiswaveFrame, state=state)
            self.notebook.tab(self.naomiFrame, state=state)
            self.notebook.tab(self.naomi2Frame, state=state)
            self.notebook.tab(self.handheldFrame, state=state)
            self.notebook.tab(self.tvgamesFrame, state=state)
        elif setKey == 'retroarch' and hardware == 'n2':
            self.notebook.tab(self.pi3RetroarchFrame, state=state)
            self.notebook.tab(self.n100RetroarchFrame, state=state)
            self.notebook.tab(self.customFrame, state=state)
            self.notebook.tab(self.neogeoaesFrame, state=state)
            self.notebook.tab(self.model2Frame, state=state)
            self.notebook.tab(self.model3Frame, state=state)
            self.notebook.tab(self.atomiswaveFrame, state=state)
            self.notebook.tab(self.naomiFrame, state=state)
            self.notebook.tab(self.naomi2Frame, state=state)
            self.notebook.tab(self.handheldFrame, state=state)
            self.notebook.tab(self.tvgamesFrame, state=state)
        elif setKey == 'retroarch' and hardware == 'n100':
            self.notebook.tab(self.pi3RetroarchFrame, state=state)
            self.notebook.tab(self.n2RetroarchFrame, state=state)
            self.notebook.tab(self.customFrame, state=state)
            self.notebook.tab(self.neogeoaesFrame, state=state)
            self.notebook.tab(self.model2Frame, state=state)
            self.notebook.tab(self.model3Frame, state=state)
            self.notebook.tab(self.atomiswaveFrame, state=state)
            self.notebook.tab(self.naomiFrame, state=state)
            self.notebook.tab(self.naomi2Frame, state=state)
            self.notebook.tab(self.handheldFrame, state=state)
            self.notebook.tab(self.tvgamesFrame, state=state)
        elif setKey == 'custom':
            self.notebook.tab(self.pi3RetroarchFrame, state=state)
            self.notebook.tab(self.n2RetroarchFrame, state=state)
            self.notebook.tab(self.n100RetroarchFrame, state=state)
            self.notebook.tab(self.neogeoaesFrame, state=state)
            self.notebook.tab(self.model2Frame, state=state)
            self.notebook.tab(self.model3Frame, state=state)
            self.notebook.tab(self.atomiswaveFrame, state=state)
            self.notebook.tab(self.naomiFrame, state=state)
            self.notebook.tab(self.naomi2Frame, state=state)
            self.notebook.tab(self.handheldFrame, state=state)
            self.notebook.tab(self.tvgamesFrame, state=state)
        elif setKey == 'neogeoaes':
            self.notebook.tab(self.pi3RetroarchFrame, state=state)
            self.notebook.tab(self.n2RetroarchFrame, state=state)
            self.notebook.tab(self.n100RetroarchFrame, state=state)
            self.notebook.tab(self.customFrame, state=state)
            self.notebook.tab(self.model2Frame, state=state)
            self.notebook.tab(self.model3Frame, state=state)
            self.notebook.tab(self.atomiswaveFrame, state=state)
            self.notebook.tab(self.naomiFrame, state=state)
            self.notebook.tab(self.naomi2Frame, state=state)
            self.notebook.tab(self.handheldFrame, state=state)
            self.notebook.tab(self.tvgamesFrame, state=state)
        elif setKey == 'model2':
            self.notebook.tab(self.pi3RetroarchFrame, state=state)
            self.notebook.tab(self.n2RetroarchFrame, state=state)
            self.notebook.tab(self.n100RetroarchFrame, state=state)
            self.notebook.tab(self.customFrame, state=state)
            self.notebook.tab(self.neogeoaesFrame, state=state)
            self.notebook.tab(self.model3Frame, state=state)
            self.notebook.tab(self.atomiswaveFrame, state=state)
            self.notebook.tab(self.naomiFrame, state=state)
            self.notebook.tab(self.naomi2Frame, state=state)
            self.notebook.tab(self.handheldFrame, state=state)
            self.notebook.tab(self.tvgamesFrame, state=state)
        elif setKey == 'model3':
            self.notebook.tab(self.pi3RetroarchFrame, state=state)
            self.notebook.tab(self.n2RetroarchFrame, state=state)
            self.notebook.tab(self.n100RetroarchFrame, state=state)
            self.notebook.tab(self.customFrame, state=state)
            self.notebook.tab(self.neogeoaesFrame, state=state)
            self.notebook.tab(self.model2Frame, state=state)
            self.notebook.tab(self.atomiswaveFrame, state=state)
            self.notebook.tab(self.naomiFrame, state=state)
            self.notebook.tab(self.naomi2Frame, state=state)
            self.notebook.tab(self.handheldFrame, state=state)
            self.notebook.tab(self.tvgamesFrame, state=state)
        elif setKey == 'atomiswave':
            self.notebook.tab(self.pi3RetroarchFrame, state=state)
            self.notebook.tab(self.n2RetroarchFrame, state=state)
            self.notebook.tab(self.n100RetroarchFrame, state=state)
            self.notebook.tab(self.customFrame, state=state)
            self.notebook.tab(self.neogeoaesFrame, state=state)
            self.notebook.tab(self.model2Frame, state=state)
            self.notebook.tab(self.model3Frame, state=state)
            self.notebook.tab(self.naomiFrame, state=state)
            self.notebook.tab(self.naomi2Frame, state=state)
            self.notebook.tab(self.handheldFrame, state=state)
            self.notebook.tab(self.tvgamesFrame, state=state)
        elif setKey == 'naomi':
            self.notebook.tab(self.pi3RetroarchFrame, state=state)
            self.notebook.tab(self.n2RetroarchFrame, state=state)
            self.notebook.tab(self.n100RetroarchFrame, state=state)
            self.notebook.tab(self.customFrame, state=state)
            self.notebook.tab(self.neogeoaesFrame, state=state)
            self.notebook.tab(self.model2Frame, state=state)
            self.notebook.tab(self.model3Frame, state=state)
            self.notebook.tab(self.atomiswaveFrame, state=state)
            self.notebook.tab(self.naomi2Frame, state=state)
            self.notebook.tab(self.handheldFrame, state=state)
            self.notebook.tab(self.tvgamesFrame, state=state)
        elif setKey == 'naomi2':
            self.notebook.tab(self.pi3RetroarchFrame, state=state)
            self.notebook.tab(self.n2RetroarchFrame, state=state)
            self.notebook.tab(self.n100RetroarchFrame, state=state)
            self.notebook.tab(self.customFrame, state=state)
            self.notebook.tab(self.neogeoaesFrame, state=state)
            self.notebook.tab(self.model2Frame, state=state)
            self.notebook.tab(self.model3Frame, state=state)
            self.notebook.tab(self.atomiswaveFrame, state=state)
            self.notebook.tab(self.naomiFrame, state=state)
            self.notebook.tab(self.handheldFrame, state=state)
            self.notebook.tab(self.tvgamesFrame, state=state)
        elif setKey == 'handheld':
            self.notebook.tab(self.pi3RetroarchFrame, state=state)
            self.notebook.tab(self.n2RetroarchFrame, state=state)
            self.notebook.tab(self.n100RetroarchFrame, state=state)
            self.notebook.tab(self.customFrame, state=state)
            self.notebook.tab(self.neogeoaesFrame, state=state)
            self.notebook.tab(self.model2Frame, state=state)
            self.notebook.tab(self.model3Frame, state=state)
            self.notebook.tab(self.atomiswaveFrame, state=state)
            self.notebook.tab(self.naomiFrame, state=state)
            self.notebook.tab(self.naomi2Frame, state=state)
            self.notebook.tab(self.tvgamesFrame, state=state)
        elif setKey == 'tvgames':
            self.notebook.tab(self.pi3RetroarchFrame, state=state)
            self.notebook.tab(self.n2RetroarchFrame, state=state)
            self.notebook.tab(self.n100RetroarchFrame, state=state)
            self.notebook.tab(self.customFrame, state=state)
            self.notebook.tab(self.neogeoaesFrame, state=state)
            self.notebook.tab(self.model2Frame, state=state)
            self.notebook.tab(self.model3Frame, state=state)
            self.notebook.tab(self.atomiswaveFrame, state=state)
            self.notebook.tab(self.naomiFrame, state=state)
            self.notebook.tab(self.naomi2Frame, state=state)
            self.notebook.tab(self.handheldFrame, state=state)

    # CONSOLE STUFF

    # Console Frame
    def __drawConsole(self):
        self.consoleFrame = Tk.Frame(self.root, padx=10)
        self.consoleFrame.grid(column=0, row=5, sticky="EW", pady=5)
        self.consoleFrame.grid_columnconfigure(0, weight=1)
        self.logTest = Tk.Text(self.consoleFrame, height=15, state='disabled', wrap='word', background='black',
                               foreground='yellow')
        self.logTest.grid(column=0, row=0, sticky="EW")
        self.logTest.tag_config('ERROR', background='black', foreground='red')
        self.logTest.tag_config('WARNING', background='black', foreground='orange')
        self.logTest.tag_config('INFO', background='black', foreground='yellow')
        self.logTest.tag_config('SUCCESS', background='black', foreground='green2')
        self.logTest.tag_config('UNKNOWN', background='black', foreground='deep sky blue')
        self.scrollbar = Tk.Scrollbar(self.consoleFrame, orient=Tk.VERTICAL, command=self.logTest.yview)
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
