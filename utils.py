# -*- coding: utf-8 -*-

import collections,os.path, shutil
import gamelist

GUIString = collections.namedtuple('GUIString', 'id label help order')

# Static data
dataDir = r"data"
confDir = r"conf"
# Configuration
confFilename = r"conf-{setKey}"
guiStringsFilename = r'gui-en-{setKey}.csv' 

def getBioses(keyset) :        
    if keyset == 'atomiswave' :
        return ['awbios']
    elif keyset == 'naomi':
        return ['f355bios','f355dlx','naomi','naomigd','segasp','naomi2']
    elif keyset == 'handheld':
        return []
    elif keyset == 'neogeoaes':
        return ['neogeo']
    elif keyset == 'model2' or keyset == 'model3' :
        return []
    else :
        return ['acpsx','atarisy1','cpzn1','cpzn2','decocass','konamigv','konamigx','megaplay',
        'megatech','neogeo','nss','pgm','playch10','skns','stvbios','taitofx1','taitogn','taitotz','tps',
        'atarisy1','coh1000t','hng64','crysbios','coh1000a','coh1002e','coh1001l','coh1002m','coh3002t',
        'sys573','sys246','sys256','chihiro','ar_bios','aleck64','neocdz','isgsm',
        'midssio','nmk004','ym2608','maxaflex']
        
def getKeySetString(string,setKey) :
        return string.replace('{setKey}',setKey)
    
def getConfFilename(setKey) :
    return getKeySetString(confFilename,setKey)+'.conf'

def getConfBakFilename(setKey) :
    return getKeySetString(confFilename,setKey)+'.bak'

def getGuiStringsFilename(setKey) :
    return getKeySetString(guiStringsFilename,setKey)

# UI Strings
def loadUIStrings(scriptDir,guiStringsFilename) :
    guiStrings = dict()
    file = open(os.path.join(scriptDir,'GUI',guiStringsFilename),'r',encoding="utf-8")
    order = 0
    for line in file.readlines()[1:] :
        confLine = line.split(";")
        if len(confLine) == 3 :
            guiStrings[confLine[0]] = GUIString(confLine[0],confLine[1],confLine[2].rstrip('\n\r '), order)
            order = order + 1
    file.close()
    return guiStrings

# Sorting and generation
def setFileCopy(exportDir,romsetFile,genre,fileName,targetDir,useGenreSubFolder,dryRun) :
    if not dryRun :         
        if os.path.exists(romsetFile) :
            if useGenreSubFolder :
                shutil.copy2(romsetFile, os.path.join(exportDir,targetDir,genre,fileName+".zip"))
            else :
                shutil.copy2(romsetFile, os.path.join(exportDir,targetDir,fileName+".zip"))

def setCHDCopy(exportDir,romsetCHD,genre,fileName,targetDir,useGenreSubFolder,dryRun) :
    if not dryRun :         
        if os.path.exists(romsetCHD) and os.path.isdir(romsetCHD) :
            if useGenreSubFolder :
                shutil.copytree(romsetCHD, os.path.join(exportDir,targetDir,genre,fileName))
            else :
                shutil.copytree(romsetCHD, os.path.join(exportDir,targetDir,fileName))

def setImageCopy(exportDir,paths,fileName,targetDir,dryRun) :
    if not dryRun :
        for path in paths.split('|') :
            filePath = os.path.join(path.strip(),fileName)            
            if os.path.exists(filePath):
                shutil.copy2(filePath, os.path.join(exportDir,targetDir,'downloaded_images',fileName))
                return
            
def writeCSV(csvFile,game,score,genre,dat,test,setKey) :
    if game in dat :
        name = dat[game].description
        year = dat[game].year
        manufacturer = dat[game].manufacturer
    else :
        name, year, manufacturer = '','',''
        
    if test is not None and setKey in test :
        hardware = test[setKey].hardware
        comments = test[setKey].comments
        notes = test[setKey].notes
    else :
        hardware,comments,notes = '','',''
    
    genreExport = genre.replace('[','')
    genreExport = genreExport.replace(']','')
    if score is not None :    
        csvFile.write("%i;%s;%s;%s;%s;%s;%s;%s;%s\n" %(score,genreExport,name,game,year,manufacturer,hardware,comments,notes))
    else :
        csvFile.write("%s;%s;%s;%s;%s;%s;%s;%s\n" %(genreExport,name,game,year,manufacturer,hardware,comments,notes))
        
def writeGamelistHiddenEntry(gamelistFile,game,genre,useGenreSubFolder) :
    gamelist.writeGamelistHiddenEntry(gamelistFile,game+".zip",genre,useGenreSubFolder)

def writeGamelistEntry(gamelistFile,game,image,dat,genre,useGenreSubFolder,test,setKey,testStatus):
    frontPic = "./downloaded_images/"+image
    
    if game in dat :
        fullName = dat[game].description
        fullName.replace('&', '&amp;')
        name = fullName
        if '(' in name :
            indPar = name.index('(')
            name = name[:(indPar-1)].strip()
        if '[' in name :
            indPar = name.index('[')
            name = name[:(indPar-1)].strip()                    
            
        year = dat[game].year if dat[game].year else ''
        developer = dat[game].manufacturer.replace('&', '&amp;') if dat[game].manufacturer else ''
        cloneof = dat[game].cloneof
    else :
        fullName, name, year, developer, cloneof = '','','','',''
        
    if test is not None and setKey in test :
        hardware = test[setKey].hardware
        comments = test[setKey].comments
        notes = test[setKey].notes
    else :
        hardware,comments,notes = '','',''
        
    desc = ('Rom : '+game+' , Clone of : ' + cloneof + '\n') if cloneof else ('Rom : '+game+'\n')
    desc = desc + ('Fullname : '+fullName+'\n')
    if testStatus is not None :
        desc = desc + ('Status : ' + testStatus + '\n' )
    desc = desc + (('Hardware : ' + hardware + '\n') if hardware else '')
    desc = desc + ((comments + '\n') if comments else '')
    desc = desc + ((notes + '\n') if notes else '')
    desc = desc + '        '
    
    gamelist.writeGamelistEntry(gamelistFile,game+".zip",name,desc,year,frontPic,developer,developer,genre,useGenreSubFolder)            