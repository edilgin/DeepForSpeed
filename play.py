from play_util import *
from createData import CreateData
from model_architectures import nvidia_arch
import torch
import os
import keyboard
import numpy as np

# function that acts as an api between game and the neural network
def playGame(modelName, trainedModelName):
    # get the neuralnet from model architectures
    neuralnet = nvidia_arch()
    # check if trained model exists if it does load them else return from the function
    nn_location = os.getcwd() + f"\\trained_models\\{trainedModelName}.pth"
    if os.path.exists(nn_location):
        neuralnet.load_state_dict(torch.load(nn_location))
        neuralnet.eval()
    else:
        print("that trained model does not exist")
        return

    # read the screen
    dataloader = CreateData()
    # wait a little before running the script to give time to open the game
    for i in range(3,0,-1):
        print(i)
        time.sleep(1)

    # main loop
    with torch.no_grad():
        while True:
            screen = dataloader.get_screen()
            # turn the screen to tensors
            road, minimap, speed = torch.tensor(screen[0]), torch.tensor(screen[1]), torch.tensor(screen[2])
            # some dummy dimension for pytorch

            road = road[None, None]
            minimap = minimap[None, None]
            speed = speed[None, None]

            output = neuralnet.forward(road/255, minimap/255, speed/255)
            print(output)

            # get the highest probability from the output and do that
            index = torch.argmax(output)
            """
            directx scan codes http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
            0x11 = w
            0x1E = A
            0x20 = D
            """
            if index == 0:          # press w
                PressKey(0x11)
                time.sleep(1)
                ReleaseKey(0x11)
                print("forward")
            elif index == 1:        # press a
                PressKey(0x1E)
                time.sleep(1)
                ReleaseKey(0x1E)
                print("left")
            elif index == 2:        # press d
                PressKey(0x20)
                time.sleep(1)
                ReleaseKey(0x20)
                print("right")
            elif index == 3:        # press wa
                PressKey(0x11)
                PressKey(0x1E)
                time.sleep(1)
                ReleaseKey(0x11)
                ReleaseKey(0x1E)
                print("forward left")
            elif index == 4:        # press wd
                PressKey(0x11)
                PressKey(0x20)
                time.sleep(1)
                ReleaseKey(0x11)
                ReleaseKey(0x20)
                print("forward right")

            elif index == 5:        # nothing
                time.sleep(1)
                print("do nothing")

            # if q is pressed quit
            if keyboard.is_pressed("q"):
                break

playGame("nvidia_arch", "test" )