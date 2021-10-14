import numpy as np
import utils
import sys
import base64
from PIL import Image
from io import BytesIO

class Operations:
    def __init__(self, size, repeatNum, imost=True):
        self.size = size
        self.repeatNum = repeatNum
        self.imgorState = imost

    def actionTranslation(self, action):#0-6 = -, 7 = 0, 8-14 = +
        dicty = {0:-0.77, 1:-0.66, 2:-0.55, 3:-0.44, 4:-0.33, 5:-0.22, 6:-0.11, 7:0.0, 8:0.11, 9:0.22, 10:0.33, 11:0.44, 12:0.55, 13:0.66, 14:0.77}
        return dicty[action]

    def argMax(self, action):
        return np.argmax(action)

    #Adds Image to the front, removing from the back of the array
    def addImage(self, imageList, image):
        #Insert to the front, delete back image
        imageList = np.insert(imageList, 0, image)
        del imageList[self.size/self.repeatNum:]
        return imageList

    #Takes the image and repeats or adds it in the correct location
    def createExperience(self, imageList, image):
        if imageList == []:
            output = np.repeat(image, self.repeatNum)
        else:
            output = self.addImage(imageList, image)
        return output, imageList


    def createImage(self, image):
        output = Image.open(BytesIO(base64.b64decode(image)))
        try:
            output = np.asarray(output)  # from PIL image to numpy array
            # output = utils.preprocess(output)  # apply the preprocessing
            output = np.array([output])  # the model expects 4D array
            output = output.flatten()
            return output/255.0

        except Exception as e:
            print(e)
            sys.exit(1)

    def checkReward(self, reward):
        if reward == 0.0:
            return -0.001
        else:
            return reward