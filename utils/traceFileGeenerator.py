import random

def generateHexNumber(length):
   return ''.join([random.choice('0123456789ABCDEF') for x in range(length)])

def generateCommandsNumber():
    return random.randint(1, 100)

command = ['L', 'S']

with open("trace.txt", 'w') as traceFile:
    for i in range(100):
        loadStoreVal = random.choice(command)
        traceLine = "{commandsNumber} {loadStore} {memoryAddress} {dataToWrite}\n".format(commandsNumber=generateCommandsNumber(),
                                                                                          loadStore=loadStoreVal,
                                                                                          memoryAddress=generateHexNumber(6),
                                                                                          dataToWrite=generateHexNumber(8) if loadStoreVal is 'S' else '')
        traceFile.write(traceLine)

