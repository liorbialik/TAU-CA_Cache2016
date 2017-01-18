import sys
import Memory
import config


def saveSimulationResultsToFiles(mainMemory, l1Cache, l2Cache):
    mainMemory.saveMemoryToFile(config.getMainMemoryStatusOutputFilePath())
    l1Cache.saveMemoryToFile(config.getL1CacheStatusOutputFilePath())
    if l2Cache:
        l2Cache.saveMemoryToFile(config.getL2Way0CacheStatusOutputFilePath())
        l2Cache.saveMemoryToFile(config.getL2Way1CacheStatusOutputFilePath())

    with open(config.getStatsFileName(), 'w') as statsFile:
        # program running cycles
        statsFile.write(str(l1Cache.readHits) + "\n")
        statsFile.write(str(l1Cache.writeHits) + "\n")
        statsFile.write(str(l1Cache.readMisses) + "\n")
        statsFile.write(str(l1Cache.writeMisses) + "\n")
        statsFile.write(str(l2Cache.readHits) + "\n")
        statsFile.write(str(l2Cache.writeHits) + "\n")
        statsFile.write(str(l2Cache.readMisses) + "\n")
        statsFile.write(str(l2Cache.writeMisses) + "\n")
        # L1 local miss rate
        # global miss rate
        # AMAT

def runSimulation():

    mainMemory = Memory.MainMemory(config.getMainMemorySize(), )

    if config.getLevelsOfCache() == 1:
        l1Cache = Memory.Cache(config.getL1MemorySize(), config.getBlockSizeForL1Cache(),
                               1, mainMemory)
        l2Cache = None
    else:
        l2Cache = Memory.Cache(config.getL2MemorySize(), config.getBlockSizeForL2Cache(),
                               2, mainMemory)
        l1Cache = Memory.Cache(config.getL1MemorySize(), config.getBlockSizeForL1Cache(),
                               1, l2Cache)

    mainMemory.getMemoryDataFromFile(config.options.meminFilePath)

    #totalNumberOfCycles = 0
    # with open(config.getTraceFilePath()) as traceFile:
    #     for line in traceFile:
    #         if 'S' in line:
    #             numberOfCyclesBeforeCmd, dstMemoryAddressStr, dataToStore = ParsingUtils.parseStoreLineIntoStoreVariables(line)  # TODO: do we need this?
    #             # numberOfCycles = MemoryUtils.storeData(dstMemoryAddressStr, dataToStore)  # TODO: need to  think of the right way to execute
    #
    #         if 'L' in line:
    #             numberOfCyclesBeforeCmd, srcMemoryAddressStr = ParsingUtils.parseLoadLineIntoStoreVariables(line)
    #             # numberOfCycles = MemoryUtils.loadData(srcMemoryAddressStr)  # TODO: need to  think of the right way to execute
    #
    #         # totalNumberOfCycles += numberOfCyclesBeforeCmd  # + numberOfCycles

    saveSimulationResultsToFiles(mainMemory, l1Cache, l2Cache)


if __name__ == "__main__":
    try:
        config.options = config.getCmdLineOptions()
    except AssertionError as e:
        print(e.message)
        sys.exit(1)

    runSimulation()
