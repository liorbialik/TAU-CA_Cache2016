import config

DEFAULT_MAIN_MEMORY_SIZE = 16777216

class MainMemory(object):
    '''
    ******description
    :param
    :return
    '''

    memory = []
    
    def __init__(self):
        self.memory = ['00' for x in range(DEFAULT_MAIN_MEMORY_SIZE)]
    
    def getMemoryDataFromFile(self, meminFilePath):
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

class L1Cache(object):
    def __init__(self):
        self.size = NotImplementedError # get size
        self.blockSize = NotImplementedError #get block size
        self.nextLevel = None  # TODO: create function: getNextLevel and get the level from options

    def readData(self, address):
        NotImplementedError

    def writeData(self, address, data):
        NotImplementedError

    def saveMemoryToFile(self, dstPath):
        NotImplementedError

class L2Cache(object):
    def __init__(self):
        self.size = NotImplementedError # get size
        self.blockSize = NotImplementedError #get block size
        self.nextLevel = None  # TODO: need to define that the next level is main memory

    def readData(self, address):
        NotImplementedError

    def writeData(self, address, data):
        NotImplementedError

    def saveMemoryToFile(self, dstPath):
        NotImplementedError

class MemoryBlock(object):
    # https://github.com/lucianohgo/CacheSimulator/blob/master/src/block.py
    NotImplementedError
