# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 09:40:32 2018

@author: Raquel Dueñas Suárez
"""
import cv2

num_frames = 0
traj_moments = [] # Vector of start and end of movements along the video
title = "--" # Capturing feedback

def on_mouse(event,x,y,flags,params):
    global traj_moments, num_frames, title
    
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Clicked")
        traj_moments[num_frames-1] = 1 # Start of movement
        title = "Recording movement"
        
    if event == cv2.EVENT_LBUTTONUP:
        print("Released")
        traj_moments[num_frames-1] = -1 # End of movement
        title = "--"
    
cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    
    num_frames = num_frames + 1
    traj_moments = traj_moments + [0]
    
    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame',on_mouse)
    if ret==True:
        frame = cv2.flip(frame,0)

        # write the flipped frame
        out.write(frame)
        img = frame

        cv2.putText(img,title, (100,400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),2)
        cv2.imshow('frame',img)
    
        if cv2.waitKey(1) & 0xFF == ord('q'): #Press Q to end video
            f = open('moments.txt','w+')
            for item in traj_moments:
                f.write("%s\n" % item)
            f.close()

            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
