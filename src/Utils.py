
class ParsingUtils(object):

    @staticmethod
    def parseStoreLineIntoStoreVariables(line):
        splitLine = line.split(' ')
        numberOfCommands = splitLine[0]
        dstMemoryAddressStr = splitLine[2]
        dataToStore = splitLine[3].rstrip('\n')
        dataToStore = [dataToStore[i:i + 2] for i in xrange(0, len(dataToStore), 2)]
        return numberOfCommands, dstMemoryAddressStr, dataToStore

    @staticmethod
    def parseLoadLineIntoStoreVariables(line):
        splitLine = line.split(' ')
        numberOfCommands = splitLine[0]
        srcMemoryAddressStr = splitLine[2].rstrip('\n')
        return numberOfCommands, srcMemoryAddressStr
