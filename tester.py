import Unitysim.utils as utils
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

sio = socketio.Server()
app = Flask(__name__)

timestep = 0
imageList = []
prevImage = []
prevReward = 0
numEpisode = 0
episodeReward = []

width = 256
height = 256
channels = 3
repeatNum = 16

size = width * height * channels * repeatNum

#Model parameters
stateDim = 39600 #nxn
actionDim = 3
update_timestep = 0

#learning rate of actor and critic
lrActor = 0.001
lrCritic = 0.001

#PPO and adams settings
gamma = 0.99
PPOEpochs = 4
clipRate = 0.2

model = PPO.PPO(stateDim, actionDim, lrActor, lrCritic, gamma, PPOEpochs, clipRate,
                 has_continuous_action_space=True, action_std_init=0.6)
#Load the model
file, index = gF.getFiles(os.listdir())
if file != None:
    model.load(file)

o = op.Operations(size, repeatNum)

@sio.on('telemetry')
def telemetry(sid, data):
    global timestep, model, imageList, prevImage, update_timestep, prevReward, numEpisode, episodeReward
    #Get the info from the environment
    image = data['image']
    done = data['resetEnv']
    reward = data['reward']

    timestep += 1

    # We need to create the image buffers, or add images to the buffer
    inputImage, imageList = o.createExperience(imageList, image)

    if prevImage == []:
        prevImage = inputImage

    if done.lower() == "true":
        print("episode gave a reward of {}, with the last reward being {} over {} actions".format(episodeReward[-1], reward, timestep))
        timestep = 0

    image = imagePrep.createImage(image)

    #Create an action
    action = model.select_action(image)

    time.sleep(0.05)

    prevImage = image

    #Save the reward, and whether it is a terminal state or not
    model.buffer.rewards.append(reward)
    model.buffer.is_terminals.append(done)

    episodeReward[-1] += reward
    prevReward = reward

    #Send the action to the environment
    send_control(action[0], (action[1]+1.0/2), action[2])

@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    reset()
    send_control(0.0, 0.0, 0.0)
    send_control(0.0, 0.0, 0.0)
    send_control(0.0, 0.0, 0.0)


def reset():
    send_control(0.0, 0.0, 0.0)
    send_control(0.0, 0.0, 0.0)
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

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)
    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
