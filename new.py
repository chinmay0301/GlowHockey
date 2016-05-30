import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):
 ret,frame = cap.read()
 if not ret : continue
 hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
	 
 lower = np.array([0,0,150])
 upper = np.array([150,150,255])

 mask = cv2.inRange(hsv, lower, upper)

 res = cv2.bitwise_and(frame,frame, mask=mask)

 cv2.imshow('frame',frame)
 cv2.imshow('mask',mask)
 cv2.imshow('res',res)

 k = cv2.waitKey(0) &0xFF

cap.release()
cv2.destroyAllWindows()
	 
