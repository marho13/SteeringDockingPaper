import os, sys, re



def findResults(directory):
    files = (os.listdir(directory))
    results = []
    names = []
    for f in files:
        if (re.search(".txt", f)):
            results.append(directory + "/" + f)
            names.append(f)
    print(results)
    return results, names

def readFile(file):
    return open(file).read()

def writeFile(file):
    return open(file, mode="w")

def removeOtherText(filey, writer):
    filey = filey.split("\n")
    output = []
    for line in filey:
        if (re.search("reward of", line)):
            output.append(line)
    return output

def writeToFile(file, data):
    for d in data:
        file.write(d + "\n")

files, filenames = findResults("C:/Users/Martin/Desktop")
for file, name in zip(files, filenames):
    reader = readFile(file)
    writer = writeFile(name)
    removeOtherText(reader, writer)

    writer.close()