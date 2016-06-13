import pygame
from pygame.locals import *
from sys import exit
import random

import cv2
import numpy as np
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
    
   
              


pygame.init()
# length= input (" Enter the length of screen:  ")   add length
# width= input (" Enter the width of screen:  ")     add width

screen=pygame.display.set_mode((640,480),0,32)     # add dimensions
pygame.display.set_caption("Pong Pong!")

back = pygame.Surface((640,480))                #add dimensions 
background = back.convert()
background.fill((0,0,0))         
goal = pygame.Surface((5,100))
mallet1 = pygame.Surface((50,50))
circ1= pygame.draw.circle(mallet1,(0,255,0),(25,25),25)   #add
mallet2 = pygame.Surface((50,50))
circ2= pygame.draw.circle(mallet2,(255,0,0),(25,25),25)
bar1 = mallet1.convert()
bar1.set_colorkey((0,0,0))
bar2 = mallet2.convert()
bar2.set_colorkey((0,0,0))
goal1 = goal.convert()
goal2 = goal.convert()
goal1.fill((0,255,0))
goal2.fill((0,255,0))
circ_sur = pygame.Surface((15,15))
circ = pygame.draw.circle(circ_sur,(0,255,0),(15/2,15/2),15/2)
circle = circ_sur.convert()
circle.set_colorkey((0,0,0))
# some definitions
RED = (255,0,0)                                   # look at this line again 
bar1_x, bar2_x = 5. , 585.
bar1_y, bar2_y = 215. , 215.
goal1_x,goal2_x = 0. , 635.                      # leftmost point 
goal1_y,goal2_y = 190. , 190.                   #topmost point
circle_x, circle_y = 312.5,232.5
bar1_movex, bar1_movey, bar2_movey,bar2_movex = 0. , 0. , 0. , 0.
speed_x, speed_y, speed_circ = 250., 250., 250.
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
    frame = pygame.draw.rect(screen,(255,255,255),Rect((5,5),(635,475)),2)
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
      a=keypoints[0].pt[0]
      ans[0] = keypoints[0].pt[0]
      print "y:"
      b= keypoints[0].pt[1]
      ans[1] = keypoints[0].pt[1]  
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

    if bar1_y >= 420.: bar1_y = 420.
    elif bar1_y <= 10. : bar1_y = 10.
    if bar1_x <= 10. :bar1_x = 10.
    elif bar1_x >= 310. :bar1_x = 310.
    if bar2_y >= 420.: bar2_y = 420.
    elif bar2_y <= 10.: bar2_y = 10.
    if bar2_x >= 620. :bar2_x = 620.
    elif bar2_x <= 340. :bar2_x = 340.
    
    
    if (circle_x <= bar1_x  and circle_x>=bar1_x-7.5): 
     if(circle_y <= bar1_y + 57.5 and circle_y >= bar1_y -7.5):
        speed_x = -speed_x
        circle_x = bar1_x -7.5

    if (circle_x <= bar1_x + 17.5 and circle_x>=bar1_x+10): 
     if(circle_y <= bar1_y + 57.5 and circle_y >= bar1_y -7.5):
        speed_x = -speed_x
        circle_x = bar1_x + 17.5    
    

    if (circle_x >= bar2_x -10 and circle_x <= bar2_x +10):
     if (circle_y <= bar2_y + 42.5 and circle_y >= bar2_y -7.5):
        speed_x = -speed_x
        circle_x = bar2_x - 10
        hit = 1  
    

    if circle_x < 5.: 
     if circle_y<=290 and circle_y>=190:
        bar2_score += 1
        circle_x, circle_y = 312.5, 232.5
        bar1_y,bar_2_y = 215., 215.
     elif not (circle_y<=290 and circle_y>=190) : speed_x = -speed_x
    elif circle_x > 627.5:
      if circle_y<=290 and circle_y>=190:
        bar1_score += 1
        circle_x, circle_y = 312.5, 232.5
        bar1_y, bar2_y = 215., 215.
      elif not (circle_y<=290 and circle_y>=190) : speed_x = -speed_x
    
    if circle_y <= 10.:
        speed_y = -speed_y
        circle_y = 10.
    elif circle_y >= 457.5:
        speed_y = -speed_y
        circle_y = 457.5

    pygame.display.update()
#cv2.destroyAllWindows()
