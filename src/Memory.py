import copy
import math
import config


class AbstractMemory(object):
    """
    This abstract class us used for inheritance by the main memory and
    the cache memory levels in order to have the same method names
    """
    TAB=''
    def __init__(self, name, size, nextLevelMem):
        self.name = name
        self.size = size
        self.nextLevel = nextLevelMem

    def initializeMemoryToZero(self):
        NotImplementedError

    def readData(self, addressInHex, blockSize):
        NotImplementedError

    def writeData(self, data, addressInHex):
        NotImplementedError

    def saveMemoryToFile(self, dstPath):
        NotImplementedError

    def getBlockLocations(self, addressInInt, blockSize):
        """
        gets the location of the relevant block in the level of the memory
        :param addressInInt: the address of the block we are looking for
        :param blockSize: the size of the memory's block
        :return addressBlockStartPos, addressBlockEndPos: the beginning and end of the wanted address
        """
        addressBlockStartPos = addressInInt - (addressInInt % blockSize)
        addressBlockEndPos = addressBlockStartPos + blockSize
        return addressBlockStartPos, addressBlockEndPos

class MainMemory(AbstractMemory):
    '''
    this class will represent the main memmory
    '''

    memory = []
    
    def __init__(self, name, size, nextLevelMem, busSizeToPrevLevel, accessTime):
        """
        initializing the memmory to the input of the program
        """
        super(MainMemory, self).__init__(name, size, nextLevelMem)
        self.memory = []
        self.name = name
        self.size = size
        self.outputLogFileName = config.getMainMemoryStatusOutputFilePath()
        self.initializeMemoryToZero()
        self.nextLevel = nextLevelMem
        self.busSizeToPrevLevel = busSizeToPrevLevel
        self.accessTime = accessTime
        self.reads = 0
        self.writes = 0

    def initializeMemoryToZero(self):
        """
        Setting all the memory addresses to zeros
        :return: None
        """
        print("initializing %s to zero" % self.name)
        self.memory = ['00' for i in range(self.size)]

    def getMemoryDataFromFile(self, meminFilePath):
        """
        fetching the initial main memory status from the memin file
        :param meminFilePath: the path to the memin.txt file
        :return: none
        """
        print("loading the memory data from %s into the main memory" % meminFilePath)
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
    
    def getTotalActualAccessTime(self, BlockSize):
        """
        Calculate the access time took for a main memory access
        :param BlockSize: the block size of the higher memory level
        :return totalAccessTime: the result
        """
        busSize = self.busSizeToPrevLevel
        blockToBusSizeFactor = int(math.ceil(1.0*BlockSize/busSize))
        print "{name} blockToBusSizeFactor = {b}".format(name=self.name, b=blockToBusSizeFactor)
        print "mainMemory reads:", self.reads, "writes:", self.writes
        singleAccessTime = self.accessTime + blockToBusSizeFactor-1
        totalAccessTime = (self.reads + self.writes) * singleAccessTime
        return totalAccessTime

    def readData(self, addressInHex, blockSize):
        """
        returns the relevant block of data
        :param addressInHex: the desired address as string
        :param blockSize: the block size of the cache that asks to load the desired data
        :return: the desired block of data
        """
        self.reads += 1
        print AbstractMemory.TAB + "***** +1 mainMemory read"
        addressInInt = int(addressInHex, 16)
        addressBlockStartPos, addressBlockEndPos = self.getBlockLocations(addressInInt, blockSize)
        return self.memory[addressBlockStartPos:addressBlockEndPos]

    def writeData(self, data, addressInHex):
        """
        writes the relevant block of data to Main memory
        :param data: the desired data as array of strings
        :param addressInHex: the relevant address as string
        :return: None
        """
        self.writes += 1
        print AbstractMemory.TAB + "***** +1 mainMemory write"
        addressInInt = int(addressInHex, 16)
        blockSize = len(data)
        addressBlockStartPos, addressBlockEndPos = self.getBlockLocations(addressInInt, blockSize)
        self.memory[addressBlockStartPos:addressBlockEndPos] = data
        print AbstractMemory.TAB+"mainMemory was updated at position [{start}:{end}] with {Data}".format(Data=data, start=addressBlockStartPos, end=addressBlockEndPos)
        return

    def saveMemoryToFile(self, dstPath):
        """
        save the memory status into an output file
        :param dstPath:
        :return:
        """
        with open(dstPath, 'w') as memoutFile:
            for i in range(self.size):
                memoutFile.write(self.memory[i] + "\n")
            memoutFile.close()


