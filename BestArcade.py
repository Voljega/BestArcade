#!/usr/lib/python2.7/
# -*- coding: utf-8 -*-
import sys, os.path, conf
from gui import GUI
from logger import Logger

scriptDir = r""

outputDir = r"output"
confFile = r"conf.conf"
scriptDir=r""

favorites = dict()
configuration = dict()
usingSystems = []
    
if __name__ == "__main__":
    scriptDir = os.path.abspath(os.path.dirname(sys.argv[0]))
    logger = Logger()    
    logger.log('Script path : '+scriptDir)
    # load conf.conf
    configuration = conf.loadConf(os.path.join(scriptDir,confFile))    
    gui = GUI(configuration,scriptDir,logger)
    logger.log('\n<--------- Load Configuration File --------->')
    logger.printDict(configuration)
    gui.draw()
    
#TODO exit terminal when GUI is closed