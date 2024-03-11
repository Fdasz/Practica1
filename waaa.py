import numpy as np
import cv2

img = cv2.imread('fotoaaa.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray, 40, 0.01, 10)
corners = np.int0(corners)
   
for i in corners:
    x,y = i.ravel()
    cv2.circle(img, (x,y), 3, 255, -1)
   
cv2.imshow('corner', img)
cv2.waitKey(0)