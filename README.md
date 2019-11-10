## Best Arcade Tool

Use this tool to generate sorted romsets keeping only the games referenced in the [BestArcade list](https://docs.google.com/spreadsheets/d/1S5qAI-TEl7wfqg6w9VNEwKciMGUtw40n9PS4xslkG3s/edit?usp=sharing), above and equal to the working state level you choose.

Fbneo version currently handled is October 10th, 2019

### WHAT THIS TOOL DOESN'T DO :
- It's not clrmamepro and will not check that your romsets files are in the right version number
- It only works with non-merged sets, split and merged sets are not supported, use clrmamepro to generate non-merged sets if needed
- It doesn't handle CHD
- It only works on Windows, well it should work on Linux by launching it manually with Python 3.7, but it needs testing to be sure.

### WHAT THIS TOOL DO :
- Generate BestArcade romsets by using your fbneo, mame2003, mame2003plus and mame2010 non-merged sets, your original sets will be kept intact
- Generate basic gamelist (Recalbox format but should work for other distribs) for your sets, with optional images. Genre images were generated with the awesome site [Game-icons.net](https://game-icons.net/)
- Generate csv files documenting the generated sets
- Generate a scoresheet comparing working level in generated sets
- Generate dat files for the generated romsets

### USAGE :
Just execute `BestArcade.exe`
After execution your will find your generated romsets in your `exportDir`
See next part for configuration explanation

`Verify` will check the validity of the various folders

`Save` will save you configuration to both the `conf.conf` file (making a copy of the previous `conf.conf` file to  `conf.bak`) and in memory

`Proceed` will save you configuration in memory only, leaving your `conf.conf` file intact and launch the whole process

You can build your own version with the instructions found in `build.txt`

### CONFIGURATION :
You can modify your configuration by editing the `conf.conf` file either directly or from the UI with your own parameters :
- `exportDir` : the target directory for generation, warning its whole content will be erased (you will be prompted) at the begining of the script
- `fbneo`, `mame2003`, `mame2003plus`, `mame2010` : the path to your original sets, this will be left untouched by the script
- `images`: Paths to your images folder (flyers, screenshot, etc) separated by ';', will be checked in consecutive order
- `imgNameFormat` : the image name format in your images folder, '{rom}' part will be replaced by each rom name
- `dryRun` : If put to 1, will do a dry run, generating only csv and dat files without copying roms and bios, good for testing
- `keepLevel`: the working state level at which you will keep the roms in the generated romset (i.e keepLevel 2 will keep only MOSTLY_WORKING and WORKING roms)
- `keepNotTested`: determines if untested roms will be kept or not, even in STRICT mode
- `exclusionType`: determines how roms will be kept (based on their working state level) if you use several romsets
- `preferedSet`: in strict mode, if rom has same working level in several sets, preferedSet will be chosen
- `usePreferedSetForGenre` : in strict mode, activate use of prefered set for specific genres
- `BeatEmUpPreferedSet`,`GunPreferedSet`,`MiscPreferedSet`,`PlatformPreferedSet`,`PuzzlePreferedSet`,`RacePreferedSet`,`RunNGunPreferedSet`,`ShootEmUpPreferedSet`,`SportPreferedSet`,`VsFightingPreferedSet` list of settings for prefered set for genre
- `genreSubFolders`: determines if your romset will use sub folders for genre or not
- `useImages`: determines if images will be used for gamelist
