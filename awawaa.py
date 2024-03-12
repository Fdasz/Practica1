import cv2

image1 = cv2.VideoCapture(0)
while True:
    # Lee un fotograma de la cámara
    ret, frame = image1.read()
    edges = cv2.Canny(frame,50,100)
    img_gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    ret, thresh1 = cv2.threshold(img_gray1, 150, 255, cv2.THRESH_BINARY)
    contours2, hierarchy2 = cv2.findContours(thresh1, cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE)
    image_copy2 = frame
    cv2.drawContours(image_copy2, contours2, -1, (0, 255, 0), 2, cv2.LINE_AA)
    image_copy3 = frame
    for i, contour in enumerate(contours2): # loop over one contour area
        for j, contour_point in enumerate(contour): # loop over the points
            # draw a circle on the current contour coordinate
            cv2.circle(image_copy3, ((contour_point[0][0], contour_point[0][1])), 2, (0, 255, 0), 2, cv2.LINE_AA)
    # see the results
    cv2.imshow('CHAIN_APPROX_SIMPLE Point only', image_copy3)
    cv2.imshow('otro', image_copy2)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

image1.release()

cv2.destroyAllWindows()