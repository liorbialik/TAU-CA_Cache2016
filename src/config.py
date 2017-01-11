import argparse
import os


validL1BlockSizes = [2, 4, 8, 16, 32, 64, 128]
validL2BlockSizes = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

# Memory Magics
mainMemorySize = 16777216  # Bytes
L1MemorySize = 4098  # Bytes
L2MemorySize = 32784  # Bytes
L1HitTimeCycles = 1
L2HitTimeCycles = 4
MemoryAccessTime = 100
secondaryMemoryAccessTime = 1

CPUL1DataBusSize = 32  # bits
CPUL1AddressBusSize = 24  # bits
L1L2BusSize = 256  # bits
L1MemBusSize = 64  # bits - if not running with L2
L2MemBusSize = 64  # bits - if running with L2

options = None


def assertOptionsInit():
    assert options is not None, "options not initialized yet"


def getCmdLineOptions():
    parser = argparse.ArgumentParser(description='Cache Simulation')

    parser.add_argument('levels',
                        type=assertValidLevels,
                        help='The levels of cache to use:\n 1 level is for L1 only.\n 2 levels is for both L1 and L2')
    parser.add_argument('b1',
                        type=assertValidL1BlockSize,
                        help='The cache block size in decimal for L1')
    parser.add_argument('b2',
                        type=assertValidL2BlockSize,
                        help='The cache block size in decimal for L2. only relevant if levels is 2')
    parser.add_argument('traceFilePath',
                        type=assertFileExists,
                        default="trace.txt",
                        help='The path to the trace file')
    parser.add_argument('meminFilePath',
                        type=assertFileExists,
                        default="memin.txt",
                        help='The path to the memin file which contains the main memory\'s status before a run')
    parser.add_argument('memoutFilePath',
                        default="memout.txt",
                        help='The path to the memout file which contains the main memory\'s status after a run')
    parser.add_argument('L1_memoutFilePath',
                        default="l1.txt",
                        help='The path to the file which contains the L1 cache memory\'s status after a run')
    parser.add_argument('L2_Way0_memoutFilePath',
                        default="l2way0.txt",
                        help='The path to the file which contains the L2, way 0 cache memory\'s status after a run')
    parser.add_argument('L2_Way1_memoutFilePath',
                        default="l2way1.txt",
                        help='The path to the file which contains the L2, way 1 cache memory\'s status after a run')
    parser.add_argument('statsFilePath',
                        default="stats.txt",
                        help='The path to the stats file which contains the running stats after a run')

    cmdLineOptions = parser.parse_args()

    return cmdLineOptions


def assertValidLevels(level):
    assert int(level) in [1, 2], "Wrong number of levels received"
    return int(level)


def assertFileExists(filePath):
    assert os.path.isfile(filePath), "Trace file %s does not exist!" % filePath
    return filePath


def assertValidL1BlockSize(blockSize):
    assert blockSize.isdigit(), "Block size has to be an integer!"
    assert blockSize in validL1BlockSizes, "L1 Block size is not in allowed scope!"
    return int(blockSize)

def assertValidL2BlockSize(blockSize):
    assert blockSize.isdigit(), "Block size has to be an integer!"
    assert blockSize in validL2BlockSizes, "L2 Block size is not in allowed scope!"
    return int(blockSize)


def getLevelsOfCache():
    assertOptionsInit()
    return int(options.levels)


def getBlockSizeForL1Cache():
    assertOptionsInit()
    return options.b1


def getBlockSizeForL2Cache():
    assertOptionsInit()
    return options.b2


def getTraceFilePath():
    assertOptionsInit()
    return options.traceFilePath


def getMemoryStatusInputFilePath():
    assertOptionsInit()
    return options.meminFilePath


def getMainMemoryStatusOutputFilePath():
    assertOptionsInit()
    return options.memoutFilePath


def getL1CacheStatusOutputFilePath():
    assertOptionsInit()
    return options.L1_memoutFilePath


def getL2Way0CacheStatusOutputFilePath():
    assertOptionsInit()
    return options.L2_Way0_memoutFilePath


def getL2Way1CacheStatusOutputFilePath():
    assertOptionsInit()
    return options.L2_Way1_memoutFilePath


def getStatsFilePath():
    assertOptionsInit()
    return options.statsFilePath
