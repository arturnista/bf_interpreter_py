import sys

# Verify if a filename was entered
if(len(sys.argv) < 2):
    print("Please, enter the file name!")
    exit(1)

# Open the .bf file
filename = sys.argv[1]
if(".bf" not in filename):
    filename += ".bf"

f = open(filename, "r")
code = f.read()

# Prepare split code data
codeData = list(code)
codeLength = len(codeData)
codeIndex = 0

# Data
arrayData = [ 0 ]
ptr = 0

# Loop queue
loop = []

# Process the code
while codeIndex < codeLength:
    currentCommand = codeData[codeIndex]
    if(currentCommand == '.'): # Print
        print(chr(arrayData[ptr]), end = '')
    elif(currentCommand == ','): # Accept (nop)
        accepted = input()
        if(len(accepted) > 0):
            arrayData[ptr] = ord(accepted)
        else:
            arrayData[ptr] = 10
    elif(currentCommand == '+'): # Increment
        arrayData[ptr] += 1
        if(arrayData[ptr] > 255):
            arrayData[ptr] = 0
    elif(currentCommand == '-'): # Decrement
        arrayData[ptr] -= 1
        if(arrayData[ptr] < 0):
            arrayData[ptr] = 255
    elif(currentCommand == '>'): # Next memory
        ptr += 1
        # If new memory index is accessed, create the new memory
        if(len(arrayData) >= ptr):
            arrayData.append(0)
    elif(currentCommand == '<'): # Previous memory
        ptr -= 1
        # If access a new memory before last, create a new memory in the beginning
        if(ptr < 0):
            ptr = 0
            arrayData.insert(0, 0)
    elif(currentCommand == '['):
        if(arrayData[ptr] != 0):
            loop.append(codeIndex)
        else:
            # Find end of the loop
            loopLookAhead = []
            codeIndex += 1
            while True:
                if(codeData[codeIndex] == '['):
                    loopLookAhead.append(codeIndex)
                elif(codeData[codeIndex] == ']'):
                    if(len(loopLookAhead) == 0):
                        break
                    else:
                        loopLookAhead.pop()
                codeIndex += 1
    elif(currentCommand == ']'):
        loopCodeIndex = loop.pop()
        if(arrayData[ptr] != 0):
            codeIndex = loopCodeIndex - 1
    else:  # Comment
        pass

    codeIndex += 1
