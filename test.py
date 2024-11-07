import collections
import os

Test = collections.namedtuple('Test', 'status genre name rom year manufacturer hardware comments notes')


def cleanString(string):
    return string.rstrip('\n\r ').lstrip()


def loadTest(testFile, key, allTests):
    tests = dict()
    file = open(testFile, 'r', encoding="utf-8")

    countLine = 0

    for line in file.readlines()[1:]:
        countLine = countLine + 1
        testLine = line.split(";")
        # print(testLine)
        rom = cleanString(testLine[3])
        status = int(cleanString(testLine[0])) if cleanString(testLine[0]) != '' else -1
        # print(rom,status)
        test = Test(status, cleanString(testLine[1]), cleanString(testLine[2]),
                    rom, cleanString(testLine[4]), cleanString(testLine[5]),
                    cleanString(testLine[6]), cleanString(testLine[7]), cleanString(testLine[8]))
        if rom not in allTests:
            allTests[rom] = dict()
        allTests[rom][key] = test
        tests[rom] = test

    #    print("debug loadTest %s lines %i -> dict %i" %(key,countLine,len(tests)))

    file.close()
    return tests


def loadTests(setKeys, sourceDir, usingSystems, logger):
    allTests = dict()
    for setKey in setKeys:
        if setKey in usingSystems:
            setTests = loadTest(os.path.join(sourceDir, setKey + '.csv'), setKey, allTests)
            logger.log('    Found ' + str(len(setTests)) + ' ' + setKey + ' tests')
            if len(setTests) == 0:
                continue
            logger.log('      WORKING {0:.2f} %'.format(
                len(list(filter(lambda x: setTests[x].status == 3, setTests.keys()))) * 100 / len(setTests)),
                logger.SUCCESS)
            logger.log('      MOSTLY WORKING {0:.2f} %'.format(
                len(list(filter(lambda x: setTests[x].status == 2, setTests.keys()))) * 100 / len(setTests)))
            logger.log('      BADLY WORKING {0:.2f} %'.format(
                len(list(filter(lambda x: setTests[x].status == 1, setTests.keys()))) * 100 / len(setTests)),
                logger.WARNING)
            logger.log('      NON WORKING {0:.2f} %'.format(
                len(list(filter(lambda x: setTests[x].status == 0, setTests.keys()))) * 100 / len(setTests)),
                logger.ERROR)
            logger.log('      UNTESTED {0:.2f} %'.format(
                len(list(filter(lambda x: setTests[x].status == -1, setTests.keys()))) * 100 / len(setTests)),
                logger.UNKNOWN)

    logger.log('    Found ' + str(len(allTests)) + ' unique tests')
    return allTests
