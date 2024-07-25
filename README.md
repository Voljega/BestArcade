[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/donate?hosted_button_id=LEAH843NKNG72)

## Best Arcade Tool

The main purpose of this tool is to filter mame/fbneo romsets to keep only the arcade games, removing:
- clones
- mahjong, medal redemption & gambling games
- adult games  
- electromechanical games and other non arcade games

This tool handles two types of usage :
- generate retroarch sorted romsets (fbneo, mame2003, mame2003plus, mame2010, regular mame) keeping only the games referenced in the [BestArcade list](https://docs.google.com/spreadsheets/d/1S5qAI-TEl7wfqg6w9VNEwKciMGUtw40n9PS4xslkG3s/edit?usp=sharing), above and equal to the working state level you choose.
  

- generate dedicated system romsets : custom mame based on Best Arcade list, neo geo aes set, sega model 2 & 3 sets, atomiswave set, naomi & naomi 2 sets, namco2x6 set, handheld set, tvgames set

FbNeo version currently tested is Apr 30th, 2024
Handheld supported romset is currently at mame 0.267 level

### WHAT THIS TOOL DOESN'T DO :
- It's not clrmamepro and will not check that your romsets files are in the right version number  
  

- It only works with non-merged sets, split and merged sets are not supported, use clrmamepro to generate non-merged sets if needed. However very few clones ares used, so it should be mostly ok with other type of sets.
  

- CHD are handled, decompressed CHD folder for each games must be located inside your CHD folder or will default to romset directory (i.e your CHD directory should contain `kinst.zip` rom and `kinst` chd folder at the same level)
  

- You can exclude CHD games from generation if that's what you want

### WHAT THIS TOOL DO :

[Detailed functionalities](https://github.com/Voljega/BestArcade/wiki/What-this-Tool-Do)

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
see the wiki page [Retroarch Romset Configuration](https://github.com/Voljega/BestArcade/wiki/Retroarch-Romset-Configuration)


### CUSTOM, NEO GEO AES, SEGA MODEL 2 & 3, ATOMISWAVE, NAOMI 1&2, NAMCO 2x6 AND HANDHELD ROMSETS CONFIGURATION :
see the wiki page [Custom & Specific Romsets Configuration](https://github.com/Voljega/BestArcade/wiki/Custom-&-Specific-Romsets-Configuration)

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate?hosted_button_id=LEAH843NKNG72)