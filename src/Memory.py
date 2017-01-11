import config
import math

class MainMemory(object):
    '''
    this class will represent the main memmory
    '''

    memory = []
    
    def __init__(self):
        """
        initializing the memmory to zeros
        """
        self.memory = []
        self.outputLogFileName = config.getMainMemoryStatusOutputFilePath()

    def initializeMemoryToZero(self):
        self.memory = ['00' for i in range(config.mainMemorySize)]

    def getMemoryDataFromFile(self, meminFilePath):
        """
        fetching the initial main memory status from the memin file
        :param meminFilePath: the path to the memin.txt file
        :return: none
        """
        with open(meminFilePath, 'r') as memfile:
            i = 0
            for line in memfile.readlines():
                hexData = line.strip()
                if len(hexData) == 2:  # each line should be 1 Byte
                    try:
                        int(hexData, 16)  # if doesn't contain chars [0-9, a-f]
                        self.memory[i] = hexData
                    except:
                        if ValueError:
                            raise ValueError("memin file contains a bad line: " + hexData)
                        elif IndexError:
                            raise IndexError("memin file has data bigger than 16MB.")
                    i += 1
                else:
                    raise ValueError("memin file contains a bad line: " + hexData)

    def readDataFromAddress(self, address):
        NotImplementedError

    def writeDataFromAddress(self, address, data):
        NotImplementedError

    def saveMemoryToFile(self, dstPath):
        NotImplementedError

class Cache(object):
    def __init__(self, size, blockSize, cacheAssociativity, nextLevelMem):
        self.data = {}
        self.size = size
        self.blockSize = blockSize
        self.associativity = cacheAssociativity
        self.nextLevel = nextLevelMem
        self.numberOfSets = self.size / self.associativity
        self.offsetSize = int(math.log(self.blockSize, 2))
        self.indexSize = int(math.log(self.numberOfSets, 2))
        self.tagSize = config.addressSize - self.indexSize - self.offsetSize
        self.readHits = 0
        self.readMisses = 0
        self.writeHits = 0
        self.writeMisses = 0

    def readData(self, address):
        NotImplementedError

    def writeData(self, address, data):
        NotImplementedError

    def saveMemoryToFile(self, dstPath):
        NotImplementedError

class MemoryBlock(object):
    # https://github.com/lucianohgo/CacheSimulator/blob/master/src/block.py
    NotImplementedError
