
class Utils(object):

    @staticmethod
    def parseStoreCmd(line):
        """
        given a 'Store' command, parse it into its different variables
        :param line: the current command in the trace
        :return numberOfCommands, dstMemoryAddressStr, dataToStore:
        """
        splitLine = line.split(' ')
        numberOfCommands = splitLine[0]
        dstMemoryAddressStr = splitLine[2]
        dataToStore = splitLine[3].rstrip('\n')
        dataToStore = [dataToStore[i:i + 2] for i in xrange(0, len(dataToStore), 2)]
        return numberOfCommands, dstMemoryAddressStr, dataToStore

    @staticmethod
    def parseLoadCmd(line):
        """
        given a 'Load' command, parse it into its different variables
        :param line: the current command in the trace
        :return numberOfCommands, dstMemoryAddressStr:
        """
        splitLine = line.split(' ')
        numberOfCommands = splitLine[0]
        srcMemoryAddressStr = splitLine[2].rstrip('\n')
        return numberOfCommands, srcMemoryAddressStr

    @staticmethod
    def sumStatResults(totalNumberOfCycles, mainMemory, l1Cache, l2Cache):
        """
        calculate all the relevant stats the are needed for presentation in the end of the simulation
        :param totalNumberOfCycles:
        :param mainMemory:
        :param l1Cache:
        :param l2Cache:
        :return stats: A list containing all the results
        """
        if l2Cache is None:
            mainMemoryAccessTime = mainMemory.getTotalActualAccessTime(l1Cache.blockSize)
            l2CacheAccessTime = 0
            l1CacheAccessTime = l1Cache.getTotalActualAccessTime(4)
            l2Misses = 0
            l2Hits = 0
            l2Stats = [0, 0, 0, 0]
        else:
            mainMemoryAccessTime = mainMemory.getTotalActualAccessTime(l2Cache.blockSize)
            l2CacheAccessTime = l2Cache.getTotalActualAccessTime(l1Cache.blockSize)
            l1CacheAccessTime = l1Cache.getTotalActualAccessTime(4)
            l2Misses = (l2Cache.readMisses + l2Cache.writeMisses)
            l2Hits = (l2Cache.readHits + l2Cache.writeHits)
            l2Stats = [l2Cache.readHits, l2Cache.writeHits, l2Cache.readMisses, l2Cache.writeMisses]

        totalAccessTime = mainMemoryAccessTime + l2CacheAccessTime + l1CacheAccessTime
        programRunningTimeInCycles = totalNumberOfCycles + totalAccessTime
        l1Misses = (l1Cache.readMisses + l1Cache.writeMisses)
        l1Hits = (l1Cache.readHits + l1Cache.writeHits)
        l1LocalMissRate = (1.0 * l1Misses) / (l1Misses + l1Hits)
        globalMissRate = (1.0 * l1Misses + l2Misses) / (l1Misses + l1Hits + l2Misses + l2Hits)
        amat = (1.0 * programRunningTimeInCycles) / (l1Misses + l1Hits + l2Misses + l2Hits)

        l1Stats = [l1Cache.readHits, l1Cache.writeHits, l1Cache.readMisses, l1Cache.writeMisses]
        generalStats = [format(l1LocalMissRate, '.4f'), format(globalMissRate, '.4f'), format(amat, '.4f')]
        stats = [programRunningTimeInCycles] + l1Stats + l2Stats + generalStats

        return stats
