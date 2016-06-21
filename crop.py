# Required modules
import cv2

# Constants for the crop size
xMin = 300
yMin = 220
xMax = 320
yMax = 240

# Open cam, decode image, show in window
cap = cv2.VideoCapture(1) # use 1 or 2 or ... for other camera
cv2.namedWindow("Original")
cv2.namedWindow("Cropped")
cv2.moveWindow("Original", 0,0)

key = -1
cv2.namedWindow("mach")
cv2.getTrackbarPos("mach", "Original")


while(key < 0):
    success, img = cap.read()

    cropImg = img[yMin:yMax,xMin:xMax] # this is all there is to cropping

    cv2.imshow("Original", img)
    cv2.imshow("Cropped", cropImg)

    key = cv2.waitKey(1)
cv2.destroyAllWindows()