
import cv2
import numpy as np

def rethsv(event,x,y,flags,param):
        global h
        if event == cv2.EVENT_LBUTTONDOWN:
            print hsv[y,x]
            h=hsv[y,x,0]

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', rethsv)  
cv2.namedWindow('mask')  


cap = cv2.VideoCapture(0)
h=174

while(1):
    # Take each frame
 _, frame = cap.read()
 frame = cv2.flip(frame,1)

 cv2.imshow('frame',frame)

 hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
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

 res = cv2.bitwise_and(frame,frame, mask=mask)

 cv2.imshow('frame',frame)
 cv2.imshow('mask',mask)
 cv2.imshow('res',res)

 k = cv2.waitKey(5) & 0xFF
 if k == 27:
        break



cv2.destroyAllWindows()
	 
