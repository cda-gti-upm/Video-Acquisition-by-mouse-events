# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 12:59:32 2018

@author: ich
"""

import os
import numpy as np
import Leap
import struct
import ctypes

root = os.getcwd()

orig_data_path = root + "/RecordedData"
proc_data_path = root + "/ProcessedData"

gestures = os.listdir(orig_data_path)
pos = []

def main():
    controller = Leap.Controller()
    for i in range(len(gestures)):
        orig_gest_path = os.path.join(orig_data_path, gestures[i])
        proc_gest_path = os.path.join(proc_data_path, gestures[i])
        
        if not os.path.exists(proc_gest_path):
            os.mkdir(proc_gest_path)
        
        users = os.listdir(orig_gest_path)
        repetition = 0
        
        for j in range(len(users)):
            orig_user_path = os.path.join(orig_gest_path, users[j])
            
            # read pressed.txt
            pressed_file = open(os.path.join(orig_user_path,"pressed.txt"), "r") 
            pressed = pressed_file.readlines()
            pressed_file.close()
            
            # find changes from 0 to 1
            changes = np.where(np.roll(pressed,1)!=pressed)[0]
            index = np.arange(0, len(changes), 2)
            
            # read trajectories
            traj_file = os.path.join(orig_user_path,"savedframes.data")
            with open(traj_file, "rb") as data_file:
                next_block_size = data_file.read(4)
                while next_block_size:
                    size = struct.unpack('i', next_block_size)[0]
                    data = data_file.read(size)
                    leap_byte_array = Leap.byte_array(size)
                    address = leap_byte_array.cast().__long__()
                    ctypes.memmove(address, data, size)
                    
                    frame = Leap.Frame()
                    frame.deserialize((leap_byte_array, size))
                    next_block_size = data_file.read(4)
                                
                    for hand in frame.hands:
                        for finger in hand.fingers:
                            if finger.type == 1:
                                pos.append(finger.tip_position)
            
            # copy frames with pressed 1 on each change to a different directory
            for l in index:
                
                if l<len(changes):

                    traj = pos[changes[l]:changes[l+1]]
                    proc_rep_path = os.path.join(proc_gest_path, "rep_"+str(repetition).zfill(3))
                    
                    if not os.path.exists(proc_rep_path):
                        os.mkdir(proc_rep_path)
                    
                    traj_proc = os.path.join(proc_rep_path, "trajectory.txt")
                    
                    with open(traj_proc, 'w') as f:
                        for item in traj:
                            f.write("%s\n" % item)
        
                    repetition = repetition + 1
          
                                
if __name__ == "__main__":
    main()