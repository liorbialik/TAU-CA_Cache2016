import config

class Memory:

    def __init__(self, size, block_size):
        self._size = config.mainMemorySize
        self._block_size = block_size  # Block size
        self._data = [0 for i in range(size)]


    def readInputMemoryStatus(self):
        with open(config.getMemoryStatusInputFilePath(), 'r') as mainMemoryStatus:
            # TODO: how to initiate the memory? to hexa or decimal?
            pass