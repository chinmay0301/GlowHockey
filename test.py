import cv2
import numpy as np


cv2.namedWindow('frame')
#cv2.setMouseCallback('frame', rethsv)  
cv2.namedWindow('mask')  


cap = cv2.VideoCapture(0)
h=174
i=0
while(i==0):
    # Take each frame
     _, frame = cap.read()
     #frame = cv2.flip(frame,1)

     
     hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
     cv2.imshow('frame',frame)
     cv2.waitKey(1)
     