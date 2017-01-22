import random

NUMBER_OF_COMMANDS = 50000

def generateHexNumber(length):
    return ''.join([random.choice('0123456789ABCDEF') for x in range(length)]).zfill(6)

def generateCommandsNumber():
    return random.randint(1, 100)

command = ['L', 'S']

with open("trace.txt", 'w') as traceFile:
    for i in range(NUMBER_OF_COMMANDS):
        loadStoreVal = random.choice(command)
        traceLine = "{commandsNumber} {loadStore} {memoryAddress}{dataToWrite}\n".format(commandsNumber=generateCommandsNumber(),
                                                                                         loadStore=loadStoreVal,
                                                                                         memoryAddress=generateHexNumber(6),
                                                                                         dataToWrite=' ' + generateHexNumber(8) if loadStoreVal is 'S' else '')
        traceFile.write(traceLine)

traceFile.close()