import subprocess

def killProcess(pid):
    output = subprocess.run("taskkill /fi \"pid eq {}\"".format(pid), stdout=subprocess.PIPE)
    print(output)