import cv2
import numpy as np
def out(): 
	
    def rethsv(event,x,y,flags,param):
		global h
		if event == cv2.EVENT_LBUTTONDOWN:
		    #print hsv[y,x]
		    h=hsv[y,x,0]

    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', rethsv)  
    cv2.namedWindow('mask')  


    cap = cv2.VideoCapture(0)
    h=174
    i=0
    while(i==0):
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
	 img = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
	 img = 255-img
	 params = cv2.SimpleBlobDetector_Params()

	 params.filterByArea = True
	 params.minArea = 50
	   
	 detector = cv2.SimpleBlobDetector(params)

	 keypoints = detector.detect(img)

	 im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

	 cv2.imshow("Keypoints", im_with_keypoints)
	 

	 cv2.imshow('frame',frame)
	 ans = [0,0]
	 i=10
	 #cv2.imshow('mask',mask)
	 #cv2.imshow('img',img)
	 if len(keypoints)>0:
	  print "x:"
	  print keypoints[0].pt[0]
	  ans[0] = keypoints[0].pt[0]
	  print "y:"
	  print keypoints[0].pt[1]
	  ans[1] = keypoints[0].pt[1]  
	 k = cv2.waitKey(5) & 0xFF
	 
	 if k == 27:
		break


    
    cv2.destroyAllWindows()
    	  
out()
