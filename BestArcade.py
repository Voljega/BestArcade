import sys
import os.path
from gui import GUI
from logger import Logger

if __name__ == "__main__":
    scriptDir = os.path.abspath(os.path.dirname(sys.argv[0]))
    title = 'BestArcade 1.6'
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

# EXTRACT error
# needs to clean <unknown> in mame gamelist -> # CHK fix gamelist
# spclforc and spcfrcii should have sound past 0.252

# clean 'NOT FOUND in any set'

# CHD Handling
# ---------------
# check handeld / tvgames still working
# Modify README.md -> mention CHD defaults to rom folder

# Allow avoiding CHD games
# ------------------------
# use property file
# Modify README.md

# 3D games overhaul
# -------------------
# Games that ran on Atari/Midway's Seattle, Vegas, and Denver hardware - NFL Blitz, California Speed, Vapor TRX, Cart Fury, SF Rush, and SF Rush 2049, among others - can require a beefy CPU at times, but are in great shape.
#
# Incredible Technologies' "Eagle" platform is in the same boat, which includes Virtual Pool and the first few releases of Golden Tee Fore! and Big Buck Hunter.
#
# Gaelco's 3D titles are in pretty great shape.
#
# Cruis'n USA, Cruis'n World, War Gods, and Off Road Challenge, likewise.
#
# 3DO M2 runs well but is on the slow side.
#
# Various 3D Konami games are in great shape, including GTI Club, Solar Assault, Polygonet Commanders, and various others.
#
# Namco System 22 (Ridge Racer, Prop Cycle, and various others" are in pretty great shape, too.
#
# PS1-based hardware (Namco System 10/11/12, Konami GQ/GV, Capcom ZN1/ZN2, and others, which encompass loads of games) is in pretty decent shape as well.
#
# Sega Model 1 is in okay shape, but needs some additional bugfixing by Olivier at some point.
#
# Sega Model 2 needs some deep digging into how it's rasterizer functions, as that's something ElSemi never even managed without cramming hacks upon hacks into NebulaM2.
#
# Sega Model 3 could really use some love, Supermodel is a better choice right now.
#
# Namco System 21 is hit-or-miss depending on the generation of the board involved.


# IDEAS
# -----------------
# error detecting is wrong for keepLevel WORKING and Exclusion Type Strict
# allow basicsorter generation without dat / prevents generation without dat ?
# add info to generate dat from mame exe (see my handheld thread on reddit)
#   -> hhhhhhm see if regular xml from mame site work
# mame64.exe -listxml > mame.dat

# allow multiple extractions
# try to handle gracefully placeholder values for all paths -> just use default values
# allow exclusion of games genres (i.e. no Puzzle games)

# NEW SETS/TESTS
# ----------------
# add neogeo MVS games tab
# add vertical games tab

# SET ERRORS & CHECKS
# --------------------
# BAD BROKEN CHD fghtmn for latest Mame

# ddp2 not found in fbneo set when it should

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
# sega system 1 v0.213
# sega system 16 v0.213
# sega system 18 v0.213
# sega system 24 v0.213
# sega system 32 v0.213
# seta1 v0.213
# sony zn1 zn2 v0.213
# taito f2 v0.213
# taito f3 v0.213
# toaplan v0.213
# williams v0.213
