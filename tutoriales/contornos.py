import cv2

image1 = cv2.imread('fotoaaa.jpg')
img_gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
 
ret, thresh1 = cv2.threshold(img_gray1, 150, 255, cv2.THRESH_BINARY)
contours2, hierarchy2 = cv2.findContours(thresh1, cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)
image_copy2 = image1.copy()


        
cv2.drawContours(image_copy2, contours2, -1, (0, 255, 0), 2, cv2.LINE_AA)

print(contours2)
def dibujando(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        for contour in contours2:
            distance = cv2.pointPolygonTest(contour, (x, y), True)
            if distance >= -15 and distance <= 15:  # Tolerancia de 10 unidades
                cv2.circle(image_copy2, (x, y), 10, (255, 0, 0), -1)
                break
            

cv2.namedWindow('SIMPLE Approximation contours')
cv2.setMouseCallback('SIMPLE Approximation contours',dibujando)

#image_copy3 = image1.copy()
#for i, contour in enumerate(contours2): # loop over one contour area
#   for j, contour_point in enumerate(contour): # loop over the points
#       # draw a circle on the current contour coordinate
#       cv2.circle(image_copy3, ((contour_point[0][0], contour_point[0][1])), 2, (0, 255, 0), 2, cv2.LINE_AA)
# see the results

#cv2.imshow('CHAIN_APPROX_SIMPLE Point only', image_copy3)
while True:
    cv2.imshow('SIMPLE Approximation contours', image_copy2)
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27: #salir
        break

cv2.destroyAllWindows()