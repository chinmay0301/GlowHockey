import pygame
from pygame.locals import *
from sys import exit
import random

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
    
   
              


pygame.init()
# length= input (" Enter the length of screen:  ")   add length
# width= input (" Enter the width of screen:  ")     add width

screen=pygame.display.set_mode((640,480),0,32)     # add dimensions
pygame.display.set_caption("Pong Pong!")

back = pygame.Surface((640,480))                #add dimensions 
background = back.convert()
background.fill((0,0,0))         
goal = pygame.Surface((5,100))
mallet1 = pygame.Surface((30,30))
circ1= pygame.draw.circle(mallet1,(0,255,0),(15,15),15)   #add
mallet2 = pygame.Surface((30,30))
circ2= pygame.draw.circle(mallet2,(0,0,255),(15,15),15)
bar1 = mallet1.convert()
bar1.set_colorkey((0,0,0))
bar2 = mallet2.convert()
bar2.set_colorkey((0,0,0))
goal1 = goal.convert()
goal2 = goal.convert()
goal1.fill((0,255,0))
goal2.fill((0,255,0))
circ_sur = pygame.Surface((30,30))
circ = pygame.draw.circle(circ_sur,(255,255,255),(30/2,30/2),30/2)
circle = circ_sur.convert()
circle.set_colorkey((0,0,0))
# some definitions
RED = (255,0,0)                                   # look at this line again 
bar1_x, bar2_x = 25. , 585.
bar1_y, bar2_y = 225. , 225.
goal1_x,goal2_x = 0. , 635.                      # leftmost point 
goal1_y,goal2_y = 190. , 190.                   #topmost point
circle_x, circle_y = 305.,225.
bar1_movex, bar1_movey, bar2_movey,bar2_movex = 0. , 0. , 0. , 0.
speed_x, speed_y,speed_circ= 00., 00.,100. 
bar1_score, bar2_score = 0,0
#clock and font objects
clock = pygame.time.Clock()
font = pygame.font.SysFont("calibri",40)
hit = 0
count=0  #variables added
t=0
prev=pygame.time.get_ticks()/1000.0
ai_speed=0
a=0
b=0


while True:
    #lines added
    if count!=0:
        t=pygame.time.get_ticks()/1000.0
    count=count+1
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
       
 
   
    score1 = font.render(str(bar1_score), True,(255,255,255))
    score2 = font.render(str(bar2_score), True,(255,255,255))

    screen.blit(background,(0,0))
    frame = pygame.draw.rect(screen,(255,255,255),Rect((5,5),(630,470)),2)
    middle_line = pygame.draw.aaline(screen,(255,255,255),(320,5),(320,475))
    screen.blit(bar1,(bar1_x,bar1_y))
    screen.blit(bar2,(bar2_x,bar2_y))
    screen.blit(goal1,(goal1_x,goal1_y))
    screen.blit(goal2,(goal2_x,goal2_y))
    screen.blit(circle,(circle_x,circle_y))
    screen.blit(score1,(250.,210.))
    screen.blit(score2,(380.,210.))
    #pygame.time.wait(500)
   
    i=0
    while(i==0):
        # Take each frame
     _, frame = cap.read()
     frame = cv2.flip(frame,1)

     #cv2.imshow('frame',frame)
     #cv2.waitKey(0)
     hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
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
     img = cv2.cvtColor(res, cv2.COLOR_RGB2GRAY)
     img = 255-img
     params = cv2.SimpleBlobDetector_Params()

     params.filterByArea = True
     params.minArea = 15
       
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
      a=keypoints[0].pt[0]
      ans[0] = keypoints[0].pt[0]
      print "y:"
      b= keypoints[0].pt[1]
      ans[1] = keypoints[0].pt[1]  
      speed1_x=(ans[0]-a)/diff
      speed1_y=(ans[1]-b)/diff
     k = cv2.waitKey(5) & 0xFF
     
     if k == 27:
        break
  
    bar1_y = b
    bar1_x = a
    bar2_y += bar2_movey
    bar2_x += bar2_movex
# movement of circle
    time_passed = clock.tick(30)
    time_sec = time_passed / 1000.0
    #3 lines added
    diff= prev-t 
    prev=t
    

    circle_x += speed_x * time_sec
    circle_y += speed_y * time_sec
    ai_speed = speed_circ * time_sec
#AI of the computer.

    if bar1_y >= 445.: bar1_y = 445.
    elif bar1_y <= 5. : bar1_y = 5.
    if bar1_x <= 5. :bar1_x = 5.
    elif bar1_x >= 305. :bar1_x = 305.
    if bar2_y >= 445.: bar2_y = 445.
    elif bar2_y <= 5.: bar2_y = 5.
    if bar2_x >= 605. :bar2_x = 605.
    elif bar2_x <= 305. :bar2_x = 305.
    
    
    if (((circle_x-bar1_x)**2 + (circle_y - bar1_y)**2)<= 900):
       
       if ((circle_x-bar1_x)!=0):
        m1= (circle_y-bar1_y)/(circle_x-bar1_x)
       
        sinx=1-((1/(1+m1*m1)) )
        cosx=1/(1+m1*m1)
        cos2x= (1-m1**2)/(1+m1**2)
        sin2x=2*m1/(1+m1**2)
        speed_x= speed1_x*cosx + speed1_y*cosx*m1-speed_x*cos2x -speed_y*sin2x
        speed_y= speed1_x*sin2x/2.0 + speed1_y*sinx - speed_x*sin2x +speed_y*cos2x

       elif ((circle_x-bar1_x)==0) :
        sinx=1
        cosx=0
        cos2x= -1
        sin2x= 0
        speed_x= speed1_x*cosx-speed_x*cos2x -speed_y*sin2x
        speed_y= speed1_x*sin2x/2.0 + speed1_y*sinx - speed_x*sin2x +speed_y*cos2x
    

    if (((circle_x-bar2_x)**2 + (circle_y - bar2_y)**2)<= 900):
       
       m2= (circle_y-bar2_y)/(circle_x-bar2_x)
       cos2x= (1-m2**2)/(1+m2**2)
       sin2x=2*m2/(1+m2**2)
       
       speed_x= speed_circ*(1/(1+m1*m1)) + speed_circ*(1/(1+m1*m1))*m1-speed_x*cos2x -speed_y*sin2x
       speed_y= speed_circ*sin2x/2.0 + speed_circ*(1-((1/(1+m1*m1)) )) - speed_x*sin2x +speed_y*cos2x
    

    if circle_x <= 5.: 
     if circle_y<=290 and circle_y>=190:
        bar2_score += 1
        circle_x, circle_y = 305., 225.
        bar1_y,bar_2_y = 225., 225.
        speed_x, speed_y, speed_circ = 250., 250., 250.
     elif not (circle_y<=260 and circle_y>=190) : speed_x = -speed_x
    elif circle_x >= 605:
      if circle_y<=290 and circle_y>=190:
        bar1_score += 1
        circle_x, circle_y = 305., 225.
        bar1_y, bar2_y = 225., 225.
        speed_x, speed_y, speed_circ = 250., 250., 250.
      elif not (circle_y<=260 and circle_y>=190) : speed_x = -speed_x
    
    if circle_y <= 5.:
        speed_y = -speed_y
        circle_y = 5.
    elif circle_y >= 445.:
        speed_y = -speed_y
        circle_y = 445.
    pygame.display.update()
cv2.destroyAllWindows()
