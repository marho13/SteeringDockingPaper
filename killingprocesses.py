import psutil
import os, sys
import subprocess

def checkMemory():
    free_mem_in_kb = psutil.virtual_memory()[1]
    if float(free_mem_in_kb) < 4000000000.0:
        print(free_mem_in_kb)
        return True
    return False

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

def killProcess(pid):
    output = subprocess.run("taskkill /fi \"pid eq {}\"".format(pid), stdout=subprocess.PIPE)
    print(output)

pid = getPid()
print(pid)
killProcess(pid)