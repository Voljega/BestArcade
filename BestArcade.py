import sys
import os.path
from gui import GUI
from logger import Logger
from version import VERSION

if __name__ == "__main__":
    scriptDir = os.path.abspath(os.path.dirname(sys.argv[0]))
    title = 'BestArcade ' + VERSION
    logger = Logger()
    logger.log(title)
    logger.log('\nScript path: ' + scriptDir)
    gui = GUI(scriptDir, logger, title)
    gui.draw()

# FIXES/ENHANCEMENT
# -----------------
# github issues
# resolution/size/scrollbar for lower resolutions than 1080p (see solution draft on my stackoverflow)

# spclforc and spcfrcii should have sound past 0.252

# error detecting is wrong for keepLevel WORKING and Exclusion Type Strict
# add info to generate dat from mame exe (see my handheld thread on reddit)
#   -> hhhhhhm see if regular xml from mame site work
# mame64.exe -listxml > mame.dat
# allow exclusion of games genres (i.e. no Puzzle games)

# NEW SETS/TESTS
# ----------------
# add neogeo MVS games tab
# add vertical games tab
