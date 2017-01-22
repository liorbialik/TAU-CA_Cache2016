import random

NUMBER_OF_MEMORY_DATA = 3000

def generateHexNumber(length):
    return ''.join([random.choice('0123456789ABCDEF') for x in range(length)])

with open("memin.txt", 'w') as meminFile:
    for i in range(NUMBER_OF_MEMORY_DATA):
        if i > 0:
            meminFile.write("\n")
        meminFile.write(generateHexNumber(2))

meminFile.close()
