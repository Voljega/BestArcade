#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-
import sys, os.path
from gui import GUI
from logger import Logger

scriptDir=r""

configuration = dict()
    
if __name__ == "__main__":
    scriptDir = os.path.abspath(os.path.dirname(sys.argv[0]))
    logger = Logger()    
    logger.log('Script path : '+scriptDir)            
    gui = GUI(scriptDir,logger)    
    gui.draw()


# TODO

#Try to handle CHD in a graceful way
#Add several tabs to the UI to handle more sets : naomi / atomiswave, and if possible handhelds (Tiger, G&W, etc...)
#In the far future (hopefully before Skynet rise), tests on a more powerfull SBC, either RockPro64, Odroid XU4 or Odroid N2
