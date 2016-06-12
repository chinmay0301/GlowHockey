from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock


import cv2
import numpy as np

def rethsv(event,x,y,flags,param):
     
        global h
        if event == cv2.EVENT_LBUTTONDOWN:
            #print hsv[y,x]
            h=hsv[y,x,0]

cv2.namedWindow('frame')
cv2.setMouseCallback('frame', rethsv)  
  


cap = cv2.VideoCapture(0)
h=174
_, x = cap.read()
x = cv2.flip(x, 1)
hsv = cv2.cvtColor(x, cv2.COLOR_RGB2HSV)

class GoalPost(Widget):
  score = NumericProperty(0) 

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    goal1 = ObjectProperty(None)
    goal2 = ObjectProperty(None)
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        #bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        #bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1
        if ( self.ball.x < self.x) or (self.ball.x+42.5 >self.width):     #42.5 is radius of puck
            self.ball.velocity_x*= -1  
        #went of to a side to score point?
        if self.ball.x < self.x and (self.ball.y >self.top/2-60 and self.ball.y<self.top/2 + 60) :
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x + 42.5 > self.width and (self.ball.y >self.top/2-60 and self.ball.y<self.top/2 + 60):
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        ans = [0,0]
        ans = self.blob_detector(touch)
        if touch.x < self.width / 3:
            self.player1.center_x = ans[0]
            self.player1.center_y = ans[1]
        if touch.x > self.width - self.width / 3:
            self.player2.center_x = ans[0]
            self.player2.center_y = ans[1]
    def blob_detector(self,touch):
         _, frame = cap.read()
         frame = cv2.flip(frame,1)
         hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

     #cv2.imshow('frame',frame)
     #cv2.waitKey(0)
         
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
         return ans
         
class PongApp(App):
    def build(self):
         game = PongGame()
         game.serve_ball()
         Clock.schedule_interval(game.update, 1.0 / 500.0)
         Clock.schedule_interval(game.blob_detector, 1.0 / 500.0)
      
 
         return game


if __name__ == '__main__':
    PongApp().run()