class Cache(AbstractMemory):
    """
    this class will represent the cache memmory of L1 (and L2 if present)
    """

    def __init__(self, name, size, blockSize, cacheAssociativity, nextLevelMem, hitTimeCycles, busSizeToPrevLevel, accessTime):
        super(Cache, self).__init__(name, size, nextLevelMem)
        self.data = []
        self.name = name
        self.size = size
        self.blockSize = blockSize
        self.associativity = cacheAssociativity
        self.nextLevel = nextLevelMem
        self.numberOfBlocks = self.size / self.blockSize
        self.numberOfSets = self.numberOfBlocks / self.associativity
        self.offsetSize = int(math.log(self.blockSize, 2))
        self.indexSize = int(math.log(self.numberOfSets, 2))
        self.tagSize = 8*config.addressSize - self.indexSize - self.offsetSize
        self.readHits = 0
        self.readMisses = 0
        self.writeHits = 0
        self.writeMisses = 0
        self.hitTimeCycles = hitTimeCycles
        self.busSizeToPrevLevel = busSizeToPrevLevel
        self.accessTime = accessTime
        self.initializeMemoryToZero()

    def initializeMemoryToZero(self):
        """
        Setting all the memory blocks and their respected values to zeros
        :return: None
        """
        print("initializing %s to zero" % self.name)
        wayDict = {'dirty': False,
                   'valid': False,
                   'tag': '-1',
                   'data': ['00' for i in range(self.blockSize)]}
        indexDict = {'way'+str(num): copy.deepcopy(wayDict) for num in range(self.associativity)}
        indexDict['LRU'] = 'way0'
        self.data = [copy.deepcopy(indexDict) for i in range(self.numberOfSets)]
    
    def getTotalActualAccessTime(self, BlockSize):
        """
        Calculate the access time took for a cache memory access
        :param BlockSize: the block size of the higher memory level
        :return totalAccessTime: the result
        """
        busSize = self.busSizeToPrevLevel
        blockToBusSizeFactor = int(math.ceil(1.0*BlockSize/busSize))
        print "{name} blockToBusSizeFactor = {b}".format(name=self.name, b=blockToBusSizeFactor)
        singleAccessTime = self.accessTime * blockToBusSizeFactor
        totalAccessTime = (self.readHits + self.writeHits
                           + self.readMisses + self.writeMisses) * singleAccessTime
        return totalAccessTime

    def otherWay(self, way):
        """
        :param way: current way of cache
        :return: the other way
        """
        if way == 'way0':
            return 'way1'
        return 'way0'

    def lookForAddressInCache(self, indexInInt, tagInBinary):
        """
        Searched the cache for the given address to check for a hit and re-set the LRU
        :param indexInInt: index value of the address
        :param tagInBinary: tag value of the address
        :return hit: whether the it was a hit or not
        :return _set['LRU']: the new way of the LRU field
        """
        hit = False
        _set = self.data[indexInInt]
        for way in [key for key in _set.keys() if 'way' in key]:
            if _set[way]['tag'] == tagInBinary and _set[way]['valid']:
                print("HIT!")
                hit = True
                return hit, way
        print("MISS!")
        return hit, _set['LRU']
    
    def calcAddressOfBlockInHex(self, indexInInt, tagInBinary):
        """
        calculated the address of the given block in hexadecimal numbering
        :param indexInInt:
        :param tagInBinary:
        :return addressInHex:
        """
        addressInBinary = (tagInBinary + bin(indexInInt)[2:].zfill(self.indexSize)).ljust(8*config.addressSize, '0')
        addressInHex = hex(int(addressInBinary, 2))[2:]
        return addressInHex
              
    def writeData(self, data, addressInHex):
        """
        writes the relevant block of data to the cache memory and if needed the next level in the hierarchy.
        updates all the relevant field accordingly
        :param data: the desired data as array of strings
        :param addressInHex: the relevant address as string
        :return: None
        """
        offsetInInt, indexInInt, tagInBinary = self.parseHexAddress(addressInHex)
        print AbstractMemory.TAB+"trying to write data to {name} from address:{addr} at index:{i}, tag:{t}...".format(name=self.name, addr=addressInHex.zfill(6), i=indexInInt, t=tagInBinary),
        hit, way = self.lookForAddressInCache(indexInInt, tagInBinary) # way will be the found way or what's in LRU if not found
        if hit:
            self.writeHits += 1
        else:
            print AbstractMemory.TAB+"writing data to {cur} from {next}".format(cur=self.name, next=self.nextLevel.name)
            AbstractMemory.TAB+='\t'
            self.writeMisses += 1
            if self.data[indexInInt][way]['dirty']:
                self.performWriteBack(indexInInt, way)
            self.data[indexInInt][way]['data'] = self.nextLevel.readData(addressInHex, self.blockSize)
            AbstractMemory.TAB = AbstractMemory.TAB[:-1]
        offsetBlockStartPos, offsetBlockEndPos = self.getBlockLocations(offsetInInt, len(data))
        self.data[indexInInt][way]['data'][offsetBlockStartPos:offsetBlockEndPos] = data
        self.data[indexInInt][way]['dirty'] = True
        print AbstractMemory.TAB+"data was written to {name}. dirtyBit:True".format(name=self.name)
        self.data[indexInInt][way]['valid'] = True
        self.data[indexInInt][way]['tag'] = tagInBinary
        self.updateLRU(indexInInt, way)

    def readData(self, addressInHex, blockSize):
        """
        read the relevant block of data into the cache memory and updates all the relevant field accordingly.
        :param blockSize: the size of the block to read (might be given by a higher level of cache)
        :param addressInHex: the relevant address as string
        :return: None
        """
        offsetInInt, indexInInt, tagInBinary = self.parseHexAddress(addressInHex)
        print AbstractMemory.TAB+"trying to read data to {name} from address:{addr} at index:{i}, tag:{t}...".format(name=self.name, addr=addressInHex.zfill(6), i=indexInInt, t=tagInBinary),
        hit, way = self.lookForAddressInCache(indexInInt, tagInBinary)
        if hit:
            self.readHits += 1
        else:
            print AbstractMemory.TAB+"reading data to {cur} from {next}".format(cur=self.name, next=self.nextLevel.name)
            AbstractMemory.TAB+='\t'
            self.readMisses += 1
            if self.data[indexInInt][way]['dirty']:
                self.performWriteBack(indexInInt, way)
            self.data[indexInInt][way]['data'] = self.nextLevel.readData(addressInHex, self.blockSize)
            AbstractMemory.TAB = AbstractMemory.TAB[:-1]
            self.data[indexInInt][way]['dirty'] = False
            print AbstractMemory.TAB+"data was written to {name}. dirtyBit:False".format(name=self.name)
            self.data[indexInInt][way]['valid'] = True
            self.data[indexInInt][way]['tag'] = tagInBinary
        self.updateLRU(indexInInt, way)
        offsetBlockStartPos, offsetBlockEndPos = self.getBlockLocations(offsetInInt, blockSize)
        return self.data[indexInInt][way]['data'][offsetBlockStartPos:offsetBlockEndPos]

    def performWriteBack(self, indexInInt, way):
        """
        preforming writeback in case of a 'on' dirty bit
        :param indexInInt:
        :param way:
        :return: None
        """
        blockAddressInHex = self.calcAddressOfBlockInHex(indexInInt, self.data[indexInInt][way]['tag'])
        print(AbstractMemory.TAB+"Performing writeback of address:{addr} from {cur} to {next}".format(addr=blockAddressInHex.upper(), cur=self.name, next=self.nextLevel.name))
        AbstractMemory.TAB+='\t'
        self.nextLevel.writeData(self.data[indexInInt][way]['data'], blockAddressInHex)
        AbstractMemory.TAB=AbstractMemory.TAB[:-1]
        print(AbstractMemory.TAB+"Ended writeback of {name}".format(name=self.name))

    def updateLRU(self, indexInInt, way):
        """
        preforming an update to the LRU field of the given index
        :param indexInInt:
        :param way:
        :return: None
        """
        if self.associativity == 2:
            self.data[indexInInt]['LRU'] = self.otherWay(way)
            print(AbstractMemory.TAB+"Updating LRU in {name} to {w}".format(name=self.name, w=self.data[indexInInt]['LRU']))

    def saveMemoryToFile(self, dstPath):
        """
        save a cache memory single way status into an output file
        :param dstPath:
        :return:
        """
        print("saving memory status of %s into the output file %s" % (self.name, dstPath))
        if 'way1' in dstPath:
            way = 'way1'
        else:
            way = 'way0'
        with open(dstPath, 'w') as memoutFile:
            for line in self.data:
                memoutFile.write('\n'.join(line[way]['data']) + "\n")
            memoutFile.close()

    def parseHexAddress(self, addressInHex):
        """
        parsing the address in hex
        :param addressInHex:
        :return offset, index, tag:
        """
        addressInBinary = bin(int(addressInHex, 16))[2:].zfill(8*config.addressSize)
        offset = addressInBinary[-self.offsetSize:]
        index = addressInBinary[-(self.offsetSize + self.indexSize):-self.offsetSize]
        if index == '':
            index = '0'
        tag = addressInBinary[:-(self.offsetSize + self.indexSize)]
        return int(offset, 2), int(index, 2), tag
