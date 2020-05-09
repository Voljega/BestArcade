# -*- coding: utf-8 -*-

import xml.etree.ElementTree as etree
import os.path, shutil
import gamelist, utils
import fav, dat

class BasicSorter :  
    
    def __init__(self,configuration,scriptDir,logger,bioses,setKey) :
        self.configuration = configuration               
        self.scriptDir = scriptDir
        self.logger = logger
        self.bioses = bioses
        self.setKey = setKey
        
    def process(self) :        
        self.prepare()
        # create bestarcade romsets
        self.logger.log('\n<--------- Create Sets --------->')        
        self.createSets(self.dats)
        self.logger.log("\n<--------- Detecting errors ----------->")
        self.checkErrors()
        self.logger.log('\n<--------- Process finished ----------->')
#            input('\n             (Press Enter)              ')
        
    def prepare(self) :
        self.usingSystems = self.useSystems(self.configuration)
        # create favorites containing fav games
        self.logger.log('\n<--------- Load Favorites Ini Files --------->')
        self.favorites = fav.loadFavs(self.scriptDir,self.setKey+'.ini',self.bioses,self.logger)
        # parse dat files
        self.logger.log('\n<--------- Load '+self.setKey+' dat --------->')        
        if 'dat' in self.configuration and os.path.exists(self.configuration['dat']) :                
            datsDict = dict(zip([self.setKey],[self.configuration['dat']]))
        else :
            datsDict = dict(zip([self.setKey],[self.setKey+'.dat']))
        self.dats = dat.parseDats(self.scriptDir,utils.dataDir,datsDict,self.usingSystems,self.logger)
        
    def useSystems(self,configuration) :
        systems = []        
        systems.append(self.setKey) if os.path.exists(configuration[self.setKey]) else None            
        self.logger.logList('Using systems',systems)
        return systems
    
    def createSets(self,dats) :
        
        self.logger.log('Creating or cleaning output directory '+ self.configuration['exportDir'])
        if os.path.exists(self.configuration['exportDir']) :
            for file in os.listdir(os.path.join(self.configuration['exportDir'])) :
                fullPath = os.path.join(self.configuration['exportDir'],file)        
                shutil.rmtree(fullPath) if os.path.isdir(fullPath) else os.remove(fullPath)
        else :
            os.makedirs(self.configuration['exportDir'])            
        
        dryRun = True if self.configuration['dryRun'] == '1' else False
        useGenreSubFolder = True if self.configuration['genreSubFolders'] == '1' else False        
        scrapeImages = True if self.configuration['useImages'] == '1' and self.configuration['images'] else False
        
        CSVs, gamelists, roots = dict(), dict(), dict()
        header="Genre;Name (mame description);Rom name;Year;Manufacturer;Hardware;Comments;Notes\n"
        
        # init CSVS
        CSVs[self.setKey] = open(os.path.join(self.configuration['exportDir'],self.setKey+".csv"),"w",encoding="utf-8")
        CSVs[self.setKey].write(header)
        # init gamelists
        roots[self.setKey] = etree.Element("datafile")
        roots[self.setKey].append(dats[self.setKey+"Header"])   
        os.makedirs(os.path.join(self.configuration['exportDir'],self.setKey))
        os.makedirs(os.path.join(self.configuration['exportDir'],self.setKey,'downloaded_images')) if scrapeImages else None        
        gamelists[self.setKey] = gamelist.initWrite(os.path.join(self.configuration['exportDir'],self.setKey))
        
        for genre in self.favorites.keys() :
            self.logger.log("Handling genre "+ genre)
            
            if useGenreSubFolder :                
                os.makedirs(os.path.join(self.configuration['exportDir'],self.setKey,genre))
                if scrapeImages :
                    gamelist.writeGamelistFolder(gamelists[self.setKey],genre,genre+'.png')
                    utils.setImageCopy(self.configuration['exportDir'],os.path.join(self.scriptDir,'data','images'),genre+'.png',self.setKey,dryRun)
                
            # copy bios in each subdirectory
            for bios in self.bioses :
                setBios = os.path.join(self.configuration[self.setKey],bios+".zip")
                utils.setFileCopy(self.configuration['exportDir'],setBios,genre,bios,self.setKey,useGenreSubFolder,dryRun)
                if os.path.exists(setBios) :
                    utils.writeGamelistHiddenEntry(gamelists[self.setKey],bios,genre,useGenreSubFolder)
            
            for game in sorted(self.favorites[genre]) :                
                
                setRom = os.path.join(self.configuration[self.setKey],game+".zip")
                setCHD = os.path.join(self.configuration[self.setKey],game)
                image = self.configuration['imgNameFormat'].replace('{rom}',game)                    
                # TODO aliases should be handled here
                utils.setFileCopy(self.configuration['exportDir'],setRom,genre,game,self.setKey,useGenreSubFolder,dryRun)
                utils.setCHDCopy(self.configuration['exportDir'],setCHD,genre,game,self.setKey,useGenreSubFolder,dryRun)
                utils.writeCSV(CSVs[self.setKey],game,None,genre,dats[self.setKey],None,self.setKey)                    
                utils.writeGamelistEntry(gamelists[self.setKey],game,image,dats[self.setKey],genre,useGenreSubFolder,None,self.setKey,None)
                roots[self.setKey].append(dats[self.setKey][game].node) if game in dats[self.setKey] else None
                if scrapeImages :                          
                    utils.setImageCopy(self.configuration['exportDir'],self.configuration['images'],image,self.setKey,dryRun)
                
                self.logger.log(setRom)
        
        # writing and closing everything        
        treeSet = etree.ElementTree(roots[self.setKey])
        treeSet.write(os.path.join(self.configuration['exportDir'],self.setKey+".dat"), xml_declaration=True, encoding="utf-8")
        CSVs[self.setKey].close()
        gamelist.closeWrite(gamelists[self.setKey])

    def checkErrors(self) :        
        foundErrors = False
        useGenreSubFolder = True if self.configuration['genreSubFolders'] == '1' else False
        dryRun = True if self.configuration['dryRun'] == '1' else False
        if not dryRun :
            for genre in self.favorites :
                for name in self.favorites[genre] :
                    if useGenreSubFolder :
                        setRom = os.path.join(self.configuration['exportDir'],self.setKey,genre,name+".zip")
                    else :
                        setRom = os.path.join(self.configuration['exportDir'],self.setKey,name+".zip")
                    if not os.path.exists(setRom) :
                        if foundErrors is False :
                            self.logger.log("Possible errors")
                            foundErrors = True
                        self.logger.log(setRom +' is missing in output dir')
                        
        if foundErrors is False :
            self.logger.log("S'all good man")
            
                            
# TODOS
# if name from dat is empty, take one from test file