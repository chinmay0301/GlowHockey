import pygame
from pygame.locals import *
from sys import exit
import math 
import random
import CircleCollisions2
from time import sleep

import cv2
import numpy as np

def rethsv(event,x,y,flags,param):
        global h
        if event == cv2.EVENT_LBUTTONDOWN:
            print hsv[y,x]
            h=hsv[y,x,0]

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', rethsv)  
cv2.namedWindow('Keypoints',cv2.WINDOW_NORMAL)  
ymin=130
ymax=300
xmin=290
xmax=480

cap = cv2.VideoCapture(0)
h=174
    

pygame.init()
# length= input (" Enter the length of screen:  ")   add length
# width= input (" Enter the width of screen:  ")     add width

screen=pygame.display.set_mode((1360,710),0,32)     # add dimensions
pygame.display.set_caption("Pong Pong!")

back = pygame.Surface((1360,710))                #add dimensions 
background = back.convert()
background.fill((0,0,0))         
goal = pygame.Surface((10.625,147.916666667))
mallet1 = pygame.Surface((63.75,63.75))
circ1= pygame.draw.circle(mallet1,(0,255,0),(32,32),32)   #add
mallet2 = pygame.Surface((63.75,63.75))
circ2= pygame.draw.circle(mallet2,(0,0,255),(32,32),32)
bar1 = mallet1.convert()
bar1.set_colorkey((0,0,0))
bar2 = mallet2.convert()
bar2.set_colorkey((0,0,0))
goal1 = goal.convert()
goal2 = goal.convert()
goal1.fill((0,255,0))
goal2.fill((0,255,0))
circ_sur = pygame.Surface((63.75,63.75))
circ = pygame.draw.circle(circ_sur,(255,255,255),(32,32),32)
circle = circ_sur.convert()
circle.set_colorkey((0,0,0))
# some definitions'

RED = (255,0,0)                                   # look at this line again 
bar1_x, bar2_x = 53.125 , 1243.125
bar1_y, bar2_y = 332.8125000000000075 , 332.8125000000000075
goal1_x,goal2_x = 0. , 1349.375                      # leftmost point 
goal1_y,goal2_y = 281.041666666666673 , 281.041666666666673             #topmost point
circle_x, circle_y = 648.125,332.8125000000000075
#clock and font objects
clock = pygame.time.Clock()
font = pygame.font.SysFont("calibri",100)

#timer_before_game 
def timer():
    counter, text = 3, '3'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    while counter>=0:
        for e in pygame.event.get():
            if e.type == pygame.USEREVENT:
                counter -= 1
                text = str(counter).rjust(3) if counter > 0 else 'GO!'
            if e.type == pygame.QUIT: break
        else:
            screen.blit(background,(0,0))
            frame = pygame.draw.rect(screen,(255,255,255),Rect((10.625,10.625),(1338.75,688.75)),2)
            middle_line = pygame.draw.aaline(screen,(255,255,255),(680,10.625),(680,699.375))
            screen.blit(bar1,(bar1_x,bar1_y))
            screen.blit(bar2,(bar2_x,bar2_y))
            screen.blit(goal1,(goal1_x,goal1_y))
            screen.blit(goal2,(goal2_x,goal2_y))
            screen.blit(circle,(circle_x,circle_y))
           
            screen.blit(font.render(text, True, (255, 255, 255)), (620, 260))
            pygame.display.flip()
            clock.tick(60)
            continue
        break

timer()

bar1_movex, bar1_movey, bar2_movey,bar2_movex = 0. , 0. , 0. , 0.
speed_x, speed_y, speed1_x, speed2_x, speed1_y, speed2_y ,speed_circ= 400., 400.,400.,400.,400.,400. ,400. 
bar1_score, bar2_score = 0,0

hit = 0
count=0  #variables added
t=0

a,p=53.125 , 1243.125
b=332.8140000000000075
q=332.8140000000000075
prev=pygame.time.get_ticks()/1000.0
ai_speed=0
flag=0
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
    frame = pygame.draw.rect(screen,(255,255,255),Rect((10.625,10.625),(1338.75,688.75)),2)
    middle_line = pygame.draw.aaline(screen,(255,255,255),(680,10.625),(680,699.375))
    screen.blit(bar1,(bar1_x,bar1_y))
    screen.blit(bar2,(bar2_x,bar2_y))
    screen.blit(goal1,(goal1_x,goal1_y))
    screen.blit(goal2,(goal2_x,goal2_y))
    screen.blit(circle,(circle_x,circle_y))
    screen.blit(score1,(531.25,310.625000000000007))
    screen.blit(score2,(807.5,310.625000000000007))
    
