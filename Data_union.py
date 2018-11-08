# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 11:24:18 2018

@author: ich

Union of two precessed datasets
"""

import os
import shutil

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)



msg = "Insert absolute path of the final database:"
final_data_path = input(msg)

msg = "Insert absolute path of the additional database:"
orig_data_path = input(msg)
        
gestures = os.listdir(orig_data_path)        

for i in range(len(gestures)):
    orig_gest_path = os.path.join(orig_data_path, gestures[i])
    final_gest_path = os.path.join(final_data_path, gestures[i])
    
    orig_repetitions = len(os.listdir(final_gest_path)) # Original number of repetitions
    extra_repetitions = len(os.listdir(orig_gest_path)) # Extra number of repetitions
    
    for j in range(extra_repetitions):
        dir_orig = os.path.join(orig_gest_path, "rep_"+str(j).zfill(3))
        dir_final = os.path.join(final_gest_path, "rep_"+str(orig_repetitions+j).zfill(3))
        
        if not os.path.exists(dir_final):
            os.mkdir(dir_final)
            
        copytree(dir_orig, dir_final)
        