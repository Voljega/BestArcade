import conf
import utils
import tkinter as Tk
from tkinter import ttk, messagebox, filedialog
import os.path
import shutil
import platform
from operator import attrgetter
from basicsorter import BasicSorter
import _thread
import wckToolTips
from functools import partial


class CustomGUI:

    def __init__(self, rootFrame, setKey, scriptDir, logger, mummy):
        self.tabFrame = rootFrame
        self.setKey = setKey
        self.scriptDir = scriptDir
        self.logger = logger
        self.mummy = mummy
        self.configuration = conf.loadConf(
            os.path.join(self.scriptDir, utils.confDir, utils.getConfFilename(self.setKey)))
        self.logger.log('Loaded ' + utils.getConfFilename(self.setKey))
        self.guiVars = dict()
        self.guiStrings = utils.loadUIStrings(self.scriptDir, utils.getGuiStringsFilename(self.setKey))

        # Init all components
        self.romsetFrame = None
        self.selectRomsetDirButton = None
        self.selectCHDDirButton = None
        self.imagesFrame = None
        self.parametersFrame = None
        self.buttonsFrame = None
        self.verifyButton = None
        self.saveButton = None
        self.proceedButton = None
        self.datButton = None

    def draw(self):
        self.__drawRomsetFrame()
        self.__drawImagesFrame()
        self.__drawParametersFrame()
        self.__drawButtonsFrame()

    def __drawRomsetFrame(self):
        # Romsets frame
        self.romsetFrame = Tk.LabelFrame(self.tabFrame, text="Your Romset", padx=10, pady=5)
        self.romsetFrame.grid(column=0, row=0, sticky="EW", pady=5)
        self.romsetFrame.grid_columnconfigure(1, weight=1)
        setRow = 0

        label = Tk.Label(self.romsetFrame, text=self.guiStrings[self.setKey].label)
        wckToolTips.register(label, self.guiStrings[self.setKey].help)
        label.grid(column=0, row=setRow, padx=5, sticky="W")
        self.guiVars[self.setKey] = Tk.StringVar()
        self.guiVars[self.setKey].set(self.configuration[self.setKey])
        entry = Tk.Entry(self.romsetFrame, textvariable=self.guiVars[self.setKey])
        entry.grid(column=1, row=setRow, padx=5, sticky="WE")
        self.selectRomsetDirButton = Tk.Button(self.romsetFrame, text=self.guiStrings['selectRomsetDir'].label,
                                               command=lambda: self.__openFileExplorer(True, self.setKey, None))
        self.selectRomsetDirButton.grid(column=2, row=setRow, padx=5, sticky="WE")
        wckToolTips.register(self.selectRomsetDirButton, self.guiStrings['selectRomsetDir'].help)
        setRow = setRow + 1

        if self.setKey not in ['handheld', 'tvgames']:
            label = Tk.Label(self.romsetFrame, text=self.guiStrings['chd'].label)
            wckToolTips.register(label, self.guiStrings['chd'].help)
            label.grid(column=0, row=setRow, padx=5, sticky="W")
            self.guiVars['chd'] = Tk.StringVar()
            self.guiVars['chd'].set(self.configuration['chd'])
            entry = Tk.Entry(self.romsetFrame, textvariable=self.guiVars['chd'])
            entry.grid(column=1, row=setRow, padx=5, sticky="WE")
            self.selectCHDDirButton = Tk.Button(self.romsetFrame, text=self.guiStrings['selectCHDDir'].label,
                                                   command=lambda: self.__openFileExplorer(True, 'chd', None))
            self.selectCHDDirButton.grid(column=2, row=setRow, padx=5, sticky="WE")
            wckToolTips.register(self.selectCHDDirButton, self.guiStrings['selectCHDDir'].help)
            setRow = setRow + 1

        label = Tk.Label(self.romsetFrame, text=self.guiStrings['dat'].label)
        wckToolTips.register(label, self.guiStrings['dat'].help)
        label.grid(column=0, row=setRow, padx=5, sticky="W")
        self.guiVars['dat'] = Tk.StringVar()
        self.guiVars['dat'].set(self.configuration['dat'])
        entry = Tk.Entry(self.romsetFrame, textvariable=self.guiVars['dat'])
        entry.grid(column=1, row=setRow, padx=5, sticky="WE")

        self.datButton = Tk.Button(self.romsetFrame, text=self.guiStrings['selectDat'].label,
                                   command=lambda: self.__openFileExplorer(False, 'dat', ['dat', 'xml']))
        self.datButton.grid(column=2, row=setRow, padx=5, sticky="WE")
        wckToolTips.register(self.datButton, self.guiStrings['selectDat'].help)
        setRow = setRow + 1

        ttk.Separator(self.romsetFrame, orient=Tk.HORIZONTAL).grid(column=0, row=setRow, columnspan=3, padx=5, pady=5,
                                                                   sticky="EW")
        setRow = setRow + 1
        outputDirLabel = Tk.Label(self.romsetFrame, text=self.guiStrings['exportDir'].label)
        wckToolTips.register(outputDirLabel, self.guiStrings['exportDir'].help)
        outputDirLabel.grid(column=0, row=setRow, padx=5, sticky="W")
        self.guiVars['exportDir'] = Tk.StringVar()
        self.guiVars['exportDir'].set(self.configuration['exportDir'])
        outputEntry = Tk.Entry(self.romsetFrame, textvariable=self.guiVars['exportDir'])
        outputEntry.grid(column=1, row=setRow, padx=5, sticky="WE")

        self.selectExportDirButton = Tk.Button(self.romsetFrame, text=self.guiStrings['selectExportDir'].label,
                                               command=lambda: self.__openFileExplorer(True, 'exportDir', None))
        self.selectExportDirButton.grid(column=2, row=setRow, padx=5, sticky="WE")
        wckToolTips.register(self.selectExportDirButton, self.guiStrings['selectExportDir'].help)

    def __drawImagesFrame(self):
        # Images frame
        self.imagesFrame = Tk.LabelFrame(self.tabFrame, text="Images", padx=10, pady=5)
        self.imagesFrame.grid(column=0, row=1, sticky="EW", pady=5)
        self.imagesFrame.grid_columnconfigure(1, weight=1)
        setRow = 0
        for path in self.configuration['images'].split('|'):
            pathLabel = self.guiStrings['images'].label + ' #' + str(setRow + 1)
            label = Tk.Label(self.imagesFrame, text=pathLabel)
            wckToolTips.register(label, self.guiStrings['images'].help)
            label.grid(column=0, row=setRow, padx=5, sticky="W")
            self.guiVars[pathLabel] = Tk.StringVar()
            self.guiVars[pathLabel].set(path.strip())
            entry = Tk.Entry(self.imagesFrame, textvariable=self.guiVars[pathLabel])
            entry.grid(column=1, row=setRow, padx=5, sticky="WE")
            selectImagesPathButton = Tk.Button(self.imagesFrame, text=self.guiStrings['selectImages'].label,
                                               command=lambda feLabel=pathLabel: self.__openFileExplorer(True, feLabel,
                                                                                                         None, feLabel))
            selectImagesPathButton.grid(column=2, row=setRow, padx=5, sticky="WE")
            wckToolTips.register(selectImagesPathButton, self.guiStrings['selectImages'].help)
            setRow = setRow + 1

        ttk.Separator(self.imagesFrame, orient=Tk.HORIZONTAL).grid(column=0, row=setRow, columnspan=3, padx=5, pady=5,
                                                                   sticky="EW")
        setRow = setRow + 1
        imgFormatLabel = Tk.Label(self.imagesFrame, text=self.guiStrings['imgNameFormat'].label)
        wckToolTips.register(imgFormatLabel, self.guiStrings['imgNameFormat'].help)
        imgFormatLabel.grid(column=0, row=setRow, padx=5, sticky=Tk.W)
        self.guiVars['imgNameFormat'] = Tk.StringVar()
        self.guiVars['imgNameFormat'].set(self.configuration['imgNameFormat'])
        # place entry in dict to retrieve later
        imgFormatEntry = Tk.Entry(self.imagesFrame, textvariable=self.guiVars['imgNameFormat'])
        imgFormatEntry.grid(column=1, row=setRow, columnspan=5, padx=5, sticky="W")

    def __drawParametersFrame(self):
        # Parameters frame
        self.parametersFrame = Tk.LabelFrame(self.tabFrame, text="Sorting Parameters", padx=10, pady=5)
        self.parametersFrame.grid(column=0, row=2, sticky="EW", pady=5)
        self.parametersFrame.grid_columnconfigure(1, weight=1)
        self.parametersFrame.grid_columnconfigure(4, weight=2)

        self.guiVars['dryRun'] = Tk.IntVar()
        self.guiVars['dryRun'].set(self.configuration['dryRun'])
        dryRunCheckButton = Tk.Checkbutton(self.parametersFrame, text=self.guiStrings['dryRun'].label,
                                           variable=self.guiVars['dryRun'], onvalue=1, offvalue=0)
        wckToolTips.register(dryRunCheckButton, self.guiStrings['dryRun'].help)
        dryRunCheckButton.grid(column=0, row=0, sticky="W")

        self.guiVars['genreSubFolders'] = Tk.IntVar()
        self.guiVars['genreSubFolders'].set(self.configuration['genreSubFolders'])
        useGenreSubFolderCheckButton = Tk.Checkbutton(self.parametersFrame,
                                                      text=self.guiStrings['genreSubFolders'].label,
                                                      variable=self.guiVars['genreSubFolders'], onvalue=1, offvalue=0)
        wckToolTips.register(useGenreSubFolderCheckButton, self.guiStrings['genreSubFolders'].help)
        useGenreSubFolderCheckButton.grid(column=2, row=0, sticky="W")

        self.guiVars['useImages'] = Tk.IntVar()
        self.guiVars['useImages'].set(self.configuration['useImages'])
        useImagesCheckButton = Tk.Checkbutton(self.parametersFrame, text=self.guiStrings['useImages'].label,
                                              variable=self.guiVars['useImages'], onvalue=1, offvalue=0)
        wckToolTips.register(useImagesCheckButton, self.guiStrings['useImages'].help)
        useImagesCheckButton.grid(column=3, row=0, sticky="W")

        if self.setKey not in ['handheld', 'tvgames']:
            self.guiVars['excludeCHDGames'] = Tk.IntVar()
            self.guiVars['excludeCHDGames'].set(self.configuration['excludeCHDGames'])
            excludeCHDGamesCheckButton = Tk.Checkbutton(self.parametersFrame, text=self.guiStrings['excludeCHDGames'].label,
                                                  variable=self.guiVars['excludeCHDGames'], onvalue=1, offvalue=0)
            wckToolTips.register(excludeCHDGamesCheckButton, self.guiStrings['excludeCHDGames'].help)
            excludeCHDGamesCheckButton.grid(column=4, row=0, sticky="W")

    def __drawButtonsFrame(self):
        self.buttonsFrame = Tk.Frame(self.tabFrame, padx=10)
        self.buttonsFrame.grid(column=0, row=3, sticky="EW", pady=5)
        emptyFrame = Tk.Frame(self.buttonsFrame, width=700, padx=10)
        emptyFrame.grid(column=0, row=0, columnspan=3, sticky="EW", pady=5)
        self.verifyButton = Tk.Button(self.buttonsFrame, text=self.guiStrings['verify'].label,
                                      command=self.__clickVerify)
        wckToolTips.register(self.verifyButton, self.guiStrings['verify'].help)
        self.verifyButton.grid(column=3, row=0, sticky="E", padx=3)
        self.saveButton = Tk.Button(self.buttonsFrame, text=self.guiStrings['save'].label, command=self.__clickSave)
        wckToolTips.register(self.saveButton, self.guiStrings['save'].help)
        self.saveButton.grid(column=4, row=0, sticky="E", padx=3)
        self.proceedButton = Tk.Button(self.buttonsFrame, text=self.guiStrings['proceed'].label,
                                       command=self.__clickProceed)
        wckToolTips.register(self.proceedButton, self.guiStrings['proceed'].help)
        self.proceedButton.grid(column=5, row=0, sticky="E", padx=3)

    def __clickSave(self):
        self.logger.log('\n<--------- Saving ' + self.setKey + ' configuration --------->')
        self.__saveConfFile()
        self.__saveConfInMem()

    def __saveConfFile(self):
        confBackupFilePath = os.path.join(self.scriptDir, utils.confDir, utils.getConfBakFilename(self.setKey))
        if os.path.exists(confBackupFilePath):
            os.remove(confBackupFilePath)
        shutil.copy2(os.path.join(self.scriptDir, utils.confDir, utils.getConfFilename(self.setKey)),
                     os.path.join(self.scriptDir, utils.confDir, utils.getConfBakFilename(self.setKey)))
        confFile = open(os.path.join(self.scriptDir, utils.confDir, utils.getConfFilename(self.setKey)), "w",
                        encoding="utf-8")
        listKeys = sorted(self.guiStrings.values(), key=attrgetter('order'))
        for key in listKeys:
            if key.id not in ['verify', 'save', 'proceed', 'confirm', 'selectRomsetDir', 'selectCHDDir', 'selectDat',
                              'selectExportDir', 'selectImages']:
                if key.help:
                    confFile.write('# ' + key.help.replace('#n', '\n# ') + '\n')
                if key.id == 'images':
                    imagesValue = self.guiVars[self.guiStrings['images'].label + ' #1'].get()
                    if self.guiStrings['images'].label + ' #2' in self.guiVars:
                        imagesValue = imagesValue + '|' + self.guiVars[self.guiStrings['images'].label + ' #2'].get()
                    confFile.write(key.id + ' = ' + imagesValue + '\n')
                else:
                    if key.id in self.guiVars:
                        confFile.write(key.id + ' = ' + str(self.guiVars[key.id].get()) + '\n')
        confFile.close()
        self.logger.log('    Configuration saved in ' + utils.getConfFilename(self.setKey) + ' file')

    def __saveConfInMem(self):
        listKeys = sorted(self.guiStrings.values(), key=attrgetter('order'))
        for key in listKeys:
            if key.id not in ['verify', 'save', 'proceed', 'confirm', 'selectRomsetDir', 'selectDat',
                              'selectExportDir', 'selectImages']:
                if key.id == 'images':
                    imagesValue = self.guiVars[self.guiStrings['images'].label + ' #1'].get()
                    if self.guiStrings['images'].label + ' #2' in self.guiVars:
                        imagesValue = imagesValue + '|' + self.guiVars[self.guiStrings['images'].label + ' #2'].get()
                    self.configuration['images'] = imagesValue
                else:
                    if key.id in self.guiVars:
                        self.configuration[key.id] = str(self.guiVars[key.id].get())
        self.logger.log('    Configuration saved in memory')

    def __clickVerify(self):
        self.logger.log('\n<--------- Verify ' + self.setKey + ' Parameters --------->')
        error = False
        for key in ['exportDir', self.setKey, 'chd', 'Images folder #1', 'Images folder #2']:
            if key in self.guiVars and not os.path.exists(self.guiVars[key].get()):
                error = True
                self.logger.log(key + ' folder does not exist', self.logger.ERROR)
        if not os.path.exists(self.guiVars['dat'].get()):
            error = True
            self.logger.log('dat does ' + self.guiVars['dat'].get() + ' not exist ', self.logger.ERROR)
        if self.guiVars['dryRun'].get() == 1:
            error = True
            self.logger.log(
                'WARNING: dryRun mode is used, only csv and gamelist files will be generated, '
                'roms and images will not be copied', self.logger.WARNING)
        if not error:
            self.logger.log('All Good!')

    def __clickProceed(self):
        self.logger.log('\n<--------- Saving ' + self.setKey + ' configuration --------->')
        self.__saveConfInMem()
        message = self.guiStrings['confirm'].help.replace('{outputDir}', self.guiVars['exportDir'].get()).replace('#n',
                                                                                                                  '\n')
        result = messagebox.askokcancel(self.guiStrings['confirm'].label, message)
        if result:
            self.verifyButton['state'] = 'disabled'
            self.saveButton['state'] = 'disabled'
            self.proceedButton['state'] = 'disabled'
            self.mummy.disableOtherTabs(self.setKey, None)
            self.logger.log('\n<--------- Starting ' + self.setKey + ' Process --------->')
            sorter = BasicSorter(self.configuration, self.scriptDir, partial(self.postProcess), self.logger,
                                 self.setKey)
            _thread.start_new(sorter.process, ())

    def postProcess(self):
        self.verifyButton['state'] = 'normal'
        self.saveButton['state'] = 'normal'
        self.proceedButton['state'] = 'normal'
        self.mummy.disableOtherTabs(self.setKey, None, False)

    # File Explorer for various vars
    def __openFileExplorer(self, openDir, var, fileTypes, label=None):
        if openDir:
            label = self.guiStrings[var].label if var in self.guiStrings else label
            result = filedialog.askdirectory(initialdir=self.guiVars[var].get(),
                                             title="Select your " + label)
        else:
            basedir = os.path.dirname(self.guiVars[var].get())
            initialDir = basedir if os.path.exists(basedir) else self.scriptDir
            fileTypes = list(map(lambda ft: ('Dat Files', '*.%s' % ft), fileTypes))
            result = filedialog.askopenfilename(initialdir=initialDir,
                                                title="Select your " + self.guiStrings[var].label,
                                                filetypes=fileTypes)
        if result != '':
            if platform.system() == 'Windows':
                result = result.replace('/', '\\')
            self.mummy.updateConsoleFromQueue()
            self.guiVars[var].set(result)