# movement of circle
   
    
    if circle_x < 680 :   
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
         lower = np.array([110,100,100])   
         upper = np.array([130,255,255])
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

         cv2.imshow('Keypoints', im_with_keypoints)


         cropImg = frame[ymin:ymax,xmin:xmax] # this is all there is to cropping

         cv2.imshow("Cropped", cropImg)
         
         cv2.imshow('frame',frame)
       
         i=10
         #cv2.imshow('mask',mask)
         #cv2.imshow('img',img)
         if len(keypoints)>0:
         
          a=keypoints[0].pt[0]
         
          b= keypoints[0].pt[1]
         
         k = cv2.waitKey(5) & 0xFF
         
         if k == 27:
            break

    else: 
        i=0
        while(i==0):
            # Take each frame
         _, frame = cap.read()
         frame = cv2.flip(frame,1)

         #cv2.imshow('frame',frame)
         #cv2.waitKey(0)
         hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
         # if h<20:
         #    l=0
         #    m=h+20
         # elif h>245:
         #    m=255
         #    l=h-10
         # else:
         #    l=h-20
         #    m=h+20
         lower = np.array([80,100,100])   
         upper = np.array([90,255,255])
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

         cv2.imshow('Keypoints', im_with_keypoints)

         cropImg = frame[ymin:ymax,xmin:xmax] # this is all there is to cropping

         cv2.imshow("Cropped", cropImg)
         
         cv2.imshow('frame',frame)
       
         i=10
         #cv2.imshow('mask',mask)
         #cv2.imshow('img',img)
         if len(keypoints)>0:
          
          p =keypoints[0].pt[0]
         
          q = keypoints[0].pt[1]
         
         k = cv2.waitKey(5) & 0xFF
         
         if k == 27:
            break
      
    bar1_y = b
    bar1_x = a
    bar2_y =q
    bar2_x =p
# movement of circle

    time_passed = clock.tick(30)
    time_sec = time_passed / 1000.0
    #3 lines added
    # diff= prev-t 
    # prev=t
    # print diff

    circle_x += speed_x * time_sec
    circle_y += speed_y * time_sec
    ai_speed = speed_circ * time_sec
