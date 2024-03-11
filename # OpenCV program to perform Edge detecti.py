# OpenCV program to perform Edge detection in real time
# import libraries of python OpenCV
# where its functionality resides
import cv2
 
# np is an alias pointing to numpy library
import numpy as np
 
 
# capture frames from a camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 3)

# loop runs if capturing has been initialized
while(1):
 
    # reads frames from a camera
    ret, frame = cap.read()
 
    # converting BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
     
    # define range of red color in HSV
    lower_red = np.array([30,150,50])
    upper_red = np.array([255,255,180])
     
    # create a red HSV colour boundary and
    # threshold HSV image
    mask = cv2.inRange(hsv, lower_red, upper_red)
 
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    
 
    # Display an original image
    #cv2.imshow('original',frame)
    edges = cv2.Canny(frame,150,200)

    laplacian = cv2.Laplacian(frame,cv2.CV_64F)
    sobelx = cv2.Sobel(edges,cv2.CV_64F,1,0,ksize=5)
    sobely = cv2.Sobel(edges,cv2.CV_64F,0,1,ksize=5)

    # cv2.imshow('Laplace',laplacian)
  #  cv2.imshow('sobelX',sobelx)
   # cv2.imshow('SobelY',sobely)
    

    # finds edges in the input image and
    # marks them in the output map edges
    gray = cv2.cornerHarris(edges, 2, 3, 0.04)
   
    height, width = gray.shape
    color = (0, 255, 0)

    for y in range(0, height):
        for x in range(0, width):
            if gray.item(y, x) > 0.01 * gray.max():
                cv2.circle(frame, (x, y), 3, color, cv2.FILLED, cv2.LINE_AA)

    
    # Display edges in a frame
    cv2.imshow('Edges',edges)

    cv2.imshow('Harris Result', gray)
 
    # Wait for Esc key to stop
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
 
 
# Close the window
cap.release()
 
# De-allocate any associated memory usage
cv2.destroyAllWindows()