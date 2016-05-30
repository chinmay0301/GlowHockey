import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    ret, img = cap.read()
#img = cv2.imread('p1.jpg')
    lower = np.array([0,0,150],dtype="uint8")
    upper = np.array([150,150,255],dtype="uint8")

    mask = cv2.inRange(img, lower, upper)
    output = cv2.bitwise_and(img, img, mask = mask)

    im = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    im = (255-im)

    detector = cv2.SimpleBlobDetector()

    keypoints = detector.detect(im)

    im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imshow("Keypoints", im_with_keypoints)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #cv2.imshow("image", np.hstack([img,output]))
    #cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()
