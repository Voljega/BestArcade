[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/donate?hosted_button_id=LEAH843NKNG72)

## Best Arcade Tool

These tool handle two types of usage :
- generate retroarch sorted romsets (fbneo, mame2003, mame2003plus, mame2010, regular mame) keeping only the games referenced in the [BestArcade list](https://docs.google.com/spreadsheets/d/1S5qAI-TEl7wfqg6w9VNEwKciMGUtw40n9PS4xslkG3s/edit?usp=sharing), above and equal to the working state level you choose.
- generate dedicated romsets : custom mame based on Best Arcade list, neo geo aes set, atomiswave set, naomi set, handheld set

FbNeo version currently tested is Jun 13th, 2023
Handheld supported romset is currently at mame 0.255 level

### WHAT THIS TOOL DOESN'T DO :
- It's not clrmamepro and will not check that your romsets files are in the right version number
- It only works with non-merged sets, split and merged sets are not supported, use clrmamepro to generate non-merged sets if needed. However very few clones ares used, so it should be mostly ok with other type of sets.
- CHD are handled, decompressed CHD folder for each games must be located directly inside romset directory (i.e your romset directory should contain `kinst.zip` rom and `kinst` chd folder at the same level)
- It only works on Windows, well it should work on Linux by launching it manually with Python 3.7, but it needs testing to be sure. Please contact me through isues if you manage to make it work or encounter bugs

### WHAT THIS TOOL DO :

Retroarch tab :
- Available in Pi3, N2/N2+, N100 miniPCs flavor
- Only N100 tests will be maintained in the future, but feel free to share your tests for other machine types
- [BestArcade list for Raspberry Pi3](https://docs.google.com/spreadsheets/d/1S5qAI-TEl7wfqg6w9VNEwKciMGUtw40n9PS4xslkG3s/edit?usp=sharing)
- [BestArcade list for Odroid N2/N2+](https://docs.google.com/spreadsheets/d/1M4J1jIRgnoo5lVzYGYLGYm0_VPXfEiwUAl5XZ91ZsB8/edit?usp=sharing)
- [BestArcade list for N100 MiniPC](https://docs.google.com/spreadsheets/d/144LnHJMpPIIiknSP-TP1-i6jjxQqO_rLD-qtjVIdy20/edit?usp=sharing)  
- Generate BestArcade romsets by using your fbneo, mame2003, mame2003plus and mame2010 non-merged sets, your original sets will be kept intact
- Generate basic gamelist (Recalbox format but should work for other distribs) for your sets, with optional images. Genre images were generated with the awesome site [Game-icons.net](https://game-icons.net/)
- Generate csv files documenting the generated sets
- Generate a scoresheet comparing working level in generated sets
- Generate dat files for the generated romsets
- All needed DATs are included in the application

Custom tab :
- Same as above, without the testing part and everything related to it
- So it will generate a set of the most interesting games
- Mame DAT must be provided by the user

Neo Geo AES tab :
- Generate Neo Geo AES full set from either FBNeo or recent mame set, FBNeo is recommanded though
- FBNeo/Mame DAT must be provided by the user

Sega Model 2, Sega Model 3, Atomiswave, Naomi and Naomi2 tabs :
- Generate full sets of this system from a recent mame set
- Mame DAT must be provided by the user

Handhelds tab :
- Generate full set of all single-game (game & watch like, no consoles) handheld devices from a recent mame set
- Mame DAT must be provided by the user

### LINUX INSTALLATION AND EXECUTION :
- BestArcade requires that python3 is installed
- first install Tkinter for python3 if needed : `sudo apt-get install python3-tk`
- directly download sources or clone the repo with :
 ```
 sudo apt install git # optional, only if git is not installed
 git clone https://github.com/Voljega/BestArcade
 ```
- give execution rights to `BestArcade.sh` :
```
cd BestArcade            # change to BestArcade directory
chmod u+x BestArcade.sh  # give execution perms (already done in git-cloned version)
```
- launch with `./BestArcade.sh` or `./BestArcade`

### WINDOWS EXECUTION
Just execute `BestArcade.exe` from latest release

### USAGE
After execution your will find your generated romsets in your `exportDir`
See next part for configuration explanation

`Verify` will check the validity of the various folders and/or dats

`Save` will save you configuration to both the related `conf.conf` file (making a copy of the previous `conf.conf` file to `conf.bak`) and in memory

`Proceed` will save your configuration in memory only, leaving your `conf.conf` file intact and launch the whole process

You can build your own Windows version with the instructions found in `build.txt`

You can also directly modify conf files manually if you prefer, see next sections

### RETROARCH ROMSET CONFIGURATION :
You can modify your configuration by editing the `conf\conf-retroarch.conf` file either directly or from the UI with your own parameters :
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

### CUSTOM, NEO GEO AES, SEGA MODEL 2 & 3, ATOMISWAVE, NAOMI 1&2 AND HANDHELD ROMSETS CONFIGURATION :
You can modify your configuration by editing the related `conf\conf-*.conf` (`conf\conf-custom.conf`, `conf\conf-naomi.conf`, etc...) file either directly or from the UI with your own parameters :
- `exportDir` : the target directory for generation, warning its whole content will be erased (you will be prompted) at the begining of the script
- `custom`, `neogeoaes`, `model2`, `model3`, `atomiswave`, `naomi` or `handheld` : the path to your original sets, this will be left untouched by the script
- `dat` : the path to your set dat
- `images`: Paths to your images folder (flyers, screenshot, etc) separated by ';', will be checked in consecutive order
- `imgNameFormat` : the image name format in your images folder, '{rom}' part will be replaced by each rom name
- `dryRun` : If put to 1, will do a dry run, generating only csv and dat files without copying roms and bios, good for testing
- `genreSubFolders`: determines if your romset will use sub folders for genre or not
- `useImages`: determines if images will be used for gamelist

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate?hosted_button_id=LEAH843NKNG72)