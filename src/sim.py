import sys
import config
from Utils import ParsingUtils


def runSimulation(L1BlockSize, L2BlockSize):
    with open(config.getTraceFilePath()) as traceFile:
        for line in traceFile:
            if 'S' in line:
                numberOfCommands, dstMemoryAddressStr, dataToStore = ParsingUtils.parseStoreLineIntoStoreVariables(line)  # TODO: do we need this?
                # storeData(dstMemoryAddress, data)  # TODO: need to  think of the right way to execute

            if 'L' in line:
                numberOfCommands, srcMemoryAddressStr = ParsingUtils.parseLoadLineIntoStoreVariables(line)
                # loadData(dstMemoryAddress)  # TODO: need to  think of the right way to execute

if __name__ == "__main__":
    try:
        config.options = config.getCmdLineOptions()
    except AssertionError as e:
        print(e.message)
        sys.exit(1)
    runSimulation(config.L1BlockSize[0], config.L2BlockSize[0])  # TODO: in the future this will run in a loop for each block size
