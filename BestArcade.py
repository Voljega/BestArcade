import sys
import os.path
from gui import GUI
from logger import Logger

if __name__ == "__main__":
    scriptDir = os.path.abspath(os.path.dirname(sys.argv[0]))
    title = 'BestArcade 1.6'
    logger = Logger()
    logger.log(title)
    logger.log('\nScript path : ' + scriptDir)
    gui = GUI(scriptDir, logger, title)
    gui.draw()

# FIXES/ENHANCEMENT
# -----------------
# scaling issue on MacOSX -> needs to externalize font size somehow
#   -> done with slider but slider doesn't appear on MacOS, revert slider ?
# resolution/size/scrollbar for lower resolutions than 1080p (see solution draft on my stackoverflow)
# allow to choose between pi3 and N2 -> double tab retroarch using hardware parameters when initializing RetroarchGUI

# error detecting is wrong for keepLevel WORKING and Exclusion Type Strict
# allow basicsorter generation without dat / prevents generation without dat ?
# add info to generate dat from mame exe (see my handheld thread on reddit)
#   -> hhhhhhm si if regular xml from mame site work
# mame64.exe -listxml > mame.dat

# allow multiple extractions
# try to handle gracefully placeholder values for all paths -> just use default values
# allow exclusion of games genres (i.e. no Puzzle games)
# move bios from utils to .ini

# NEW SETS/TESTS
# ----------------
# add neogeo MVS games tab
# retest for N2
# add vertical games tab

# SET ERRORS & CHECKS
# --------------------
# CHK Rumba Lumber
# ironhors -> RunNGun
# loht -> RunNGun
# mightguy -> ShootEmUp
# thundfox -> RunNGun
# ddpdojp -> clone of ddp3, remove it
# CHK Opa Opa (opaopa)
# CHK Video Vince (vidvince)
# BAD BROKEN CHD fghtmn for latest Mame
# xmen6p
# fantland -> RunNGun
# dynagear -> RunNGun
# biomtoy -> RunNGun
# CHK sexyparo  (J) / sexyparoa (En?) clone/parent
# orleg2 -> BeatEmUp
# aliensyn -> ShootEmUp
# chaoshea -> ShootEmUp
# CHK les deux flavour de Demon's World sont là
# desertbr -> ShootEmUp
# flamegun -> ShootEmUp
# greenber -> Misc
# riot -> ShootEmUp
# CHK coolridr en double ?

# MAYBE not delete old names, usefull for old sets
# DELETE tvrs2 non working bootleg of Rastar
# MAYBE DELETE dw old name of Dynasty Wars
# CHECK ALL REN
# MAYBE DELETE snowbros3, old name of snowbro3
# MAYBE DELETE moo, old name of moomesa
# MAYBE DELETE platoon, old name of nvs_platoon

# capcom cps-1 v0.213
# capcom cps-2 v0.213
# capcom cps-3 v0.213
# cave pgm v0.213
# irem m-72 v0.213
# irem m-92 v0.213
# itech32 v0.213
# konami system573 v0.213
# mitchell v0.213
# namco s1 v0.213
# namco s12 v0.213
# namco s2 v0.213
# nmk 16 v0.213
# sega model 1 v0.213
# sega model 2 v0.213
# sega model 3 v0.213
# sega naomi v0.213
# sega stv v0.213
# sega system 1 v0.213
# sega system 16 v0.213
# sega system 18 v0.213
# sega system 24 v0.213
# sega system 32 v0.213
# sega system c-2 v0.213
# seta1 v0.213
# snk neogeo v0.213
# sony zn1 zn2 v0.213
# taito f2 v0.213
# taito f3 v0.213
# toaplan v0.213
# triforce v0.213
# williams v0.213
