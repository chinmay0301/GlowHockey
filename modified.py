import pygame
from pygame.locals import *
from sys import exit
from math import * 
import random
from combination import out

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
   
 #pygame.time.wait(5000)
    bar1_y += bar1_movey
    bar1_x += bar1_movex
    bar2_y += bar2_movey
    bar2_x += bar2_movex
# movement of circle
    time_passed = clock.tick(30)
    time_sec = time_passed / 1000.0
    #3 lines added
    diff= prev-t 
    prev=t
    print diff

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
       m1= (circle_y-bar1_y)/(circle_x-bar1_x)
       cosx= (1-m1**2)/(1+m1**2)
       sinx=2*m1/(1+m1**2)
       speed_x= (speed_circ-speed_x)*cosx + (speed_circ-speed_y)*sinx
       speed_y= (speed_circ-speed_x)*sinx + (speed_circ-speed_y)*cosx
    if (((circle_x-bar2_x)**2 + (circle_y - bar2_y)**2)<= 900):
       m2= (circle_y-bar2_y)/(circle_x-bar2_x)
       cosx= (1-m2**2)/(1+m2**2)
       sinx=2*m2/(1+m2**2)
       speed_x= (speed_circ-speed_x)*cosx + (speed_circ-speed_y)*sinx
       speed_y= (speed_circ-speed_x)*sinx + (speed_circ-speed_y)*cosx
  

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
	