#AI of the computer.

    if bar1_y >= 635.375: bar1_y = 635.375
    elif bar1_y <= 10.625 : bar1_y = 10.625
    if bar1_x <= 10.625 :bar1_x = 10.625
    elif bar1_x >= 648.125 :bar1_x = 648.125
    if bar2_y >= 635.375: bar2_y = 635.375
    elif bar2_y <= 10.625: bar2_y = 10.625
    if bar2_x >= 1285.625 :bar2_x = 1285.625
    elif bar2_x <= 648.125 :bar2_x = 648.125
    

    if (((circle_x-bar1_x)**2 + (circle_y - bar1_y)**2)<= 4064.0625):
            C1Speed = math.sqrt((speed_x**2)+(speed_y**2))
            XDiff = -(circle_x-bar1_x)
            YDiff = -(circle_y-bar1_y)
            if XDiff > 0:
                if YDiff > 0:
                    Angle = math.degrees(math.atan(YDiff/XDiff))
                    XSpeed = -C1Speed*math.cos(math.radians(Angle))
                    YSpeed = -C1Speed*math.sin(math.radians(Angle))
                elif YDiff < 0:
                    Angle = math.degrees(math.atan(YDiff/XDiff))
                    XSpeed = -C1Speed*math.cos(math.radians(Angle))
                    YSpeed = -C1Speed*math.sin(math.radians(Angle))
            elif XDiff < 0:
                if YDiff > 0:
                    Angle = 180 + math.degrees(math.atan(YDiff/XDiff))
                    XSpeed = -C1Speed*math.cos(math.radians(Angle))
                    YSpeed = -C1Speed*math.sin(math.radians(Angle))
                elif YDiff < 0:
                    Angle = -180 + math.degrees(math.atan(YDiff/XDiff))
                    XSpeed = -C1Speed*math.cos(math.radians(Angle))
                    YSpeed = -C1Speed*math.sin(math.radians(Angle))
            elif XDiff == 0:
                if YDiff > 0:
                    Angle = -90
                else:
                    Angle = 90
                XSpeed = C1Speed*math.cos(math.radians(Angle))
                YSpeed = C1Speed*math.sin(math.radians(Angle))
            elif YDiff == 0:
                if XDiff < 0:
                    Angle = 0
                else:
                    Angle = 180
                XSpeed = C1Speed*math.cos(math.radians(Angle))
                YSpeed = C1Speed*math.sin(math.radians(Angle))
            speed_x = XSpeed
            speed_y = YSpeed
       
    if (((circle_x-bar2_x)**2 + (circle_y - bar2_y)**2)<= 4064.0625):
       
            C1Speed = math.sqrt((speed_x**2)+(speed_y**2))
            XDiff = -(circle_x-bar2_x)
            YDiff = -(circle_y-bar2_y)
            if XDiff > 0:
                if YDiff > 0:
                    Angle = math.degrees(math.atan(YDiff/XDiff))
                    XSpeed = -C1Speed*math.cos(math.radians(Angle))
                    YSpeed = -C1Speed*math.sin(math.radians(Angle))
                elif YDiff < 0:
                    Angle = math.degrees(math.atan(YDiff/XDiff))
                    XSpeed = -C1Speed*math.cos(math.radians(Angle))
                    YSpeed = -C1Speed*math.sin(math.radians(Angle))
            elif XDiff < 0:
                if YDiff > 0:
                    Angle = 180 + math.degrees(math.atan(YDiff/XDiff))
                    XSpeed = -C1Speed*math.cos(math.radians(Angle))
                    YSpeed = -C1Speed*math.sin(math.radians(Angle))
                elif YDiff < 0:
                    Angle = -180 + math.degrees(math.atan(YDiff/XDiff))
                    XSpeed = -C1Speed*math.cos(math.radians(Angle))
                    YSpeed = -C1Speed*math.sin(math.radians(Angle))
            elif XDiff == 0:
                if YDiff > 0:
                    Angle = -90
                else:
                    Angle = 90
                XSpeed = C1Speed*math.cos(math.radians(Angle))
                YSpeed = C1Speed*math.sin(math.radians(Angle))
            elif YDiff == 0:
                if XDiff < 0:
                    Angle = 0
                else:
                    Angle = 180
                XSpeed = C1Speed*math.cos(math.radians(Angle))
                YSpeed = C1Speed*math.sin(math.radians(Angle))
            speed_x = XSpeed
            speed_y = YSpeed
    
        
    if circle_x <= 10.625: 
     if circle_y<=428.958333333333343 and circle_y>=281.041666666666673:
        bar2_score += 1
        
        circle_x, circle_y = 648.125,332.8125000000000075
        a,p=53.125 , 1243.125
        b,q= 332.8125000000000075, 332.8125000000000075
        speed_x, speed_y, speed_circ = 400., 400., 400.
        timer()
        pygame.time.wait(3000)
        
     elif not (circle_y<=384.583333333333342 and circle_y>=281.041666666666673) : speed_x = -speed_x
    elif circle_x >= 1285.625:
      if circle_y<=428.958333333333343 and circle_y>=281.041666666666673:
        bar1_score += 1
        
        circle_x, circle_y = 648.125,332.8125000000000075
        a,p=53.125 , 1243.125
        b, q = 332.8125000000000075, 332.8125000000000075
        speed_x, speed_y, speed_circ = 400., 400., 400.
        goald = font.render("goal!", True,(255,255,255))
        screen.blit(goald,(531.25,410.625000000000007))
        timer()
        pygame.time.wait(3000)
        
        
      elif not (circle_y<=384.583333333333342 and circle_y>=281.041666666666673) : speed_x = -speed_x
    
    if circle_y <= 10.625:
        speed_y = -speed_y
        circle_y = 10.625
    elif circle_y >= 635.375:
        speed_y = -speed_y
        circle_y = 635.375

    
    pygame.display.update()