#!/usr/bin/env python

import cv2
import numpy as np

# init hsv detect function
h = 0
cv2.namedWindow('Original')

def rethsv(event,x,y,flags,param):
        global h
        if event == cv2.EVENT_LBUTTONDOWN:
            #print hsv[y,x]
            h=hsv[y,x,0]

cv2.setMouseCallback('Original', rethsv)  

# choose default camera
cap = cv2.VideoCapture(0)

while(1):
    # Take each frame
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)

    cv2.imshow('Original',frame)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define hue limits and create mask
    if h<20:
           l=0
           m=h+20
    elif h>245:
           m=255
           l=h-10
    else:
           l=h-20
           m=h+20
    lower = np.array([l,100,100])   
    upper = np.array([m,255,255])
    mask = cv2.inRange(hsv, lower, upper)

    # generate result image
    mask_res = cv2.bitwise_and(frame,frame, mask=mask)

    # convert to grayscale and invert
    img = cv2.cvtColor(mask_res, cv2.COLOR_BGR2GRAY)
    img = 255-img

    # Blob Detector Parameters
    params = cv2.SimpleBlobDetector_Params()

    params.filterByArea = True
    params.minArea = 100
      
    detector = cv2.SimpleBlobDetector(params)

    keypoints = detector.detect(img)

    im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Detected and drawn to show: the blobs

    cv2.imshow("Keypoints", im_with_keypoints)

    # Print Keypoint position
    if len(keypoints)>0:
        print "x:", keypoints[0].pt[0]
        print "y:", keypoints[0].pt[1]
    
    if (cv2.waitKey(5) & 0xFF) == 27:
        break

# clean up
cv2.destroyAllWindows()
	 
