#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-

import collections,os.path

GUIString = collections.namedtuple('GUIString', 'id label help order')

# UI Strings
def loadUIStrings(scriptDir,guiStringsFilename) :
    guiStrings = dict()
    file = open(os.path.join(scriptDir,'GUI',guiStringsFilename),'r')
    order = 0
    for line in file.readlines()[1:] :
        confLine = line.split(";")
        if len(confLine) == 3 :
            guiStrings[confLine[0]] = GUIString(confLine[0],confLine[1],confLine[2].rstrip('\n\r '), order)
            order = order + 1
    file.close()
    return guiStrings

# Sorting and generation
