import subprocess

def split(input):
    return str(input.stdout).split(" ")

def removeWhiteSpace(texter):
    output = []
    for t in texter:
        if t != "":
            output.append(t)
    return output

def findPid(texty):
    for t in range(len(texty)):
        if texty[t].endswith(".exe"):
            return texty[t+1]

def getPid():
    output = subprocess.run("tasklist /fi \"imagename eq boatSimulation2D.exe\"", stdout=subprocess.PIPE)
    splitter = split(output)
    whiteSpace = removeWhiteSpace(splitter)
    return findPid(whiteSpace)