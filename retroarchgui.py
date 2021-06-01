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

    def __init__(self, rootFrame, scriptDir, logger, mummy, hardware):
        self.tabFrame = rootFrame
        self.scriptDir = scriptDir
        self.logger = logger
        self.mummy = mummy
        self.hardware = hardware
        self.configuration = conf.loadConf(
            os.path.join(self.scriptDir, utils.confDir, utils.getConfFilename('retroarch-'+self.hardware)))
        self.logger.log('Loaded ' + utils.getConfFilename('retroarch-'+self.hardware))
        self.guiVars = dict()
        self.guiStrings = utils.loadUIStrings(self.scriptDir, utils.getGuiStringsFilename('retroarch-'+self.hardware))

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
        self.beatEmUpPreferedSetLabel = None
        self.beatEmUpPreferedSetComboBox = None
        self.gunPreferedSetLabel = None
        self.gunPreferedSetComboBox = None
        self.miscPreferedSetLabel = None
        self.miscPreferedSetComboBox = None
        self.platformPreferedSetLabel = None
        self.platformPreferedSetComboBox = None
        self.puzzlePreferedSetLabel = None
        self.puzzlePreferedSetComboBox = None
        self.racePreferedSetLabel = None
        self.racePreferedSetComboBox = None
        self.runNGunPreferedSetLabel = None
        self.runNGunPreferedSetComboBox = None
        self.shootEmUpPreferedSetLabel = None
        self.shootEmUpPreferedSetComboBox = None
        self.sportPreferedSetLabel = None
        self.sportPreferedSetComboBox = None
        self.vsFightingPreferedSetLabel = None
        self.vsFightingPreferedSetComboBox = None
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
        self.romsetFrame = Tk.LabelFrame(self.tabFrame, text="Your Romsets", padx=10, pady=5)
        self.romsetFrame.grid(column=0, row=0, sticky="EW", pady=5)
        self.romsetFrame.grid_columnconfigure(1, weight=1)
        setRow = 0
        for key in Sorter.setKeys[self.hardware]:
            label = Tk.Label(self.romsetFrame, text=self.guiStrings[key].label)
            wckToolTips.register(label, self.guiStrings[key].help)
            label.grid(column=0, row=setRow, padx=5, sticky="W")
            self.guiVars[key] = Tk.StringVar()
            self.guiVars[key].set(self.configuration[key])
            entry = Tk.Entry(self.romsetFrame, textvariable=self.guiVars[key])
            entry.grid(column=1, row=setRow, padx=5, sticky="WE")
            selectRomsetDirButton = Tk.Button(
                self.romsetFrame, text=self.guiStrings['selectRomsetDir'].label,
                command=lambda setKey=key: self.__openFileExplorer(True, setKey, None, self.guiStrings[setKey].label))
            selectRomsetDirButton.grid(column=2, row=setRow, padx=5, sticky="WE")
            wckToolTips.register(selectRomsetDirButton, self.guiStrings['selectRomsetDir'].help)
            setRow = setRow + 1

        ttk.Separator(self.romsetFrame, orient=Tk.HORIZONTAL).grid(column=0, row=setRow, columnspan=3, padx=5, pady=5,
                                                                   sticky="EW")
        setRow = setRow + 1
        outputDirLabel = Tk.Label(self.romsetFrame, text=self.guiStrings['exportDir'].label)
        wckToolTips.register(outputDirLabel, self.guiStrings['exportDir'].help)
        outputDirLabel.grid(column=0, row=setRow, padx=5, sticky=Tk.W)
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
        ttk.Separator(self.parametersFrame, orient=Tk.HORIZONTAL).grid(column=0, row=1, columnspan=5, padx=5, pady=5,
                                                                       sticky="EW")
        keepLevelLabel = Tk.Label(self.parametersFrame, text=self.guiStrings['keepLevel'].label)
        wckToolTips.register(keepLevelLabel, self.guiStrings['keepLevel'].help)
        keepLevelLabel.grid(column=0, row=2, sticky="W")
        self.guiVars['keepLevel'] = Tk.StringVar()
        self.guiVars['keepLevel'].set(Sorter.getStatus(int(self.configuration['keepLevel'])))
        keepLevelComboBox = ttk.Combobox(self.parametersFrame, state="readonly", textvariable=self.guiVars['keepLevel'])
        keepLevelComboBox.grid(column=1, row=2, sticky="W", pady=5)
        keepLevelComboBox['values'] = ('WORKING', 'MOSTLY WORKING', 'BADLY WORKING', 'NON WORKING')
        self.guiVars['keepNotTested'] = Tk.IntVar()
        self.guiVars['keepNotTested'].set(self.configuration['keepNotTested'])
        keepNotTestedCheckButton = Tk.Checkbutton(self.parametersFrame, text=self.guiStrings['keepNotTested'].label,
                                                  variable=self.guiVars['keepNotTested'], onvalue=1, offvalue=0)
        wckToolTips.register(keepNotTestedCheckButton, self.guiStrings['keepNotTested'].help)
        keepNotTestedCheckButton.grid(column=2, row=2, sticky="W")
        ttk.Separator(self.parametersFrame, orient=Tk.HORIZONTAL).grid(column=0, row=3, columnspan=5, padx=5, pady=5,
                                                                       sticky="EW")
        exclusionTypeLabel = Tk.Label(self.parametersFrame, text=self.guiStrings['exclusionType'].label)
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
        self.preferedSetLabel = Tk.Label(self.parametersFrame, text=self.guiStrings['preferedSet'].label)
        wckToolTips.register(self.preferedSetLabel, self.guiStrings['preferedSet'].help)
        self.preferedSetLabel.grid(column=0, row=5, sticky="W", pady=5)
        self.guiVars['preferedSet'] = Tk.StringVar()
        self.guiVars['preferedSet'].set(self.configuration['preferedSet'])
        self.preferedSetComboBox = ttk.Combobox(self.parametersFrame, state="readonly",
                                                textvariable=self.guiVars['preferedSet'])
        self.preferedSetComboBox.grid(column=1, row=5, sticky="W", pady=5, padx=5)
        self.preferedSetValues = Sorter.setKeys[self.hardware].copy()
        self.preferedSetComboBox['values'] = self.preferedSetValues
        self.guiVars['usePreferedSetForGenre'] = Tk.IntVar()
        self.guiVars['usePreferedSetForGenre'].set(self.configuration['usePreferedSetForGenre'])
        self.usePreferedSetForGenreCheckButton = Tk.Checkbutton(self.parametersFrame,
                                                                text=self.guiStrings['usePreferedSetForGenre'].label,
                                                                variable=self.guiVars['usePreferedSetForGenre'],
                                                                onvalue=1, offvalue=0,
                                                                command=self.__changeUsePreferedSetForGenre)
        wckToolTips.register(self.usePreferedSetForGenreCheckButton, self.guiStrings['usePreferedSetForGenre'].help)
        self.usePreferedSetForGenreCheckButton.grid(column=2, row=5, sticky="W")
        self.preferedSetForGenreFrame = Tk.Frame(self.parametersFrame)
        self.preferedSetForGenreFrame.grid(column=0, row=6, columnspan=5, sticky="EW")
        self.preferedSetForGenreFrame.grid_columnconfigure(2, weight=1)
        self.preferedSetForGenreFrame.grid_columnconfigure(5, weight=1)
        # usePreferedSetForGenre comboboxes
        self.beatEmUpPreferedSetLabel = Tk.Label(self.preferedSetForGenreFrame,
                                                 text=self.guiStrings['BeatEmUpPreferedSet'].label)
        wckToolTips.register(self.beatEmUpPreferedSetLabel, self.guiStrings['BeatEmUpPreferedSet'].help)
        self.beatEmUpPreferedSetLabel.grid(column=0, row=0, sticky="W", pady=5)
        self.guiVars['BeatEmUpPreferedSet'] = Tk.StringVar()
        self.guiVars['BeatEmUpPreferedSet'].set(self.configuration['BeatEmUpPreferedSet'])
        self.beatEmUpPreferedSetComboBox = ttk.Combobox(self.preferedSetForGenreFrame, state="readonly",
                                                        textvariable=self.guiVars['BeatEmUpPreferedSet'])
        self.beatEmUpPreferedSetComboBox.grid(column=1, row=0, sticky="W", pady=5, padx=5)
        self.beatEmUpPreferedSetComboBox['values'] = self.preferedSetValues
        self.gunPreferedSetLabel = Tk.Label(self.preferedSetForGenreFrame, text=self.guiStrings['GunPreferedSet'].label)
        wckToolTips.register(self.gunPreferedSetLabel, self.guiStrings['GunPreferedSet'].help)
        self.gunPreferedSetLabel.grid(column=3, row=0, sticky="W", pady=5)
        self.guiVars['GunPreferedSet'] = Tk.StringVar()
        self.guiVars['GunPreferedSet'].set(self.configuration['GunPreferedSet'])
        self.gunPreferedSetComboBox = ttk.Combobox(self.preferedSetForGenreFrame, state="readonly",
                                                   textvariable=self.guiVars['GunPreferedSet'])
        self.gunPreferedSetComboBox.grid(column=4, row=0, sticky="W", pady=5, padx=5)
        self.gunPreferedSetComboBox['values'] = self.preferedSetValues
        self.miscPreferedSetLabel = Tk.Label(self.preferedSetForGenreFrame,
                                             text=self.guiStrings['MiscPreferedSet'].label)
        wckToolTips.register(self.miscPreferedSetLabel, self.guiStrings['MiscPreferedSet'].help)
        self.miscPreferedSetLabel.grid(column=6, row=0, sticky="W", pady=5)
        self.guiVars['MiscPreferedSet'] = Tk.StringVar()
        self.guiVars['MiscPreferedSet'].set(self.configuration['MiscPreferedSet'])
        self.miscPreferedSetComboBox = ttk.Combobox(self.preferedSetForGenreFrame, state="readonly",
                                                    textvariable=self.guiVars['MiscPreferedSet'])
        self.miscPreferedSetComboBox.grid(column=7, row=0, sticky="W", pady=5, padx=5)
        self.miscPreferedSetComboBox['values'] = self.preferedSetValues
        self.platformPreferedSetLabel = Tk.Label(self.preferedSetForGenreFrame,
                                                 text=self.guiStrings['PlatformPreferedSet'].label)
        wckToolTips.register(self.platformPreferedSetLabel, self.guiStrings['PlatformPreferedSet'].help)
        self.platformPreferedSetLabel.grid(column=0, row=1, sticky="W", pady=5)
        self.guiVars['PlatformPreferedSet'] = Tk.StringVar()
        self.guiVars['PlatformPreferedSet'].set(self.configuration['PlatformPreferedSet'])
        self.platformPreferedSetComboBox = ttk.Combobox(self.preferedSetForGenreFrame, state="readonly",
                                                        textvariable=self.guiVars['PlatformPreferedSet'])
        self.platformPreferedSetComboBox.grid(column=1, row=1, sticky="W", pady=5, padx=5)
        self.platformPreferedSetComboBox['values'] = self.preferedSetValues
        self.puzzlePreferedSetLabel = Tk.Label(self.preferedSetForGenreFrame,
                                               text=self.guiStrings['PuzzlePreferedSet'].label)
        wckToolTips.register(self.puzzlePreferedSetLabel, self.guiStrings['PuzzlePreferedSet'].help)
        self.puzzlePreferedSetLabel.grid(column=3, row=1, sticky="W", pady=5)
        self.guiVars['PuzzlePreferedSet'] = Tk.StringVar()
        self.guiVars['PuzzlePreferedSet'].set(self.configuration['PuzzlePreferedSet'])
        self.puzzlePreferedSetComboBox = ttk.Combobox(self.preferedSetForGenreFrame, state="readonly",
                                                      textvariable=self.guiVars['PuzzlePreferedSet'])
        self.puzzlePreferedSetComboBox.grid(column=4, row=1, sticky="W", pady=5, padx=5)
        self.puzzlePreferedSetComboBox['values'] = self.preferedSetValues
        self.racePreferedSetLabel = Tk.Label(self.preferedSetForGenreFrame,
                                             text=self.guiStrings['RacePreferedSet'].label)
        wckToolTips.register(self.racePreferedSetLabel, self.guiStrings['RacePreferedSet'].help)
        self.racePreferedSetLabel.grid(column=6, row=1, sticky="W", pady=5)
        self.guiVars['RacePreferedSet'] = Tk.StringVar()
        self.guiVars['RacePreferedSet'].set(self.configuration['RacePreferedSet'])
        self.racePreferedSetComboBox = ttk.Combobox(self.preferedSetForGenreFrame, state="readonly",
                                                    textvariable=self.guiVars['RacePreferedSet'])
        self.racePreferedSetComboBox.grid(column=7, row=1, sticky="W", pady=5, padx=5)
        self.racePreferedSetComboBox['values'] = self.preferedSetValues
        self.runNGunPreferedSetLabel = Tk.Label(self.preferedSetForGenreFrame,
                                                text=self.guiStrings['RunNGunPreferedSet'].label)
        wckToolTips.register(self.runNGunPreferedSetLabel, self.guiStrings['RunNGunPreferedSet'].help)
        self.runNGunPreferedSetLabel.grid(column=0, row=2, sticky="W", pady=5)
        self.guiVars['RunNGunPreferedSet'] = Tk.StringVar()
        self.guiVars['RunNGunPreferedSet'].set(self.configuration['RunNGunPreferedSet'])
        self.runNGunPreferedSetComboBox = ttk.Combobox(self.preferedSetForGenreFrame, state="readonly",
                                                       textvariable=self.guiVars['RunNGunPreferedSet'])
        self.runNGunPreferedSetComboBox.grid(column=1, row=2, sticky="W", pady=5, padx=5)
        self.runNGunPreferedSetComboBox['values'] = self.preferedSetValues
        self.shootEmUpPreferedSetLabel = Tk.Label(self.preferedSetForGenreFrame,
                                                  text=self.guiStrings['ShootEmUpPreferedSet'].label)
        wckToolTips.register(self.shootEmUpPreferedSetLabel, self.guiStrings['ShootEmUpPreferedSet'].help)
        self.shootEmUpPreferedSetLabel.grid(column=3, row=2, sticky="W", pady=5)
        self.guiVars['ShootEmUpPreferedSet'] = Tk.StringVar()
        self.guiVars['ShootEmUpPreferedSet'].set(self.configuration['ShootEmUpPreferedSet'])
        self.shootEmUpPreferedSetComboBox = ttk.Combobox(self.preferedSetForGenreFrame, state="readonly",
                                                         textvariable=self.guiVars['ShootEmUpPreferedSet'])
        self.shootEmUpPreferedSetComboBox.grid(column=4, row=2, sticky="W", pady=5, padx=5)
        self.shootEmUpPreferedSetComboBox['values'] = self.preferedSetValues
        self.sportPreferedSetLabel = Tk.Label(self.preferedSetForGenreFrame,
                                              text=self.guiStrings['SportPreferedSet'].label)
        wckToolTips.register(self.sportPreferedSetLabel, self.guiStrings['SportPreferedSet'].help)
        self.sportPreferedSetLabel.grid(column=6, row=2, sticky="W", pady=5)
        self.guiVars['SportPreferedSet'] = Tk.StringVar()
        self.guiVars['SportPreferedSet'].set(self.configuration['SportPreferedSet'])
        self.sportPreferedSetComboBox = ttk.Combobox(self.preferedSetForGenreFrame, state="readonly",
                                                     textvariable=self.guiVars['SportPreferedSet'])
        self.sportPreferedSetComboBox.grid(column=7, row=2, sticky="W", pady=5, padx=5)
        self.sportPreferedSetComboBox['values'] = self.preferedSetValues
        self.vsFightingPreferedSetLabel = Tk.Label(self.preferedSetForGenreFrame,
                                                   text=self.guiStrings['VsFightingPreferedSet'].label)
        wckToolTips.register(self.vsFightingPreferedSetLabel, self.guiStrings['VsFightingPreferedSet'].help)
        self.vsFightingPreferedSetLabel.grid(column=0, row=3, sticky="W", pady=5)
        self.guiVars['VsFightingPreferedSet'] = Tk.StringVar()
        self.guiVars['VsFightingPreferedSet'].set(self.configuration['VsFightingPreferedSet'])
        self.vsFightingPreferedSetComboBox = ttk.Combobox(self.preferedSetForGenreFrame, state="readonly",
                                                          textvariable=self.guiVars['VsFightingPreferedSet'])
        self.vsFightingPreferedSetComboBox.grid(column=1, row=3, sticky="W", pady=5, padx=5)
        self.vsFightingPreferedSetComboBox['values'] = self.preferedSetValues
        self.__showHide()

    def __changeExclusionType(self, event):
        self.__showHide()

    def __changeUsePreferedSetForGenre(self):
        self.__showHide()

    def __showHide(self):
        if self.guiVars['exclusionType'].get() == 'STRICT':
            self.preferedSetLabel['state'] = 'normal'
            self.preferedSetComboBox['state'] = 'readonly'
            self.usePreferedSetForGenreCheckButton['state'] = 'normal'
            if self.guiVars['usePreferedSetForGenre'].get() == 1:
                self.beatEmUpPreferedSetLabel['state'] = 'normal'
                self.beatEmUpPreferedSetComboBox['state'] = 'readonly'
                self.gunPreferedSetLabel['state'] = 'normal'
                self.gunPreferedSetComboBox['state'] = 'readonly'
                self.miscPreferedSetLabel['state'] = 'normal'
                self.miscPreferedSetComboBox['state'] = 'readonly'
                self.platformPreferedSetLabel['state'] = 'normal'
                self.miscPreferedSetComboBox['state'] = 'readonly'
                self.platformPreferedSetLabel['state'] = 'normal'
                self.platformPreferedSetComboBox['state'] = 'readonly'
                self.puzzlePreferedSetLabel['state'] = 'normal'
                self.puzzlePreferedSetComboBox['state'] = 'readonly'
                self.racePreferedSetLabel['state'] = 'normal'
                self.racePreferedSetComboBox['state'] = 'readonly'
                self.runNGunPreferedSetLabel['state'] = 'normal'
                self.runNGunPreferedSetComboBox['state'] = 'readonly'
                self.shootEmUpPreferedSetLabel['state'] = 'normal'
                self.shootEmUpPreferedSetComboBox['state'] = 'readonly'
                self.sportPreferedSetLabel['state'] = 'normal'
                self.sportPreferedSetComboBox['state'] = 'readonly'
                self.vsFightingPreferedSetLabel['state'] = 'normal'
                self.vsFightingPreferedSetComboBox['state'] = 'readonly'
            else:
                self.beatEmUpPreferedSetLabel['state'] = 'disabled'
                self.beatEmUpPreferedSetComboBox['state'] = 'disabled'
                self.gunPreferedSetLabel['state'] = 'disabled'
                self.gunPreferedSetComboBox['state'] = 'disabled'
                self.miscPreferedSetLabel['state'] = 'disabled'
                self.miscPreferedSetComboBox['state'] = 'disabled'
                self.platformPreferedSetLabel['state'] = 'disabled'
                self.miscPreferedSetComboBox['state'] = 'disabled'
                self.platformPreferedSetLabel['state'] = 'disabled'
                self.platformPreferedSetComboBox['state'] = 'disabled'
                self.puzzlePreferedSetLabel['state'] = 'disabled'
                self.puzzlePreferedSetComboBox['state'] = 'disabled'
                self.racePreferedSetLabel['state'] = 'disabled'
                self.racePreferedSetComboBox['state'] = 'disabled'
                self.runNGunPreferedSetLabel['state'] = 'disabled'
                self.runNGunPreferedSetComboBox['state'] = 'disabled'
                self.shootEmUpPreferedSetLabel['state'] = 'disabled'
                self.shootEmUpPreferedSetComboBox['state'] = 'disabled'
                self.sportPreferedSetLabel['state'] = 'disabled'
                self.sportPreferedSetComboBox['state'] = 'disabled'
                self.vsFightingPreferedSetLabel['state'] = 'disabled'
                self.vsFightingPreferedSetComboBox['state'] = 'disabled'
        else:
            self.preferedSetLabel['state'] = 'disabled'
            self.preferedSetComboBox['state'] = 'disabled'
            self.usePreferedSetForGenreCheckButton['state'] = 'disabled'
            self.beatEmUpPreferedSetLabel['state'] = 'disabled'
            self.beatEmUpPreferedSetComboBox['state'] = 'disabled'
            self.gunPreferedSetLabel['state'] = 'disabled'
            self.gunPreferedSetComboBox['state'] = 'disabled'
            self.miscPreferedSetLabel['state'] = 'disabled'
            self.miscPreferedSetComboBox['state'] = 'disabled'
            self.platformPreferedSetLabel['state'] = 'disabled'
            self.miscPreferedSetComboBox['state'] = 'disabled'
            self.platformPreferedSetLabel['state'] = 'disabled'
            self.platformPreferedSetComboBox['state'] = 'disabled'
            self.puzzlePreferedSetLabel['state'] = 'disabled'
            self.puzzlePreferedSetComboBox['state'] = 'disabled'
            self.racePreferedSetLabel['state'] = 'disabled'
            self.racePreferedSetComboBox['state'] = 'disabled'
            self.runNGunPreferedSetLabel['state'] = 'disabled'
            self.runNGunPreferedSetComboBox['state'] = 'disabled'
            self.shootEmUpPreferedSetLabel['state'] = 'disabled'
            self.shootEmUpPreferedSetComboBox['state'] = 'disabled'
            self.sportPreferedSetLabel['state'] = 'disabled'
            self.sportPreferedSetComboBox['state'] = 'disabled'
            self.vsFightingPreferedSetLabel['state'] = 'disabled'
            self.vsFightingPreferedSetComboBox['state'] = 'disabled'

    def __drawButtonsFrame(self):
        self.buttonsFrame = Tk.Frame(self.tabFrame, padx=10)
        self.buttonsFrame.grid(column=0, row=3, sticky="EW", pady=5)

        emptyFrame = Tk.Frame(self.buttonsFrame, width=700, padx=10)
        emptyFrame.grid(column=0, row=0, columnspan=3, sticky="EW", pady=5)
        self.verifyButton = Tk.Button(self.buttonsFrame, text=self.guiStrings['verify'].label, command=self.__clickVerify)
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
        self.logger.log('\n<---------- Saving retroarch-%s configuration ----------->' % self.hardware)
        self.__saveConfFile()
        self.__saveConfInMem()

    def __saveConfFile(self):
        confBackupFilePath = os.path.join(self.scriptDir, utils.confDir,
                                          utils.getConfBakFilename('retroarch-'+self.hardware))
        if os.path.exists(confBackupFilePath):
            os.remove(confBackupFilePath)
        shutil.copy2(os.path.join(self.scriptDir, utils.confDir, utils.getConfFilename('retroarch-'+self.hardware)),
                     os.path.join(self.scriptDir, utils.confDir, utils.getConfBakFilename('retroarch-'+self.hardware)))
        confFile = open(os.path.join(self.scriptDir, utils.confDir, utils.getConfFilename('retroarch-'+self.hardware)), "w",
                        encoding="utf-8")
        listKeys = sorted(self.guiStrings.values(), key=attrgetter('order'))
        for key in listKeys:
            if key.id not in ['verify', 'save', 'proceed', 'confirm', 'selectRomsetDir', 'selectDat',
                              'selectExportDir', 'selectImages']:
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
        self.logger.log('    Configuration saved in ' + utils.getConfFilename('retroarch-'+self.hardware) + ' file')

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
                elif key.id == 'keepLevel':
                    self.configuration['keepLevel'] = str(Sorter.getIntStatus(self.guiVars[key.id].get()))
                else:
                    if key.id in self.guiVars:
                        self.configuration[key.id] = str(self.guiVars[key.id].get())
        self.logger.log('    Configuration saved in memory')

    def __clickVerify(self):
        self.logger.log('\n<--------- Verify retroarch Parameters --------->')
        error = False
        for key in ['exportDir', 'fbneo', 'mame2010', 'mame2003', 'mame2003plus', 'Images folder #1',
                    'Images folder #2']:
            if not os.path.exists(self.guiVars[key].get()):
                error = True
                self.logger.log(key + ' folder does not exist', self.logger.ERROR)
        if self.guiVars['dryRun'].get() == 1:
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
            self.mummy.disableOtherTabs('retroarch', self.hardware)
            self.logger.log('\n<--------- Starting retroarch Process --------->')
            sorter = Sorter(self.configuration, self.scriptDir, partial(self.postProcess), self.logger, self.hardware)
            _thread.start_new(sorter.process, ())

    def postProcess(self):
        self.verifyButton['state'] = 'normal'
        self.saveButton['state'] = 'normal'
        self.proceedButton['state'] = 'normal'
        self.mummy.disableOtherTabs('retroarch', self.hardware, False)

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
