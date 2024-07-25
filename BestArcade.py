import sys
import os.path
from gui import GUI
from logger import Logger

if __name__ == "__main__":
    scriptDir = os.path.abspath(os.path.dirname(sys.argv[0]))
    title = 'BestArcade 1.8'
    logger = Logger()
    logger.log(title)
    logger.log('\nScript path: ' + scriptDir)
    gui = GUI(scriptDir, logger, title)
    gui.draw()

# FIXES/ENHANCEMENT
# -----------------
# github issues
# scaling issue on MacOSX -> needs to externalize font size somehow
#   -> done with slider but slider doesn't appear on MacOS, revert slider ?
# resolution/size/scrollbar for lower resolutions than 1080p (see solution draft on my stackoverflow)

# spclforc and spcfrcii should have sound past 0.252

# error detecting is wrong for keepLevel WORKING and Exclusion Type Strict
# allow basicsorter generation without dat / prevents generation without dat ?
# add info to generate dat from mame exe (see my handheld thread on reddit)
#   -> hhhhhhm see if regular xml from mame site work
# mame64.exe -listxml > mame.dat

# try to handle gracefully placeholder values for all paths -> just use default values
# allow exclusion of games genres (i.e. no Puzzle games)

# NEW SETS/TESTS
# ----------------
# add neogeo MVS games tab
# add vertical games tab
