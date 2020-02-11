# -*- coding: utf-8 -*-
import os.path
import utils

def parseSetFile(setFile, favorites) :
    file = open(setFile,'r')
    genre = None
    # Parse iniFile in iniFile dir    
    for line in file.readlines() :
        line = line.rstrip('\n\r ')
        if (line.startswith('[') and not line == '[FOLDER_SETTINGS]' and not line == '[ROOT_FOLDER]') :            
            genre = line
            if genre not in favorites :                
                favorites[genre] = []
        else :
            if (genre is not None and not line == '' ) :
                favorites[genre].append(line)
                
    file.close()

def loadFavs(scriptDir,fileName,bioses, logger) :    
    favorites = dict()    
    parseSetFile(os.path.join(scriptDir,utils.dataDir,fileName),favorites)
    
    logger.log('Nb Genre : '+ str(len(favorites)))    
    sumGames = 0
    for key in favorites.keys() :        
        sumGames = sumGames + len(favorites[key])
        
    logger.log('Nb Games : '+ str(sumGames))
    logger.log('Nb Bios : ' + str(len(bioses)))
    return favorites