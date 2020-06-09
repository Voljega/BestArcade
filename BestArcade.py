# -*- coding: utf-8 -*-
import sys, os.path
from gui import GUI
from logger import Logger
    
if __name__ == "__main__":
    scriptDir = os.path.abspath(os.path.dirname(sys.argv[0]))
    title = 'BestArcade 1.5'
    logger = Logger()
    logger.log(title)
    logger.log('\nScript path : '+scriptDir)            
    gui = GUI(scriptDir,logger, title) 
    gui.draw()


# FIXES/ENHANCEMENT
#-----------------
# scaling issue on MacOSX -> needs to externalize font size somehow
# resolution/size/scrollbar for lower resolutions than 1080p (see solution draft on my stackoverflow)

# error detecting is wrong for keepLevel WORKING and Exclusion Type Strict
# allow basicsorter generation without dat / prevents generation without dat ?
# add info to generate dat from mame exe (see my handheld thread on reddit) -> hhhhhhm si if regular xml from mame site work

# NEW SETS/TESTS
#----------------
# add neogeo MVS games tab
# retest for N2
# allow to choose between pi3 and N2
# add vertical games tab
