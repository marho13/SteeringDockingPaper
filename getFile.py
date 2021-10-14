def lastCheckpoint(listy):
    maxInd = 0
    index = 0
    for a in range(len(listy)):
        for b in range(len(listy[a])):
            try:
                _ = (int(listy[a][b:-4]))
                if int(listy[a][b:-4]) > maxInd:
                    maxInd = int(listy[a][b:-4])
                    index = a
                break

            except:
                pass
    print(maxInd, index)
    if maxInd > 0:
        return listy[index], maxInd
    return None, 0


def removeNonCheck(files):
    for f in range(len(files) - 1, -1, -1):
        if files[f][:4] == "PPO_":
            pass
        else:
            del files[f]
    return files

def getFiles(listy):
    files = removeNonCheck(listy)

    if files != []:
        file, ind = lastCheckpoint(listy)
        if file != []:
            return file, ind
    return None, 0
