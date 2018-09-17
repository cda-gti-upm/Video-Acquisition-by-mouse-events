 # -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 10:28:40 2018

@author: Raquel Dueñas Suárez
"""

import Leap, sys, os, ctypes, struct
from pynput import mouse


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
    print('{0}'.format(
        'Pressed' if pressed else 'Released'))
    if pressed:
        pressing = 1
    else:
        pressing = 0

def on_scroll(x, y, dx, dy): # Mouse scroll
    return False
    

# CREATE DIRECTORIES
msg = "Indique el gesto: eg = 0, 1, 2,..."
gesto = input(msg)
data_frames = []
size_frames = []
pressed_moments = []
pressing = 0

root = os.getcwd()
directory = root + '\\Data/gesture' + str(gesto) # gesture directory

if not os.path.exists(directory):
    os.mkdir(directory)

rep = fcount(directory)
directory = directory + '/user' + str(rep) # Repetition/user directory

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
        data_frames.append(frame.serialize[0])
        size_frames.append(frame.serialize[1])
        pressed_moments.append(pressing)
        print("Frame read")
        
        for hand in frame.hands:
            for finger in hand.fingers:
                if finger.type == 1:
                    print("Index position: " + str(finger.tip_position))
                    
                    
def main():
    listener = LeapMotionListener()
    controller = Leap.Controller()
    
    controller.add_listener(listener)
    
    print("Roll to quit...")
    try:
        # Mouse
        with mouse.Listener(
                on_move=on_move,
                on_click=on_click,
                on_scroll=on_scroll) as mouseListener:
            mouseListener.join()
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        
        # Save frames
        with open(frames_path, "wb") as data_file:
            for f in range(len(data_frames)):
                data = data_frames[f]
                size = size_frames[f]
                data_file.write(struct.pack("i", size))

                data_address = data.cast().__long__()
                buffering = (ctypes.c_ubyte * size).from_address(data_address)
                data_file.write(buffering)
        
        # Save mouse events
        f = open(pressed_path, "w")
        for p in pressed_moments:
            f.write("%s\n" % p)
        f.close()
        
        controller.remove_listener(listener)
        
if __name__ == "__main__":
    main()