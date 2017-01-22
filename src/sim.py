import sys
import Memory
import config
from utils import Utils
import time
import matplotlib.pyplot as plt

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
                l1Cache.readData(srcMemoryAddressStr, config.getWordSize())

            totalNumberOfCycles += int(numberOfCyclesBeforeCmd) 
            print("\n\n")
    statResults = Utils.sumStatResults(totalNumberOfCycles, mainMemory, l1Cache, l2Cache)
    saveSimulationResultsToFiles(mainMemory, l1Cache, l2Cache, statResults)
    print 'DONE'
    return statResults

def graph1ForTestTrace():
    L1MissRate = []
    for blockSize in config.validL1BlockSizes:
        config.options.b1 = blockSize
        simulationResults = runSimulation()
        L1MissRate.append(simulationResults[-3])
    plt.plot(config.validL1BlockSizes, L1MissRate, 'g^')
    plt.title("L1 Miss Rate relative to the block size")
    plt.xlabel("L1 Block Size [Bytes]")
    plt.ylabel("L1 Miss Rate")
    plt.show()

def graph2ForTestTrace():
    simulationRunningTimeList = []
    config.options.levels = 2
    config.options.b2 = 128
    for blockSize in config.validL1BlockSizes:
        config.options.b1 = blockSize
        # startTime = time.time()
        simulationResults = runSimulation()
        # simulationRunningTime = time.time() - startTime
        simulationRunningTimeList.append(simulationResults[0])
    plt.plot(config.validL1BlockSizes, simulationRunningTimeList, 'g^')
    plt.title("Simulation running time relative to L1 block size")
    plt.xlabel("L1 Block Size [Bytes]")
    plt.ylabel("Running Time [Cycles]")
    plt.show()

def graph3ForTestTrace():
    config.options.levels = 2
    config.options.b1 = 8
    amatList = []
    L2BlockSizes = [8, 16, 32, 64, 128, 256]
    for blockSize in L2BlockSizes:
        config.options.b2 = blockSize
        simulationResults = runSimulation()
        amatList.append(simulationResults[-1])
    plt.plot(L2BlockSizes, amatList, 'g^')
    plt.title("AMAT result relative to L2 block size")
    plt.xlabel("L2 Block Size [Bytes]")
    plt.ylabel("AMAT")
    plt.show()
    plt.show()

def main():
    try:
        config.options = config.getCmdLineOptions()
    except AssertionError as e:
        print(e.message)
        sys.exit(1)

#     graph1ForTestTrace()
#     graph2ForTestTrace()
#     graph3ForTestTrace()
    runSimulation()

if __name__ == "__main__":
    main()

