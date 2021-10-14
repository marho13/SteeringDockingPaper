from PIL import Image
from io import BytesIO
import numpy as np
import base64
from Unitysim import utils
import sys

def createImage(image):
    output = Image.open(BytesIO(base64.b64decode(image)))
    try:
        output = np.asarray(output)  # from PIL image to numpy array
        # output = utils.preprocess(output)  # apply the preprocessing
        output = np.array([output])  # the model expects 4D array
        output = output.flatten()
        return output / 255.0

    except Exception as e:
        print(e)
        sys.exit(1)