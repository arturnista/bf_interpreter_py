import sys

MIN_VALUE = 0
MAX_VALUE = 255

# Read filename from args
def getFilenameEntered():
    # Verify if a filename was entered
    if(len(sys.argv) < 2):
        print("Please, enter the file name!")
        exit(1)

    # Open the .bf file
    filename = sys.argv[1]
    if(".bf" not in filename):
        filename += ".bf"

    return filename

# Read code file
def readCode(filename):
    f = open(filename, "r")
    code = f.read()

    # Split the commands
    codeData = list(code)
    codeIndex = 0

    # Cleans code, removing comments
    availableCommands = ['.', ',', '+', '-', '>', '<', '[', ']']
    while codeIndex < len(codeData):
        if(codeData[codeIndex] not in availableCommands):
            del codeData[codeIndex]
        else:
            codeIndex += 1

    return codeData

# Cache start and ending loop positions
def cacheLoopData(codeData):
    loop = []
    cache = {}

    codeLength = len(codeData)

    for i in range(codeLength):
        currentCommand = codeData[i]
        if(currentCommand == '['):
            loop.append(i)
        elif(currentCommand == ']'):
            if(len(loop) == 0):
                print("Syntax error!\n']' at position " +
                    str(i) + " has no matching '['.")
                exit(1)

            index = loop.pop()
            cache[index] = i

    if(len(loop) > 0):
        print("Syntax error!\n'[' at position " +
            str(loop[0]) + " has no matching ']'.")
        exit(1)

    return cache

def main():
    # Get filaname
    filename = getFilenameEntered()

    # Get the code data
    codeData = readCode(filename)
    codeLength = len(codeData)
    codeIndex = 0

    # "Memeory" Data
    arrayData = [0]
    ptr = 0

    # Loop queue
    loop = []
    loopCache = cacheLoopData(codeData)

    # Process the code
    while codeIndex < codeLength:

        # Get current command
        currentCommand = codeData[codeIndex]

        if(currentCommand == '+'):  # Increment
            arrayData[ptr] += 1
            if(arrayData[ptr] > MAX_VALUE):
                arrayData[ptr] = MIN_VALUE

        elif(currentCommand == '-'):  # Decrement
            arrayData[ptr] -= 1
            if(arrayData[ptr] < MIN_VALUE):
                arrayData[ptr] = MAX_VALUE

        elif(currentCommand == '>'):  # Next memory
            ptr += 1
            # If new memory index is accessed, create the new memory position
            if(len(arrayData) >= ptr):
                arrayData.append(0)

        elif(currentCommand == '<'):  # Previous memory
            ptr -= 1
            # If access a new memory before last, create a new memory in the beginning
            if(ptr < 0):
                ptr = 0
                arrayData.insert(0, 0)

        elif(currentCommand == '['): # Start loop
            if(arrayData[ptr] != 0):
                loop.append(codeIndex)
            else:
                codeIndex = loopCache[codeIndex]

        elif(currentCommand == ']'): # End loop
            loopCodeIndex = loop.pop()
            if(arrayData[ptr] != 0):
                codeIndex = loopCodeIndex - 1

        elif(currentCommand == '.'):  # Print
            print(chr(arrayData[ptr]), end='')

        elif(currentCommand == ','):  # Accept
            accepted = input()
            if(len(accepted) > 0):
                arrayData[ptr] = ord(accepted)
            else:
                arrayData[ptr] = 10

        else:  # Comment
            pass

        codeIndex += 1


if(__name__ == "__main__"):
    main()
