import matplotlib.pyplot as plt
import re

def readFile(fileName):
    return open(fileName).read()

def splitNewLine(text):
    output = []
    split = text.split("\n")
    del split[-1]
    for s in split:
        output.append(float(s))

    return output

def findRewLines(data):
    liney = data.split("\n")
    output = []
    for d in liney:
        if re.search("reward of", d):
            output.append(d)
    return output

def getRewards(data):
    rewards = []
    for d in data:
        first = (re.search("reward of ", d)).span()[1]
        last = (re.search(",", d[first:])).span()[0]
        rewards.append(float(d[first:first+last]))
    return rewards

def findMaxVal(data):
    return max(data)

def findMinVal(data):
    return min(data)

def removeExtremes(data):
    output = []
    for d in data:
        if d > 15000:
            output.append(15000)
        elif d < - 5000:
            output.append(-5000)
        else:
            output.append(d)
    return output

def plotter(data):
    plt.plot(data)
    plt.ylabel("Backpropagation")
    plt.show()

filey = readFile("C:/Users/Martin/Desktop/tempFile.txt")
rewLines = findRewLines(filey)
rew = getRewards(rewLines)
removed = removeExtremes(rew)
print(removed)
# splitFile = splitNewLine(filey)
# maxy = findMaxVal(splitFile)
# miny = findMinVal(splitFile)
# distance = (maxy - miny)/1000
# print(splitFile)
# removed = removeExtremes(splitFile)
# # normalised = normalise(splitFile, maxy)
# # print(normalised)
#
plotter(removed)