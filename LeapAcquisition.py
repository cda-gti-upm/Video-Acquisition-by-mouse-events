 # -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 10:28:40 2018

@author: Raquel Dueñas Suárez

Capturing data from Leap Motion:
    - Instert the gesture you are about to perform
    - Click and keep press the left button when performing the gesture
    - When finished, press the right button
"""

import Leap
import sys
import os
import ctypes
import struct
import numpy as np
import cv2

from pynput import mouse
 

## VARIABLES

frames = []
data_frames = []
size_frames = []
pressed_moments = []
pressing = 0 


## AUXILIAR FUNCTIONS

def fcount(path): # Counter of subdirectories
    count1 = 0
    for root, dirs, files in os.walk(path):
        count1 += len(dirs)
    return count1
        
def on_move(x, y): # Mouse moving
    pass

def on_click(x, y, button, pressed): # Mouse click
    global pressing
    if button == mouse.Button.left:
        print('{0}'.format(
            'Pressed' if pressed else 'Released'))
        if pressed:
            pressing = 1
        else:
            pressing = 0
    else:
        return False

def on_scroll(x, y, dx, dy): # Mouse scroll
    pass


## CREATE DIRECTORIES

msg = "Indique el gesto: eg = 0, 1, 2,..."
gesto = input(msg)

root = os.getcwd()
directory = root + '\\RecordedData/gesture_' + str(gesto) # Gesture directory

if not os.path.exists(directory):
    os.mkdir(directory)

rep = fcount(directory)
directory = directory + '/session_' + str(rep).zfill(3) # Session directory

if not os.path.exists(directory):
    os.mkdir(directory)
    
frames_path = directory + "/savedframes.data"
pressed_path = directory + "/pressed.txt"
    
 
## LEAP MOTION
    
class LeapMotionListener(Leap.Listener):
    
    def on_init(self, controller):
        print("Initialized")
        
    def on_connect(self,controller):
        print("Motion Sensor Connected")
        
    def on_disconnect(self, controller):
        print("Motion Sensor Disconnected")
        
    def on_exit(self, controller):
        print("Exited")
        
    def on_frame(self, controller):
        frame = controller.frame()
        frames.append(frame)
        data_frames.append(frame.serialize[0])
        size_frames.append(frame.serialize[1])
        pressed_moments.append(pressing)
  
    
## MAIN FUNCTION
                
def main():
    
    controller = Leap.Controller()
    listener = LeapMotionListener()  
    controller.add_listener(listener)
    controller.set_policy(Leap.Controller.POLICY_IMAGES)
    
    print("Press right button to quit...")
    
    try:
        # MOUSE LISTENING
        with mouse.Listener(
                on_move=on_move,
                on_click=on_click,
                on_scroll=on_scroll) as mouseListener:
            mouseListener.join()
        sys.stdin.readline()
        
    except KeyboardInterrupt:
        pass
    
    finally:
        
        controller.remove_listener(listener) #Stop capturing data
        
        # SAVE FRAMES
        with open(frames_path, "wb") as data_file:
            for f in range(len(data_frames)):
                data = data_frames[f]
                size = size_frames[f]
                data_file.write(struct.pack("i", size))

                data_address = data.cast().__long__()
                buffering = (ctypes.c_ubyte * size).from_address(data_address)
                data_file.write(buffering)
        
        # SAVE IMAGES
        for i in range(len(frames)):
            
            if frames[i].images[0].is_valid:
                image = frames[i].images[0]
                i_address = image.data_pointer
                ctype_array_def = ctypes.c_ubyte * image.height * image.width
                # as ctypes array
                as_ctype_array = ctype_array_def.from_address(int(i_address))
                # as numpy array
                as_numpy_array = np.ctypeslib.as_array(as_ctype_array)
                img = np.reshape(as_numpy_array, (image.height, image.width))
                
                images_path = directory + "/image_" + str(i).zfill(5) + ".png"
                cv2.imwrite(images_path,img)
        
        # SAVE MOUSE EVENTS
        f = open(pressed_path, "w")
        for p in pressed_moments:
            f.write("%s\n" % p)
        f.close()
        
        
if __name__ == "__main__":
    main()