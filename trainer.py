from Unitysim import imagePrep
import os
from flask import Flask
import eventlet.wsgi
import socketio
import time
import Unitysim.PPO as PPO
import Unitysim.getFile as gF
import torch
import Unitysim.operations as op
import time
import scipy.misc
from scipy.misc import imshow
import numpy as np
import subprocess
import psutil
from Unitysim.getPid import getPid
from Unitysim.killPid import killProcess

sio = socketio.Server()
app = Flask(__name__)

lastPacket = time.time()
timestep = 0
imageList = []
prevImage = []
prevReward = 0
numEpisode = 0
episodeReward = [0.0]

width = 256
height = 256
channels = 3
repeatNum = 16

size = width * height * channels * repeatNum

#Model parameters
stateDim = 196608#6 #nxn
actionDim = 3
update_timestep = 2000

#learning rate of actor and critic
lrActor = 0.001
lrCritic = 0.001

#PPO and adams settings
gamma = 0.99
PPOEpochs = 4
clipRate = 0.2

model = PPO.PPO(stateDim, actionDim, lrActor, lrCritic, gamma, PPOEpochs, clipRate,
                 has_continuous_action_space=True, action_std_init=0.6)
# model.load("PPO_road_50.pth")
#Load the model
file, index = gF.getFiles(os.listdir())
# if file != None:
#     model.load(file)

o = op.Operations(size, repeatNum)

print(psutil.virtual_memory()[1])
class process:
    def __init__(self, file):
        self.filenName = file
        self.process = self.startProcess()

    def startProcess(self):
       proc = subprocess.Popen(self.filenName, stdout=subprocess.DEVNULL, stderr=None)
       time.sleep(0.1)
       return proc

    def closeProcess(self, process):
       process.kill()
       time.sleep(5)
       output = self.startProcess()
       return output

# proc = process("C:/Users/Martin/Desktop/oceanImageTask2/boatSimulation2D.exe")

@sio.on('telemetry')
def telemetry(sid, data):
    global timestep, model, imageList, prevImage, update_timestep, prevReward, numEpisode, episodeReward
    #Get the info from the environment
    image = data['image']#np.asarray(data["state"].split(","), dtype=float)  # state = data['state']  # Can be image or state
    done = data['resetEnv']
    reward = float(data['reward'])
    lastPacket = time.time()
    timestep += 1

    # We need to create the image buffers, or add images to the buffer
    inputImage, imageList = o.createExperience(imageList, image)

    if prevImage == []:
        prevImage = inputImage#image
    # print(done)

    if done == 'True':
        if timestep >= update_timestep:
            print("Resetting, and updating")
            timestep, episodeReward, numEpisode = train(numEpisode, prevReward, timestep, episodeReward,
                                                                data["reward"])
            if checkMemory():
                model.save('PPO_task1_{}.pth'.format(len(episodeReward)))
                model = None
                time.sleep(5)
                model = PPO.PPO(stateDim, actionDim, lrActor, lrCritic, gamma, PPOEpochs, clipRate,
                                has_continuous_action_space=True, action_std_init=0.6)
                model.load("PPO_task1_{}.pth".format(len(episodeReward)))
            print("Trained")
            reset()
            time.sleep(1)
            send_control(0.0, 0.0, 0.0)
        else:
            if checkMemory():
                model.save('PPO_task1_{}.pth'.format(len(episodeReward)))
                model = None
                time.sleep(5)
                model = PPO.PPO(stateDim, actionDim, lrActor, lrCritic, gamma, PPOEpochs, clipRate,
                                has_continuous_action_space=True, action_std_init=0.6)
                model.load("PPO_task1_{}.pth".format(len(episodeReward)))
            print("Resetting, without updating {}".format(timestep))
            reset()
            time.sleep(1)
            send_control(0.0, 0.0, 0.0)

    else:
        if timestep > 5000:
            print("Resetting, and updating")
            timestep, episodeReward, numEpisode = train(numEpisode, prevReward, timestep, episodeReward,
                                                        data["reward"])
            if checkMemory():
                model.save('PPO_task1_{}.pth'.format(len(episodeReward)))
                model = None
                time.sleep(5)
                model = PPO.PPO(stateDim, actionDim, lrActor, lrCritic, gamma, PPOEpochs, clipRate,
                                has_continuous_action_space=True, action_std_init=0.6)
                model.load("PPO_task1_{}.pth".format(len(episodeReward)))
            print("Trained")
            reset()
            time.sleep(1)
            send_control(0.0, 0.0, 0.0)

    image = imagePrep.createImage(image)  # Can be ignored if we run on states

    #Create an action
    action = model.select_action(image)  # action = model.select_action(state)

    #time.sleep(0.05)

    prevImage = image

    #Save the reward, and whether it is a terminal state or not
    model.buffer.rewards.append(reward)
    model.buffer.is_terminals.append(done)

    episodeReward[-1] += float(reward)
    prevReward = float(reward)
    time.sleep(0.01)
    #Send the action to the environment
    send_control(action[0], (action[1]+1.0/2), action[2])

def train(numEpisode, reward, timestep, episodeReward, datarew):
    numEpisode += 1
    episodeReward[-1] += reward
    print("episode: {}, gave a reward of {}, with the last reward being {} over {} actions".format(
        len(episodeReward), episodeReward[-1], datarew, timestep))

    model.update()

    episodeReward.append(0.0)
    timestep = 0

    if ((len(episodeReward))) % 50 == 0 and len(episodeReward)>1:
        torch.save(model.policy.state_dict(), 'PPO_task1_{}.pth'.format(len(episodeReward)))
        writer = open("resultTask1.txt", mode="a")
        [writer.write(str(rew) + "\n") for rew in episodeReward[-50:]]
        print("saving!")

    return timestep, episodeReward, numEpisode

@sio.on('connect')
def connect(sid, environ):
    global proc, model, episodeReward
    print("connect ", sid)
    reset()
    send_control(0.0, 0.0, 0.0)


def reset():
    send_control(0.0, 0.0, 0.0)

def ready():
    sio.emit("ready",
             data={})
    send_control(0.0, 0.0, 0.0)


def send_control(steering_angle, throttle, bucket):
    sio.emit(
        "steer",
        data={
            'steering_angle': steering_angle.__str__(),
            'acceleration': throttle.__str__(),
            'bucket' : bucket.__str__()
        },
        skip_sid=True)

def checkMemory():
    free_mem_in_kb = psutil.virtual_memory()[1]
    if float(free_mem_in_kb) < 4000000000.0:
        print(free_mem_in_kb)
        # pid = getPid()
        # killProcess(pid)
        # time.sleep(5)
        return True
    return False

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)
    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
