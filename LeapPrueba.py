 # -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 10:28:40 2018

@author: Raquel Dueñas Suárez
"""
# COMPLETE: Include mouse events

import Leap, sys, os

def fcount(path): # Counter of subdirectories
    count1 = 0
    for root, dirs, files in os.walk(path):
        count1 += len(dirs)
    return count1

# Create directory to save outputs
msg = "Indique el gesto: eg = 0, 1, 2,..."
gesto = input(msg)

root = os.getcwd()
directory = root + '\\Data/' + str(gesto) # gesture directory

if not os.path.exists(directory):
    os.mkdir(directory)

rep = fcount(directory)
directory = directory + '/' + str(rep) # repetition/user directory

if not os.path.exists(directory):
    os.mkdir(directory)
    
moment = directory + '/moments.txt' 
    
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
        
        # COMPLETE: Save frames
        
        
        for hand in frame.hands:
            
            for finger in hand.fingers:
                if finger.type == 1:
                    print("Index position: " + str(finger.tip_position))
                    
                    # COMPLETE: Save fingertip location
                    
                    
def main():
    listener = LeapMotionListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    print("Press Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)
        
if __name__ == "__main__":
    main()