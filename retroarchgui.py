import conf
import utils
import tkinter as Tk
from tkinter import ttk, messagebox, filedialog
import os.path
import shutil
import platform
from operator import attrgetter
from sorter import Sorter
import _thread
import wckToolTips
from functools import partial


class RetroarchGUI:
    GENRES = ['BeatEmUp', 'Gun', 'Misc', 'Platform', 'Puzzle', 'Race', 'RunNGun', 'ShootEmUp', 'Sport', 'VsFighting']
    GENRES_PER_ROW = 5
    GENRE_COMBOBOX_WIDTH = 12

    def __init__(self, rootFrame, scriptDir, logger, mummy):
        self.tabFrame = rootFrame
        self.scriptDir = scriptDir
        self.logger = logger
        self.mummy = mummy
        self.guiStrings = utils.loadUIStrings(self.scriptDir, utils.getGuiStringsFilename('retroarch'))
        self.configuration = conf.loadConf(
            os.path.join(self.scriptDir, utils.confDir, utils.getConfFilename('retroarch')),
            self.guiStrings, self.scriptDir)
        self.logger.log('Loaded ' + utils.getConfFilename('retroarch'))
        self.guiVars = dict()
        if not self.configuration['iniFile']:
            self.configuration['iniFile'] = os.path.join(self.scriptDir, utils.dataDir, Sorter.bigSetFile)

        # Init all components
        self.romsetFrame = None
        self.selectExportDirButton = None
        self.imagesFrame = None
        self.parametersFrame = None
        self.preferedSetLabel = None
        self.preferedSetComboBox = None
        self.preferedSetValues = None
        self.preferedSetForGenreFrame = None
        self.usePreferedSetForGenreCheckButton = None
        # (label, combobox) of each genre prefered set
        self.genreWidgets = []
        self.buttonsFrame = None
        self.verifyButton = None
        self.saveButton = None
        self.proceedButton = None

    def draw(self):
        self.__drawRomsetFrame()
        self.__drawImagesFrame()
        self.__drawParametersFrame()
        self.__drawButtonsFrame()

    def __drawRomsetFrame(self):
        # Romsets frame
        self.romsetFrame = ttk.LabelFrame(self.tabFrame, text="Your Romsets", padding=(10, 5))
        self.romsetFrame.grid(column=0, row=0, sticky="EW", pady=5)
        self.romsetFrame.grid_columnconfigure(1, weight=1)
        setRow = 0
        romsetKeys = Sorter.setKeys + ['chd']
        for key in romsetKeys:
            label = ttk.Label(self.romsetFrame, text=self.guiStrings[key].label)
            wckToolTips.register(label, self.guiStrings[key].help)
            label.grid(column=0, row=setRow, padx=5, sticky="W")
            self.guiVars[key] = Tk.StringVar()
            self.guiVars[key].set(self.configuration[key])
            entry = ttk.Entry(self.romsetFrame, textvariable=self.guiVars[key])
            entry.grid(column=1, row=setRow, padx=5, sticky="WE")
            selectRomsetDirButton = ttk.Button(
                self.romsetFrame, text=self.guiStrings['selectRomsetDir'].label,
                command=lambda setKey=key: self.__openFileExplorer(True, setKey, None, self.guiStrings[setKey].label))
            selectRomsetDirButton.grid(column=2, row=setRow, padx=5, sticky="WE")
            wckToolTips.register(selectRomsetDirButton, self.guiStrings['selectRomsetDir'].help)
            setRow = setRow + 1

        ttk.Separator(self.romsetFrame, orient=Tk.HORIZONTAL).grid(column=0, row=setRow, columnspan=3, padx=5, pady=5,
                                                                   sticky="EW")
        setRow = setRow + 1
        iniLabel = ttk.Label(self.romsetFrame, text=self.guiStrings['iniFile'].label)
        wckToolTips.register(iniLabel, self.guiStrings['iniFile'].help)
        iniLabel.grid(column=0, row=setRow, padx=5, sticky="W")
        self.guiVars['iniFile'] = Tk.StringVar()
        self.guiVars['iniFile'].set(self.configuration['iniFile'])
        iniEntry = ttk.Entry(self.romsetFrame, textvariable=self.guiVars['iniFile'])
        iniEntry.grid(column=1, row=setRow, padx=5, sticky="WE")
        self.selectIniButton = ttk.Button(self.romsetFrame, text=self.guiStrings['selectIni'].label,
                                         command=lambda: self.__openFileExplorer(False, 'iniFile', ['ini']))
        self.selectIniButton.grid(column=2, row=setRow, padx=5, sticky="WE")
        wckToolTips.register(self.selectIniButton, self.guiStrings['selectIni'].help)
        setRow = setRow + 1
        outputDirLabel = ttk.Label(self.romsetFrame, text=self.guiStrings['exportDir'].label)
        wckToolTips.register(outputDirLabel, self.guiStrings['exportDir'].help)
        outputDirLabel.grid(column=0, row=setRow, padx=5, sticky=Tk.W)
        self.guiVars['exportDir'] = Tk.StringVar()
        self.guiVars['exportDir'].set(self.configuration['exportDir'])
        outputEntry = ttk.Entry(self.romsetFrame, textvariable=self.guiVars['exportDir'])
        outputEntry.grid(column=1, row=setRow, padx=5, sticky="WE")

        self.selectExportDirButton = ttk.Button(self.romsetFrame, text=self.guiStrings['selectExportDir'].label,
                                               command=lambda: self.__openFileExplorer(True, 'exportDir', None))
        self.selectExportDirButton.grid(column=2, row=setRow, padx=5, sticky="WE")
        wckToolTips.register(self.selectExportDirButton, self.guiStrings['selectExportDir'].help)

    def __drawImagesFrame(self):
        # Images frame
        self.imagesFrame = ttk.LabelFrame(self.tabFrame, text="Images", padding=(10, 5))
        self.imagesFrame.grid(column=0, row=1, sticky="EW", pady=5)
        self.imagesFrame.grid_columnconfigure(1, weight=1)
        setRow = 0
        for path in self.configuration['images'].split('|'):
            pathLabel = self.guiStrings['images'].label + ' #' + str(setRow + 1)
            label = ttk.Label(self.imagesFrame, text=pathLabel)
            wckToolTips.register(label, self.guiStrings['images'].help)
            label.grid(column=0, row=setRow, padx=5, sticky="W")
            self.guiVars[pathLabel] = Tk.StringVar()
            self.guiVars[pathLabel].set(path.strip())
            entry = ttk.Entry(self.imagesFrame, textvariable=self.guiVars[pathLabel])
            entry.grid(column=1, row=setRow, padx=5, sticky="WE")
            selectImagesPathButton = ttk.Button(self.imagesFrame, text=self.guiStrings['selectImages'].label,
                                               command=lambda feLabel=pathLabel: self.__openFileExplorer(True, feLabel,
                                                                                                         None, feLabel))
            selectImagesPathButton.grid(column=2, row=setRow, padx=5, sticky="WE")
            wckToolTips.register(selectImagesPathButton, self.guiStrings['selectImages'].help)
            setRow = setRow + 1

        ttk.Separator(self.imagesFrame, orient=Tk.HORIZONTAL).grid(column=0, row=setRow, columnspan=3, padx=5, pady=5,
                                                                   sticky="EW")
        setRow = setRow + 1
        imgFormatLabel = ttk.Label(self.imagesFrame, text=self.guiStrings['imgNameFormat'].label)
        wckToolTips.register(imgFormatLabel, self.guiStrings['imgNameFormat'].help)
        imgFormatLabel.grid(column=0, row=setRow, padx=5, sticky=Tk.W)
        self.guiVars['imgNameFormat'] = Tk.StringVar()
        self.guiVars['imgNameFormat'].set(self.configuration['imgNameFormat'])
        # place entry in dict to retrieve later
        imgFormatEntry = ttk.Entry(self.imagesFrame, textvariable=self.guiVars['imgNameFormat'])
        imgFormatEntry.grid(column=1, row=setRow, padx=5, sticky="WE")

    def __drawParametersFrame(self):
        # Parameters frame
        self.parametersFrame = ttk.LabelFrame(self.tabFrame, text="Sorting Parameters", padding=(10, 5))
        self.parametersFrame.grid(column=0, row=2, sticky="EW", pady=5)

        checkButtonsFrame = ttk.Frame(self.parametersFrame)
        checkButtonsFrame.grid(column=0, row=0, columnspan=5, pady=5, sticky="W")
        # nothing else is in this column: it gets the room left so other columns keep their natural width
        self.parametersFrame.grid_columnconfigure(5, weight=1)

        self.guiVars['datOnly'] = Tk.IntVar()
        self.guiVars['datOnly'].set(self.configuration['datOnly'])
        datOnlyCheckButton = ttk.Checkbutton(checkButtonsFrame, text=self.guiStrings['datOnly'].label,
                                            variable=self.guiVars['datOnly'], onvalue=1, offvalue=0,
                                            command=self.__toggleDatOnly)
        wckToolTips.register(datOnlyCheckButton, self.guiStrings['datOnly'].help)
        datOnlyCheckButton.grid(column=0, row=0, padx=(10, 20), sticky="W")

        self.guiVars['dryRun'] = Tk.IntVar()
        self.guiVars['dryRun'].set(self.configuration['dryRun'])
        dryRunCheckButton = ttk.Checkbutton(checkButtonsFrame, text=self.guiStrings['dryRun'].label,
                                           variable=self.guiVars['dryRun'], onvalue=1, offvalue=0)
        wckToolTips.register(dryRunCheckButton, self.guiStrings['dryRun'].help)
        dryRunCheckButton.grid(column=1, row=0, padx=20, sticky="W")
        self.dryRunCheckButton = dryRunCheckButton
        self.dryRunBeforeDatOnly = self.configuration['dryRun']
        self.__toggleDatOnly(init=True)

        self.guiVars['genreSubFolders'] = Tk.IntVar()
        self.guiVars['genreSubFolders'].set(self.configuration['genreSubFolders'])
        useGenreSubFolderCheckButton = ttk.Checkbutton(checkButtonsFrame,
                                                      text=self.guiStrings['genreSubFolders'].label,
                                                      variable=self.guiVars['genreSubFolders'], onvalue=1, offvalue=0)
        wckToolTips.register(useGenreSubFolderCheckButton, self.guiStrings['genreSubFolders'].help)
        useGenreSubFolderCheckButton.grid(column=2, row=0, padx=20, sticky="W")

        self.guiVars['useImages'] = Tk.IntVar()
        self.guiVars['useImages'].set(self.configuration['useImages'])
        useImagesCheckButton = ttk.Checkbutton(checkButtonsFrame, text=self.guiStrings['useImages'].label,
                                              variable=self.guiVars['useImages'], onvalue=1, offvalue=0)
        wckToolTips.register(useImagesCheckButton, self.guiStrings['useImages'].help)
        useImagesCheckButton.grid(column=3, row=0, padx=20, sticky="W")

        self.guiVars['excludeCHDGames'] = Tk.IntVar()
        self.guiVars['excludeCHDGames'].set(self.configuration['excludeCHDGames'])
        excludeCHDGamesCheckButton = ttk.Checkbutton(checkButtonsFrame, text=self.guiStrings['excludeCHDGames'].label,
                                              variable=self.guiVars['excludeCHDGames'], onvalue=1, offvalue=0)
        wckToolTips.register(excludeCHDGamesCheckButton, self.guiStrings['excludeCHDGames'].help)
        excludeCHDGamesCheckButton.grid(column=4, row=0, padx=20, sticky="W")

        ttk.Separator(self.parametersFrame, orient=Tk.HORIZONTAL).grid(column=0, row=1, columnspan=6, padx=5, pady=5,
                                                                       sticky="EW")
        # own frame so that the combobox is right next to its label
        keepLevelFrame = ttk.Frame(self.parametersFrame)
        keepLevelFrame.grid(column=0, row=2, columnspan=2, sticky="W")
        keepLevelLabel = ttk.Label(keepLevelFrame, text=self.guiStrings['keepLevel'].label)
        wckToolTips.register(keepLevelLabel, self.guiStrings['keepLevel'].help)
        keepLevelLabel.grid(column=0, row=0, sticky="W")
        self.guiVars['keepLevel'] = Tk.StringVar()
        self.guiVars['keepLevel'].set(Sorter.getStatus(int(self.configuration['keepLevel'])))
        keepLevelComboBox = ttk.Combobox(keepLevelFrame, state="readonly", textvariable=self.guiVars['keepLevel'])
        keepLevelComboBox.grid(column=1, row=0, sticky="W", pady=5, padx=5)
        keepLevelComboBox['values'] = ('WORKING', 'MOSTLY WORKING', 'BADLY WORKING', 'NON WORKING')
        self.guiVars['keepNotTested'] = Tk.IntVar()
        self.guiVars['keepNotTested'].set(self.configuration['keepNotTested'])
        keepNotTestedCheckButton = ttk.Checkbutton(self.parametersFrame, text=self.guiStrings['keepNotTested'].label,
                                                  variable=self.guiVars['keepNotTested'], onvalue=1, offvalue=0)
        wckToolTips.register(keepNotTestedCheckButton, self.guiStrings['keepNotTested'].help)
        keepNotTestedCheckButton.grid(column=2, row=2, padx=20, sticky="W")
        ttk.Separator(self.parametersFrame, orient=Tk.HORIZONTAL).grid(column=0, row=3, columnspan=6, padx=5, pady=5,
                                                                       sticky="EW")
        # exclusion type, prefered set and genre prefered sets switch on one line
        exclusionTypeLabel = ttk.Label(self.parametersFrame, text=self.guiStrings['exclusionType'].label)
        wckToolTips.register(exclusionTypeLabel,
                             self.guiStrings['exclusionType'].help.replace('#n', '\n').replace(',', '\n'))
        exclusionTypeLabel.grid(column=0, row=4, sticky="W")
        self.guiVars['exclusionType'] = Tk.StringVar()
        self.guiVars['exclusionType'].set(self.configuration['exclusionType'])
        exclusionTypeComboBox = ttk.Combobox(self.parametersFrame, state="readonly",
                                             textvariable=self.guiVars['exclusionType'])
        exclusionTypeComboBox.grid(column=1, row=4, sticky="W", pady=5, padx=5)
        exclusionTypeComboBox['values'] = ('STRICT', 'EQUAL', 'NONE')
        exclusionTypeComboBox.bind('<<ComboboxSelected>>', self.__changeExclusionType)
        # own frame: its columns are sized by their content and not by the checkboxes row above
        preferedSetFrame = ttk.Frame(self.parametersFrame)
        preferedSetFrame.grid(column=2, row=4, columnspan=4, padx=20, sticky="W")
        self.preferedSetLabel = ttk.Label(preferedSetFrame, text=self.guiStrings['preferedSet'].label)
        wckToolTips.register(self.preferedSetLabel, self.guiStrings['preferedSet'].help)
        self.preferedSetLabel.grid(column=0, row=0, sticky="W")
        self.guiVars['preferedSet'] = Tk.StringVar()
        self.guiVars['preferedSet'].set(self.configuration['preferedSet'])
        self.preferedSetComboBox = ttk.Combobox(preferedSetFrame, state="readonly",
                                                textvariable=self.guiVars['preferedSet'])
        self.preferedSetComboBox.grid(column=1, row=0, sticky="W", pady=5, padx=5)
        self.preferedSetValues = Sorter.setKeys.copy()
        self.preferedSetComboBox['values'] = self.preferedSetValues
        self.guiVars['usePreferedSetForGenre'] = Tk.IntVar()
        self.guiVars['usePreferedSetForGenre'].set(self.configuration['usePreferedSetForGenre'])
        self.usePreferedSetForGenreCheckButton = ttk.Checkbutton(preferedSetFrame,
                                                                text=self.guiStrings['usePreferedSetForGenre'].label,
                                                                variable=self.guiVars['usePreferedSetForGenre'],
                                                                onvalue=1, offvalue=0,
                                                                command=self.__changeUsePreferedSetForGenre)
        wckToolTips.register(self.usePreferedSetForGenreCheckButton, self.guiStrings['usePreferedSetForGenre'].help)
        self.usePreferedSetForGenreCheckButton.grid(column=2, row=0, padx=20, sticky="W")
        self.preferedSetForGenreFrame = ttk.Frame(self.parametersFrame)
        self.preferedSetForGenreFrame.grid(column=0, row=5, columnspan=6, sticky="EW")
        # genre prefered sets, GENRES_PER_ROW groups of label and combobox per row
        for index, genre in enumerate(self.GENRES):
            key = genre + 'PreferedSet'
            column = 2 * (index % self.GENRES_PER_ROW)
            row = index // self.GENRES_PER_ROW
            label = ttk.Label(self.preferedSetForGenreFrame, text=self.guiStrings[key].label)
            wckToolTips.register(label, self.guiStrings[key].help)
            label.grid(column=column, row=row, sticky="W", pady=5)
            self.guiVars[key] = Tk.StringVar()
            self.guiVars[key].set(self.configuration[key])
            comboBox = ttk.Combobox(self.preferedSetForGenreFrame, state="readonly", width=self.GENRE_COMBOBOX_WIDTH,
                                    textvariable=self.guiVars[key], values=self.preferedSetValues)
            comboBox.grid(column=column + 1, row=row, sticky="W", pady=5, padx=(5, 10))
            self.genreWidgets.append((label, comboBox))
        self.__showHide()

    def __toggleDatOnly(self, init=False):
        """Dry run is implied by dat only: ticked and disabled, its previous value is back when dat only is not"""
        if self.guiVars['datOnly'].get() == 1:
            if not init:
                self.dryRunBeforeDatOnly = self.guiVars['dryRun'].get()
            self.guiVars['dryRun'].set(1)
            self.dryRunCheckButton.state(['disabled'])
        else:
            if not init:
                self.guiVars['dryRun'].set(self.dryRunBeforeDatOnly)
            self.dryRunCheckButton.state(['!disabled'])

    def __changeExclusionType(self, event):
        self.__showHide()

    def __changeUsePreferedSetForGenre(self):
        self.__showHide()

    def __showHide(self):
        strict = self.guiVars['exclusionType'].get() == 'STRICT'
        genres = strict and self.guiVars['usePreferedSetForGenre'].get() == 1
        self.preferedSetLabel['state'] = 'normal' if strict else 'disabled'
        self.preferedSetComboBox['state'] = 'readonly' if strict else 'disabled'
        self.usePreferedSetForGenreCheckButton['state'] = 'normal' if strict else 'disabled'
        for label, comboBox in self.genreWidgets:
            label['state'] = 'normal' if genres else 'disabled'
            comboBox['state'] = 'readonly' if genres else 'disabled'

    def __drawButtonsFrame(self):
        self.buttonsFrame = ttk.Frame(self.tabFrame, padding=(10, 0))
        self.buttonsFrame.grid(column=0, row=3, sticky="EW", pady=5)

        # empty column takes all the room left, buttons are on the right of the window
        self.buttonsFrame.grid_columnconfigure(0, weight=1)
        emptyFrame = ttk.Frame(self.buttonsFrame, width=700, padding=(10, 0))
        emptyFrame.grid(column=0, row=0, columnspan=3, sticky="EW", pady=5)
        self.verifyButton = ttk.Button(self.buttonsFrame, text=self.guiStrings['verify'].label, command=self.__clickVerify)
        wckToolTips.register(self.verifyButton, self.guiStrings['verify'].help)
        self.verifyButton.grid(column=3, row=0, sticky="E", padx=3)
        self.saveButton = ttk.Button(self.buttonsFrame, text=self.guiStrings['save'].label, command=self.__clickSave)
        wckToolTips.register(self.saveButton, self.guiStrings['save'].help)
        self.saveButton.grid(column=4, row=0, sticky="E", padx=3)
        self.proceedButton = ttk.Button(self.buttonsFrame, text=self.guiStrings['proceed'].label,
                                       command=self.__clickProceed)
        wckToolTips.register(self.proceedButton, self.guiStrings['proceed'].help)
        self.proceedButton.grid(column=5, row=0, sticky="E", padx=3)

    def __clickSave(self):
        self.logger.log('\n<---------- Saving retroarch configuration ----------->')
        self.__saveConfFile()
        self.__saveConfInMem()

    def __saveConfFile(self):
        confBackupFilePath = os.path.join(self.scriptDir, utils.confDir,
                                          utils.getConfBakFilename('retroarch'))
        if os.path.exists(confBackupFilePath):
            os.remove(confBackupFilePath)
        confFilePath = os.path.join(self.scriptDir, utils.confDir, utils.getConfFilename('retroarch'))
        os.makedirs(os.path.join(self.scriptDir, utils.confDir), exist_ok=True)
        if os.path.exists(confFilePath):
            shutil.copy2(confFilePath, confBackupFilePath)
        confFile = open(os.path.join(self.scriptDir, utils.confDir, utils.getConfFilename('retroarch')), "w",
                        encoding="utf-8")
        listKeys = sorted(self.guiStrings.values(), key=attrgetter('order'))
        for key in listKeys:
            if key.id not in ['verify', 'save', 'proceed', 'confirm', 'selectRomsetDir', 'selectDat',
                              'selectExportDir', 'selectImages', 'selectIni']:
                if key.help:
                    confFile.write('# ' + key.help.replace('#n', '\n# ') + '\n')
                if key.id == 'images':
                    imagesValue = self.guiVars[self.guiStrings['images'].label + ' #1'].get()
                    if self.guiStrings['images'].label + ' #2' in self.guiVars:
                        imagesValue = imagesValue + '|' + self.guiVars[self.guiStrings['images'].label + ' #2'].get()
                    confFile.write(key.id + ' = ' + imagesValue + '\n')
                elif key.id == 'keepLevel':
                    confFile.write(key.id + ' = ' + str(Sorter.getIntStatus(self.guiVars[key.id].get())) + '\n')
                else:
                    if key.id in self.guiVars:
                        confFile.write(key.id + ' = ' + str(self.guiVars[key.id].get()) + '\n')
        confFile.close()
        self.logger.log('    Configuration saved in ' + utils.getConfFilename('retroarch') + ' file')

    def __saveConfInMem(self):
        listKeys = sorted(self.guiStrings.values(), key=attrgetter('order'))
        for key in listKeys:
            if key.id not in ['verify', 'save', 'proceed', 'confirm', 'selectRomsetDir', 'selectDat',
                              'selectExportDir', 'selectImages', 'selectIni']:
                if key.id == 'images':
                    imagesValue = self.guiVars[self.guiStrings['images'].label + ' #1'].get()
                    if self.guiStrings['images'].label + ' #2' in self.guiVars:
                        imagesValue = imagesValue + '|' + self.guiVars[self.guiStrings['images'].label + ' #2'].get()
                    self.configuration['images'] = imagesValue
                elif key.id == 'keepLevel':
                    self.configuration['keepLevel'] = str(Sorter.getIntStatus(self.guiVars[key.id].get()))
                else:
                    if key.id in self.guiVars:
                        self.configuration[key.id] = str(self.guiVars[key.id].get())
        self.logger.log('    Configuration saved in memory')

    def __clickVerify(self):
        self.logger.log('\n<--------- Verify retroarch Parameters --------->')
        error = False
        datOnly = self.guiVars['datOnly'].get() == 1
        # no romset nor images needed in dat only mode
        keys = ['exportDir'] if datOnly else Sorter.setKeys + ['exportDir', 'Images folder #1', 'Images folder #2']
        for key in keys:
            if not os.path.exists(self.guiVars[key].get()):
                error = True
                self.logger.log(key + ' folder does not exist', self.logger.ERROR)
        if not os.path.exists(self.guiVars['iniFile'].get()):
            error = True
            self.logger.log('Roms selection ' + self.guiVars['iniFile'].get() + ' does not exist', self.logger.ERROR)
        if datOnly:
            error = True
            self.logger.log(
                'WARNING: dat only mode is used, only the filtered dats, csv and gamelist files will be generated '
                'from the bundled dats, games are considered present if they are in them', self.logger.WARNING)
        elif self.guiVars['dryRun'].get() == 1:
            error = True
            self.logger.log(
                'WARNING: dryRun mode is used, only csv and gamelist files will be generated, '
                'roms and images will not be copied', self.logger.WARNING)
        if not error:
            self.logger.log('All Good!')

    def __clickProceed(self):
        self.logger.log('\n<--------- Saving retroarch configuration --------->')
        self.__saveConfInMem()
        message = self.guiStrings['confirm'].help.replace('{outputDir}', self.guiVars['exportDir'].get()).replace('#n',
                                                                                                                  '\n')
        result = messagebox.askokcancel(self.guiStrings['confirm'].label, message)
        if result:
            self.verifyButton['state'] = 'disabled'
            self.saveButton['state'] = 'disabled'
            self.proceedButton['state'] = 'disabled'
            self.mummy.disableOtherTabs('retroarch')
            self.logger.log('\n<--------- Starting retroarch Process --------->')
            sorter = Sorter(self.configuration, self.scriptDir, partial(self.postProcess), self.logger)
            _thread.start_new(sorter.process, ())

    def postProcess(self):
        self.verifyButton['state'] = 'normal'
        self.saveButton['state'] = 'normal'
        self.proceedButton['state'] = 'normal'
        self.mummy.disableOtherTabs('retroarch', False)

        # File Explorer for various vars

    def __openFileExplorer(self, openDir, var, fileTypes, label=None):
        if openDir:
            label = self.guiStrings[var].label if var in self.guiStrings else label
            result = filedialog.askdirectory(initialdir=self.guiVars[var].get(),
                                             title="Select your " + label)
        else:
            basedir = os.path.dirname(self.guiVars[var].get())
            initialDir = basedir if os.path.exists(basedir) else self.scriptDir
            fileTypes = list(map(lambda ft: (ft.upper() + ' Files', '*.%s' % ft), fileTypes))
            result = filedialog.askopenfilename(initialdir=initialDir,
                                                title="Select your " + self.guiStrings[var].label,
                                                filetypes=fileTypes)
        if result != '':
            if platform.system() == 'Windows':
                result = result.replace('/', '\\')
            self.mummy.updateConsoleFromQueue()
            self.guiVars[var].set(result)
