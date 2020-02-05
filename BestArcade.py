#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-
import sys, os.path
from gui import GUI
from logger import Logger
    
if __name__ == "__main__":
    scriptDir = os.path.abspath(os.path.dirname(sys.argv[0]))
    logger = Logger()
    logger.log('BestArcade 1.3')
    logger.log('\nScript path : '+scriptDir)            
    gui = GUI(scriptDir,logger) 
    gui.draw()


# TODO

# might need to kill sorters thread when exiting UI ??

# allow basicsorter generation without dat

# custom icon

# remove atomiswave & naomi games from regular (BigSet and custom) ini and tests
# check samurai & baby cart, glob and super glob games (also any arcade game in Reddit saved post)
# check psyvarar2 shit (should be in naomi anyway)

# full regeneration of all 4 tabs romsets

# release 1.3

# Add handhelds tab (Tiger, G&W, etc...) if possible
# In the far future (hopefully before Skynet rise), tests on a more powerfull SBC, either RockPro64, Odroid XU4 or Odroid N2
