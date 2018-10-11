# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 12:59:32 2018

@author: ich
"""

import os
import shutil
import numpy as np

root = os.getcwd()

orig_data_path = root + "/RecordedData"
proc_data_path = root + "/ProcessedData"

gestures = os.listdir(orig_data_path)

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
        
        # copy frames with pressed 1 on each change to a different directory
        for l in index:
            
            if l<len(changes):
                
                init = changes[l]
                end = changes[l+1]
                images = np.arange(init, end)
                proc_rep_path = os.path.join(proc_gest_path, "rep_"+str(repetition).zfill(3))
                
                if not os.path.exists(proc_rep_path):
                    os.mkdir(proc_rep_path)
                
                for k in range(len(images)):
                    img_orig = os.path.join(orig_user_path, "image_"+str(images[k]).zfill(5)+".png")
                    img_proc = os.path.join(proc_rep_path, "image_"+str(k).zfill(3)+".png")
                    shutil.copy(img_orig, img_proc)
            
                repetition = repetition + 1
        
        