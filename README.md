# Boat-steering
Steering the boats in the different simulators
The simulator git is here: https://github.com/marho13/boatSimulator
You should both have access, also the FFI code is written to work with the FFI simulator, and does not work with the Unity simulator.
The Neural Networks are the same though, and should therefore be able transfer from one environment to another.

The actions are taken from the FFI simulator and is implemented on the Unity simulator for full compatibility.
It is currently just the 3 of us who have access, if you want anyone else to gain access, just send me an email as to whom with their github account and i can add them.


Tasks FFI sim:
*Create a reward system, some way of getting a reward
*Use the reward to update the PPO (only need to add the rewards and such to the memory and run the update function every N timesteps)

Tasks Unity sim:
*Find an agreeable reward system, i.e. the current reward system + one which takes into account the angle to the dock, making it so that when the boat is 0 degrees from the dock the reward is bigger
*Start the training and testing to see the effects of the different reward systems
