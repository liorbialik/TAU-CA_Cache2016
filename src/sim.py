import sys
import Memory
import config
from utils import Utils


def saveSimulationResultsToFiles(mainMemory, l1Cache, l2Cache, statResults):
    """
    Saves the current snapshot the memory hierarchy into default files
    :param mainMemory:
    :param l1Cache:
    :param l2Cache:
    :param statResults:
    :return: None
    """
    mainMemory.saveMemoryToFile(config.getMainMemoryStatusOutputFilePath())
    l1Cache.saveMemoryToFile(config.getL1CacheStatusOutputFilePath())
    if l2Cache:
        l2Cache.saveMemoryToFile(config.getL2Way0CacheStatusOutputFilePath())
        l2Cache.saveMemoryToFile(config.getL2Way1CacheStatusOutputFilePath())

    with open(config.getStatsFileName(), 'w') as statsFile:
        for stat in statResults:
            statsFile.write(str(stat) + '\n')


def runSimulation():
    """
    the reading the the input trace file and execution of the commands in the given cache-memory scheme.
    :return: None
    """
    print("Beginning Simulation!\n")
    mainMemory = Memory.MainMemory("Main Memory", config.getMainMemorySize(), None,
                                   config.getCache2MemBusSize(), config.getMainMemoryAccessTime())

    if config.getLevelsOfCache() == 1:
        l1Cache = Memory.Cache("L1 Cache", config.getL1MemorySize(), config.getBlockSizeForL1Cache(),
                               1, mainMemory, config.getL1HitTimeCycles(),
                               config.getCPUL1BusSize(), config.getL1AccessTime())
        l2Cache = None
    else:
        l2Cache = Memory.Cache("L2 Cache", config.getL2MemorySize(), config.getBlockSizeForL2Cache(),
                               2, mainMemory, config.getL2HitTimeCycles(),
                               config.getL1L2BusSize(), config.getL2AccessTime())
        l1Cache = Memory.Cache("L1 Cache", config.getL1MemorySize(), config.getBlockSizeForL1Cache(),
                               1, l2Cache, config.getL1HitTimeCycles(),
                               config.getCPUL1BusSize(), config.getL1AccessTime())

    mainMemory.getMemoryDataFromFile(config.options.meminFilePath)

    totalNumberOfCycles = 0
    with open(config.getTraceFilePath()) as traceFile:
        for line in traceFile:
            print("Parsing current command line:" + line)
            if 'S' in line:
                numberOfCyclesBeforeCmd, dstMemoryAddressStr, dataToStore = Utils.parseStoreCmd(line)
                print("executing Store command to address %s with data: %s" % (str(dstMemoryAddressStr), str(dataToStore)))
                l1Cache.writeData(dataToStore, dstMemoryAddressStr)

            else:
                numberOfCyclesBeforeCmd, srcMemoryAddressStr = Utils.parseLoadCmd(line)
                print("executing Load command from address: %s" % str(srcMemoryAddressStr))
                l1Cache.readData(srcMemoryAddressStr, 4)

            totalNumberOfCycles += int(numberOfCyclesBeforeCmd) 
            print("\n\n")
    statResults = Utils.sumStatResults(totalNumberOfCycles, mainMemory, l1Cache, l2Cache)
    saveSimulationResultsToFiles(mainMemory, l1Cache, l2Cache, statResults)
    print 'DONE'


def main():
    try:
        config.options = config.getCmdLineOptions()
    except AssertionError as e:
        print(e.message)
        sys.exit(1)

    runSimulation()

if __name__ == "__main__":
    main()
