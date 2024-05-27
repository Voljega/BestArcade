import collections
import os

Properties = collections.namedtuple('Properties', 'rom orientation chd samples')


def cleanString(string):
    return string.rstrip('\n\r ').lstrip()


def loadProperties(propertyFile):
    properties = dict()
    file = open(propertyFile, 'r', encoding="utf-8")

    countLine = 0

    for line in file.readlines()[1:]:
        countLine = countLine + 1
        propertiesLine = line.split(";")
        # print(testLine)
        rom = cleanString(propertiesLine[0])
        orientation = cleanString(propertiesLine[1])
        chd = cleanString(propertiesLine[2])
        samples = cleanString(propertiesLine[3])
        # print(rom,status)
        romProperties = Properties(rom, orientation, chd, samples)
        properties[rom] = romProperties

    file.close()
    return properties
