import sys
import config
import Memory
from Utils import ParsingUtils, MemoryUtils


def runSimulation():
    mainMemory = Memory.MainMemory()
    mainMemory.getMemoryDataFromFile(config.options.meminFilePath)
    pass
#     totalNumberOfCommands = 0
#     with open(config.getTraceFilePath()) as traceFile:
#         for line in traceFile:
#             if 'S' in line:
#                 numberOfCommands, dstMemoryAddressStr, dataToStore = ParsingUtils.parseStoreLineIntoStoreVariables(line)  # TODO: do we need this?
#                 numberOfCycles = MemoryUtils.storeData(dstMemoryAddressStr, dataToStore)  # TODO: need to  think of the right way to execute
# 
#             if 'L' in line:
#                 numberOfCommands, srcMemoryAddressStr = ParsingUtils.parseLoadLineIntoStoreVariables(line)
#                 numberOfCycles = MemoryUtils.loadData(srcMemoryAddressStr)  # TODO: need to  think of the right way to execute
#             
#             totalNumberOfCommands += numberOfCommands + numberOfCycles


if __name__ == "__main__":
    try:
        config.options = config.getCmdLineOptions()
    except AssertionError as e:
        print(e.message)
        sys.exit(1)
    
    config.L1BlockSize = config.L1BlockSizes[0]
    config.L2BlockSize = config.L2BlockSizes[0]
    runSimulation()
            