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

# problems with empty name for all handheld

# test new games / update csvs in repo

# solve compilation questions and try on an ubuntu VM

# allow basicsorter generation without dat / prevents generation without dat ? 

# custom icon
