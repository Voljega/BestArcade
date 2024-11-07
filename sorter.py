import xml.etree.ElementTree as etree
import os.path
import shutil
import gamelist
import utils
import fav
import test
import dat
import properties

class Sorter:
    setKeys = {'pi3': ['fbneo', 'mame2003', 'mame2003plus', 'mame2010'], 'n2': ['fbneo', 'mame'], 'n100': ['fbneo', 'mame']}
    bigSetFile = r"custom.ini"

    def __init__(self, configuration, scriptDir, postProcess, logger, hardware):
        self.configuration = configuration
        self.scriptDir = scriptDir
        self.bioses = []
        self.logger = logger
        self.hardware = hardware
        self.postProcess = postProcess

        # Init class vars
        self.usingSystems = None
        self.favorites = None
        self.allTests = None
        self.dats = None

    def process(self):
        self.__prepare()
        # create bestarcade romsets
        self.logger.log('\n<--------- Create Sets --------->')
        self.__createSets(self.allTests, self.dats)
        self.logger.log("\n<--------- Detecting errors ----------->")
        if not self.configuration['exclusionType'] == 'STRICT':
            self.__checkErrors(self.allTests, self.configuration['keepLevel'])
        self.logger.log('\n<--------- Process finished ----------->')
        self.postProcess()

    def __prepare(self):
        self.usingSystems = self.__useSystems(self.configuration)
        # create favorites containing fav games
        self.logger.log('\n<--------- Load Favorites Ini Files --------->')
        self.favorites = fav.loadFavs(self.scriptDir, Sorter.bigSetFile, self.logger)
        # parse dat files
        self.logger.log('\n<--------- Load FBNeo & Mame Dats --------->')
        datsDict = dict(zip(self.setKeys[self.hardware],
                            list(map(lambda key: key + '.dat', self.setKeys[self.hardware]))))
        self.dats = dat.parseDats(self.scriptDir, utils.dataDir, datsDict, self.usingSystems, self.logger)
        # parse test files
        self.logger.log('\n<--------- Load Tests Files --------->')
        self.allTests = test.loadTests(Sorter.setKeys[self.hardware],
                                       os.path.join(self.scriptDir, utils.dataDir, self.hardware),
                                       self.usingSystems, self.logger)
        self.logger.log('\n<--------- Load Property File --------->')
        self.properties = properties.loadProperties(os.path.join(self.scriptDir, utils.dataDir, 'custom.properties'))

    def __useSystems(self, configuration):
        systems = []
        for setKey in self.setKeys[self.hardware]:
            systems.append(setKey) if os.path.exists(configuration[setKey]) else None
        self.logger.logList('Using systems', systems)
        return systems

    @staticmethod
    def __computeScore(setKey, setDir, game, test):
        # always return -2 if file doesn't exist in set
        if not os.path.exists(os.path.join(setDir, game + ".zip")):
            return -2
        score = test[setKey].status if (test is not None and setKey in test) else -2
        # if file exists in set but not in test, should return -1
        if score == -2 and os.path.exists(os.path.join(setDir, game + ".zip")):
            score = -1

        return score

    def __isPreferedSetForGenre(self, genre, keySet):
        return self.configuration[genre + 'PreferedSet'] == keySet

    def __keepSet(self, keepNotTested, usePreferedSetForGenre, exclusionType, keepLevel, scores, key, genre, keep):
        maxScore = max(scores.values())
        if keepNotTested and scores[key] == -1:
            return True
        elif exclusionType == 'NONE':
            return scores[key] >= keepLevel
        elif exclusionType == 'EQUAL':
            if scores[key] == maxScore:
                return scores[key] >= keepLevel
        elif exclusionType == 'STRICT':
            genreTest = genre.replace('[', '')
            genreTest = genreTest.replace(']', '')
            if usePreferedSetForGenre and genreTest + 'PreferedSet' in self.configuration:  # check not empty
                if self.__isPreferedSetForGenre(genreTest, key):
                    return scores[key] >= keepLevel
                else:
                    return False
            if scores[key] == maxScore:
                if key == self.configuration['preferedSet']:
                    return scores[key] >= keepLevel
                elif len(keep) == 0:  # check not already in keep
                    return scores[key] >= keepLevel

    @staticmethod
    def getStatus(status):
        if status == -1:
            return 'UNTESTED'
        elif status == 0:
            return 'NON WORKING'
        elif status == 1:
            return 'BADLY WORKING'
        elif status == 2:
            return 'MOSTLY WORKING'
        elif status == 3:
            return 'WORKING'
        else:
            return 'UNTESTED &amp; FRESHLY ADDED'

    @staticmethod
    def getIntStatus(status):
        if status == 'UNTESTED':
            return -1
        elif status == 'NON WORKING':
            return 0
        elif status == 'BADLY WORKING':
            return 1
        elif status == 'MOSTLY WORKING':
            return 2
        elif status == 'WORKING':
            return 3
        else:
            return -1

    def __createSets(self, allTests, dats):

        self.logger.log('Creating or cleaning output directory ' + self.configuration['exportDir'])
        if os.path.exists(self.configuration['exportDir']):
            for file in os.listdir(os.path.join(self.configuration['exportDir'])):
                fullPath = os.path.join(self.configuration['exportDir'], file)
                shutil.rmtree(fullPath) if os.path.isdir(fullPath) else os.remove(fullPath)
        else:
            os.makedirs(self.configuration['exportDir'])

        notInAnySet = []
        onlyInOneSet = dict()
        dryRun = True if self.configuration['dryRun'] == '1' else False
        useGenreSubFolder = True if self.configuration['genreSubFolders'] == '1' else False
        keepNotTested = True if self.configuration['keepNotTested'] == '1' else False
        keepLevel = int(self.configuration['keepLevel'])
        usePreferedSetForGenre = True if self.configuration['usePreferedSetForGenre'] == '1' else False
        scrapeImages = True if self.configuration['useImages'] == '1' and self.configuration['images'] else False

        scoreSheet = open(os.path.join(self.configuration['exportDir'], "scoreSheet.csv"), "w", encoding="utf-8")
        scoreSheet.write('rom;' + ';'.join(list(map(lambda key: key + 'Score', self.setKeys[self.hardware]))) + '\n')

        CSVs, gamelists, roots = dict(), dict(), dict()
        header = "Status;Genre;Name (mame description);Rom name;Year;Manufacturer;Hardware;Comments;Notes\n"
        for setKey in self.usingSystems:
            # init CSVS
            CSVs[setKey] = open(os.path.join(self.configuration['exportDir'], setKey + ".csv"), "w", encoding="utf-8")
            CSVs[setKey].write(header)
            # init gamelists
            roots[setKey] = etree.Element("datafile")
            roots[setKey].append(dats[setKey + "Header"])
            os.makedirs(os.path.join(self.configuration['exportDir'], setKey))
            os.makedirs(
                os.path.join(self.configuration['exportDir'], setKey, 'downloaded_images')) if scrapeImages else None
            gamelists[setKey] = gamelist.initWrite(os.path.join(self.configuration['exportDir'], setKey))

        # get bioses
        if '[BIOSES]' in self.favorites.keys():
            self.bioses = self.favorites['[BIOSES]']
            del self.favorites['[BIOSES]']

        for genre in self.favorites.keys():
            self.logger.log("Handling genre " + genre)

            if useGenreSubFolder:
                for setKey in self.usingSystems:
                    os.makedirs(os.path.join(self.configuration['exportDir'], setKey, genre))
                    if scrapeImages:
                        gamelist.writeGamelistFolder(gamelists[setKey], genre, genre + '.png')
                        utils.setImageCopy(self.configuration['exportDir'],
                                           os.path.join(self.scriptDir, 'data', 'images'), genre + '.png', setKey,
                                           dryRun)

            # copy bios in each subdirectory
            for bios in self.bioses:
                for setKey in self.usingSystems:
                    setBios = os.path.join(self.configuration[setKey], bios + ".zip")
                    utils.setFileCopy(self.configuration['exportDir'], setBios, genre, bios, setKey, useGenreSubFolder,
                                      dryRun)
                    if os.path.exists(setBios):
                        utils.writeGamelistHiddenEntry(gamelists[setKey], bios, genre, useGenreSubFolder)

            for favs in sorted(self.favorites[genre]):
                # needed to handle multi names games
                if ';' in favs:
                    games = favs.split(';')
                else:
                    games = [favs]

                multiGameFoundInSet = False
                for game in games:
                    # TODO TEMP debug
                    if game == 'pbobblen' or game == 'prosoccr' or game == 'sdtennis':
                        print('ouaich')
                    # TODO END TEMP debug
                    audit = game + " -> "
                    scores = dict()
                    testForGame = allTests[game] if game in allTests else None

                    for setKey in self.setKeys[self.hardware]:
                        scores[setKey] = self.__computeScore(setKey, self.configuration[setKey], game,
                                                             testForGame) if setKey in self.usingSystems else -2

                    audit = audit + " SCORES: " + \
                        " ".join(list(map(lambda key: str(scores[key]), self.setKeys[self.hardware]))) + " ,"
                    scoreSheet.write(game + ';' +
                                     ';'.join(list(map(lambda key: str(scores[key]), self.setKeys[self.hardware])))
                                     + '\n')

                    selected = []
                    for setKey in self.usingSystems:
                        selected.append(setKey) if self.__keepSet(keepNotTested, usePreferedSetForGenre,
                                                                  self.configuration['exclusionType'], keepLevel,
                                                                  scores,
                                                                  setKey, genre, selected) else None

                    audit = audit + " SELECTED: " + str(selected)

                    for setKey in self.usingSystems:
                        setRom = os.path.join(self.configuration[setKey], game + ".zip")
                        setCHD = os.path.join(self.configuration['chd'], game) if 'chd' in self.configuration \
                            else os.path.join(self.configuration[setKey], game)
                        excludedBecauseCHDGame = 'excludeCHDGames' in self.configuration and \
                                                 self.configuration['excludeCHDGames'] == '1' and \
                                                 game in self.properties and \
                                                 self.properties[game].chd == 'yes'
                        image = self.configuration['imgNameFormat'].replace('{rom}', game)
                        if setKey in selected and not excludedBecauseCHDGame:
                            multiGameFoundInSet = True
                            utils.setFileCopy(self.configuration['exportDir'], setRom, genre, game, setKey,
                                              useGenreSubFolder, dryRun)
                            utils.setCHDCopy(self.configuration['exportDir'], setCHD, genre, game, setKey,
                                             useGenreSubFolder, dryRun)
                            utils.writeCSV(CSVs[setKey], game, scores[setKey], genre, dats[setKey], testForGame, setKey)
                            testStatus = self.getStatus(testForGame[setKey].status) \
                                if testForGame is not None and setKey in testForGame else 'UNTESTED &amp; FRESHLY ADDED'
                            utils.writeGamelistEntry(gamelists[setKey], game, image, dats[setKey], genre,
                                                     useGenreSubFolder, testForGame, setKey, testStatus)
                            roots[setKey].append(dats[setKey][game].node) if game in dats[setKey] else None
                            if scrapeImages:
                                utils.setImageCopy(self.configuration['exportDir'], self.configuration['images'], image,
                                                   setKey, dryRun)
                    # Works only if most recent game is first in line (raidendx;raidndx not the opposite)
                    if len(selected) == 0 and not multiGameFoundInSet:
                        notInAnySet.append(game)
                    elif len(selected) == 1:
                        if selected[0] not in onlyInOneSet:
                            onlyInOneSet[selected[0]] = []
                        onlyInOneSet[selected[0]].append(game)

                    self.logger.log("    " + audit)

        # writing and closing everything
        for setKey in self.usingSystems:
            treeSet = etree.ElementTree(roots[setKey])
            treeSet.write(os.path.join(self.configuration['exportDir'], setKey + ".dat"), xml_declaration=True,
                          encoding="utf-8")
            CSVs[setKey].close()
            gamelist.closeWrite(gamelists[setKey])

        scoreSheet.close()

        self.logger.log("\n<------------------ RESULTS ------------------>")
        self.logger.log("NOT FOUND IN ANY SET : " + str(len(notInAnySet)), self.logger.WARNING)
        self.logger.log(" ".join(notInAnySet), self.logger.WARNING)

    def __checkErrors(self, inputTests, keepLevel):
        self.logger.log("Loading Output Tests")
        outputTests = test.loadTests(Sorter.setKeys[self.hardware], os.path.join(self.configuration['exportDir']),
                                     self.usingSystems, self.logger)
        foundErrors = False
        for rom in inputTests.keys():

            romNotInFav = True
            multiName = []
            flatFavList = []
            for genre in self.favorites:
                flatFavList.extend(self.favorites[genre])

            for name in flatFavList:
                if name == rom:
                    romNotInFav = False
                    multiName = []
                    break
                elif (rom + ';') in name or (';' + rom) in name:
                    romNotInFav = False
                    multiName = name.split(';')
                    break

            if romNotInFav:
                if foundErrors is False:
                    self.logger.log("Possible errors", self.logger.ERROR)
                    foundErrors = True
                self.logger.log("    Orphan rom %s not in favs" % rom, self.logger.ERROR)

            # at least higher than keepLevel in one set
            higherThanKeepLevel = True
            for key in inputTests[rom]:
                higherThanKeepLevel = higherThanKeepLevel and inputTests[rom][key].status >= int(keepLevel)

            if higherThanKeepLevel:
                if rom not in outputTests:
                    inError = True
                    # Check if the rom is multiname or not
                    if len(multiName) > 0:
                        for name in multiName:
                            inError = name not in outputTests and inError
                    if inError:
                        if foundErrors is False:
                            self.logger.log("Possible errors", self.logger.WARNING)
                            foundErrors = True
                        self.logger.log("    ERROR " + rom + " not found in ouput csvs, but found in input",
                                        self.logger.ERROR)
                else:
                    for key in inputTests[rom]:
                        if key not in outputTests[rom]:
                            if foundErrors is False:
                                self.logger.log("Possible errors", self.logger.WARNING)
                                foundErrors = True
                            self.logger.log("    ERROR " + rom + " should be exported for " + key, self.logger.WARNING)

        if foundErrors is False:
            self.logger.log("\nS'all good man", self.logger.SUCCESS)
