import sys
import Memory
import config
from Utils import ParsingUtils


def sumStatResults(totalNumberOfCycles, mainMemory, l1Cache, l2Cache):
    if l2Cache == None:
        mainMemoryAccessTime = mainMemory.getTotalActualAccessTime(l1Cache.blockSize)
        l2CacheAccessTime = 0
        l1CacheAccessTime = mainMemory.getTotalActualAccessTime(4)
        l2Misses = 0
        l2Hits = 0

    else:
        mainMemoryAccessTime = mainMemory.getTotalActualAccessTime(l2Cache.blockSize)
        l2CacheAccessTime = mainMemory.getTotalActualAccessTime(l1Cache.blockSize)
        l1CacheAccessTime = mainMemory.getTotalActualAccessTime(4)
        l2Misses = (l2Cache.readMisses + l2Cache.writeMisses)
        l2Hits = (l2Cache.readHits + l2Cache.writeHits)

    totalAccessTime = mainMemoryAccessTime + l2CacheAccessTime + l1CacheAccessTime
    programRunningTimeInCycles = totalNumberOfCycles + totalAccessTime
    l1Misses = (l1Cache.readMisses + l1Cache.writeMisses)
    l1Hits = (l1Cache.readHits + l1Cache.writeHits)
    l1LocalMissRate = (1.0 * l1Misses) / (l1Misses + l1Hits)
    globalMissRate = (1.0 * l1Misses + l2Misses) / (l1Misses + l1Hits + l2Misses + l2Hits)
    amat = (1.0 * programRunningTimeInCycles) / (l1Misses + l1Hits + l2Misses + l2Hits) 
    
    if l2Cache != None:
        stats = [programRunningTimeInCycles,
                 l1Cache.readHits,
                 l1Cache.writeHits,
                 l1Cache.readMisses,
                 l1Cache.writeMisses,
                 l2Cache.readHits,
                 l2Cache.writeHits,
                 l2Cache.readMisses,
                 l2Cache.writeMisses,
                 format(l1LocalMissRate, '.4f'),
                 format(globalMissRate, '.4f'),
                 format(amat, '.4f')]
    else:
        stats = [programRunningTimeInCycles,
                 l1Cache.readHits,
                 l1Cache.writeHits,
                 l1Cache.readMisses,
                 l1Cache.writeMisses,
                 0,
                 0,
                 0,
                 0,
                 format(l1LocalMissRate, '.4f'),
                 format(globalMissRate, '.4f'),
                 format(amat, '.4f')]
    
    return stats

def saveSimulationResultsToFiles(mainMemory, l1Cache, l2Cache, statResults):
    mainMemory.saveMemoryToFile(config.getMainMemoryStatusOutputFilePath())
    l1Cache.saveMemoryToFile(config.getL1CacheStatusOutputFilePath())
    if l2Cache:
        l2Cache.saveMemoryToFile(config.getL2Way0CacheStatusOutputFilePath())
        l2Cache.saveMemoryToFile(config.getL2Way1CacheStatusOutputFilePath())

    with open(config.getStatsFileName(), 'w') as statsFile:
        for stat in statResults:
            statsFile.write(str(stat) + '\n')

def runSimulation():

    mainMemory = Memory.MainMemory(config.getMainMemorySize(), None,
                                   config.getCache2MemBusSize(), config.getMainMemoryAccessTime())

    if config.getLevelsOfCache() == 1:
        l1Cache = Memory.Cache(config.getL1MemorySize(), config.getBlockSizeForL1Cache(),
                               1, mainMemory, config.getL1HitTimeCycles(),
                               config.getCPUL1BusSize(), config.getL1AccessTime())
        l2Cache = None
    else:
        l2Cache = Memory.Cache(config.getL2MemorySize(), config.getBlockSizeForL2Cache(),
                               2, mainMemory, config.getL2HitTimeCycles(),
                               config.getL1L2BusSize(), config.getL2AccessTime())
        l1Cache = Memory.Cache(config.getL1MemorySize(), config.getBlockSizeForL1Cache(),
                               1, l2Cache, config.getL1HitTimeCycles(),
                               config.getCPUL1BusSize(), config.getL1AccessTime())

    mainMemory.getMemoryDataFromFile(config.options.meminFilePath)

    totalNumberOfCycles = 0
    with open(config.getTraceFilePath()) as traceFile:
        for line in traceFile:
            if 'S' in line:
                numberOfCyclesBeforeCmd, dstMemoryAddressStr, dataToStore = ParsingUtils.parseStoreLineIntoStoreVariables(line)  
                l1Cache.writeData(dataToStore, dstMemoryAddressStr)  
    
            if 'L' in line:
                numberOfCyclesBeforeCmd, srcMemoryAddressStr = ParsingUtils.parseLoadLineIntoStoreVariables(line)
                l1Cache.readData(srcMemoryAddressStr, 4) 
    
            totalNumberOfCycles += int(numberOfCyclesBeforeCmd) 
    statResults = sumStatResults(totalNumberOfCycles, mainMemory, l1Cache, l2Cache)
    saveSimulationResultsToFiles(mainMemory, l1Cache, l2Cache, statResults)
    print 'DONE'

if __name__ == "__main__":
    try:
        config.options = config.getCmdLineOptions()
    except AssertionError as e:
        print(e.message)
        sys.exit(1)

    runSimulation()
