import os.path

def cleanString(string):
    return string.rstrip('\n\r ').lstrip()


# GUI string ids that are not configuration values
NON_CONF_KEYS = ['verify', 'save', 'proceed', 'confirm', 'selectRomsetDir', 'selectCHDDir', 'selectDat',
                 'selectExportDir', 'selectImages']
# Defaults other than an empty value
DEFAULT_VALUES = {'imgNameFormat': '{rom}.png', 'dryRun': '1', 'genreSubFolders': '1', 'useImages': '1',
                  'excludeCHDGames': '0', 'keepLevel': '0', 'keepNotTested': '1', 'exclusionType': 'NONE',
                  'usePreferedSetForGenre': '0'}


def defaultConf(guiStrings):
    return {key: DEFAULT_VALUES.get(key, '') for key in guiStrings if key not in NON_CONF_KEYS}


def loadConf(confFile, guiStrings):
    """Load confFile over the defaults of the given GUI strings, a missing file gives the defaults only"""
    conf = defaultConf(guiStrings)
    if not os.path.exists(confFile):
        return conf

    file = open(confFile, 'r', encoding="utf-8")
    for line in file.readlines():
        if not line.startswith('#'):
            confLine = line.split("=")
            if len(confLine) == 2:
                conf[cleanString(confLine[0])] = cleanString(confLine[1])

    file.close()
    return conf
