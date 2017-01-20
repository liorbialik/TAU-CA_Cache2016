import sys
import Memory
import config
from utils import Utils


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
                numberOfCyclesBeforeCmd, dstMemoryAddressStr, dataToStore = Utils.parseStoreLine(line)
                l1Cache.writeData(dataToStore, dstMemoryAddressStr)  
    
            else:
                numberOfCyclesBeforeCmd, srcMemoryAddressStr = Utils.parseLoadLine(line)
                l1Cache.readData(srcMemoryAddressStr, 4)
    
            totalNumberOfCycles += int(numberOfCyclesBeforeCmd) 
    statResults = Utils.sumStatResults(totalNumberOfCycles, mainMemory, l1Cache, l2Cache)
    saveSimulationResultsToFiles(mainMemory, l1Cache, l2Cache, statResults)
    print 'DONE'


if __name__ == "__main__":
    try:
        config.options = config.getCmdLineOptions()
    except AssertionError as e:
        print(e.message)
        sys.exit(1)

    runSimulation()
