import sys
import config
import Memory
from Utils import ParsingUtils  # MemoryUtils


def runSimulation():

    mainMemory = Memory.MainMemory()

    if config.getLevelsOfCache() == 1:
        l1Cache = Memory.Cache(config.L1MemorySize, config.getBlockSizeForL1Cache(),
                               1, mainMemory)
    if config.getLevelsOfCache() == 2:
        l2Cache = Memory.Cache(config.L2MemorySize, config.getBlockSizeForL2Cache(),
                               2, mainMemory)
        l1Cache = Memory.Cache(config.L1MemorySize, config.getBlockSizeForL1Cache(),
                               1, l2Cache)

    mainMemory.getMemoryDataFromFile(config.options.meminFilePath)
    # # init caches (depending on levels)
    # totalNumberOfCycles = 0
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
    #         totalNumberOfCycles += numberOfCyclesBeforeCmd  # + numberOfCycles
    #
    # # print main memory final status into 'memout' file
    # # print l1 cache  memory final status into file
    # # print l2 cache  memory final status into ***2*** files
    # # print Stats

if __name__ == "__main__":
    try:
        config.options = config.getCmdLineOptions()
    except AssertionError as e:
        print(e.message)
        sys.exit(1)

    runSimulation()
