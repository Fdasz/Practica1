import cv2 
import math


image1 = cv2.VideoCapture(0)
image1.set(cv2.CAP_PROP_FPS, 20)
minCani = 50
maxCani = 150
savedPoints = []
savedPointsReserve = []
copySavedPoints = []

while True:
    # Lee un fotograma de la cámara
    ret, frame = image1.read()
    edges = cv2.Canny(frame,minCani,maxCani)
    img_gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    ret, thresh1 = cv2.threshold(img_gray1, 150, 255, cv2.THRESH_BINARY)
    th = cv2.medianBlur(thresh1, 7)
    contours2, hierarchy2 = cv2.findContours(th, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    image_copy2 = frame
    cv2.drawContours(image_copy2, contours2, -1, (0, 255, 0), 2, cv2.LINE_AA)
    image_copy3 = frame
    for i, contour in enumerate(contours2): # loop over one contour area
        for j, contour_point in enumerate(contour): # loop over the points
            # draw a circle on the current contour coordinate
            cv2.circle(image_copy3, ((contour_point[0][0], contour_point[0][1])), 2, (0, 255, 0), 2, cv2.LINE_AA)
    # see the results
    cv2.rectangle(frame , (0,0), (frame.shape[1],40), (0,0,0), -1)
    variablesCanny = str(minCani)
    cara = 'minCani: '+str(minCani)
    mesa = 'maxCani: '+ str(maxCani)
    
    for c in contours2:
      area = cv2.contourArea(c)
      peri = cv2.arcLength(c, True)
      approx = cv2.approxPolyDP(c, 0.02*peri, True)
      if area >= 200 and area <= 2000:
        if len(approx) == 4:
            cv2.drawContours(image_copy3, [approx], -1, (255, 0, 0), 2, cv2.LINE_AA)
    
    
    def dibujando(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            for contour in contours2:
                distance = cv2.pointPolygonTest(contour, (x, y), True)
                if distance >= -15 and distance <= 15:  # Tolerancia de 10 unidades
                    cv2.circle(image_copy2, (x, y), 10, (255, 0, 0), -1)
                    savedPointsReserve.append((x,y))
                    break
    def calcular_distancia(punto1, punto2):
        x1, y1 = punto1
        x2, y2 = punto2
        distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distancia
    def actualizarPunto():
        return print("actualizado")
    
    def dibujarLineas():
        perimetro = 0
        font = cv2.FONT_HERSHEY_SIMPLEX
        if len(copySavedPoints) >= 2:
            for ind,put in enumerate(copySavedPoints):
                if ind < len(copySavedPoints)-1:
                    distancia = calcular_distancia(put, copySavedPoints[ind+1])
                    perimetro = perimetro + distancia  
                    cv2.line(image_copy3,put,copySavedPoints[ind+1],(0,255,255),2)
                    cv2.putText(image_copy3,"{:.3f}".format(distancia),put,font,1,(0,0,255),2,cv2.LINE_AA)
                if ind == len(copySavedPoints)-1:
                    distancia = calcular_distancia(put, copySavedPoints[0])
                    perimetro = perimetro + distancia    
                    cv2.line(image_copy3,put,copySavedPoints[0],(0,255,255),2)
                    cv2.putText(image_copy3,"{:.3f}".format(distancia),put,font,1,(0,0,255),2,cv2.LINE_AA)
        return perimetro
                    
        
    savedPoints = savedPointsReserve[:]
    copySavedPoints = savedPointsReserve[:]
    for index, circle in enumerate(savedPoints):
        #print(savedPointsReserve)
        for contour in contours2:
            punto = [circle]            
            for point in contour:
                    
                disComp = calcular_distancia(point[0], punto[0])
                dis = calcular_distancia(point[0],circle)
                if disComp <= 10:
                    cv2.circle(image_copy3, punto[0], 10, (0, 0, 255), -1)
                    copySavedPoints[index] = tuple(point[0])
                        
                    break
                if dis >= -10 and dis < 10:
                    cv2.circle(image_copy3, tuple(point[0]), 10, (0, 0, 255), -1)
                    punto.remove(punto[0])
                    punto.append(tuple(point[0]))
                    savedPointsReserve[index] = tuple(point[0])
                    break 
                
    peri = dibujarLineas()
            

    cv2.namedWindow('CHAIN_APPROX_SIMPLE Point only')
    cv2.setMouseCallback('CHAIN_APPROX_SIMPLE Point only',dibujando)
    
    cv2.drawContours(image_copy3, [approx], -1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(image_copy3,"perimetro: " + str(peri),(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
    cv2.putText(image_copy3, mesa, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(image_copy3, cara, (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('CHAIN_APPROX_SIMPLE Point only', image_copy3)
    cv2.imshow('otro', thresh1)

    #aumenta y disminuye los valores de min/max de las variables de canny
    k = cv2.waitKey(5) & 0xFF

    if k == ord('a'):
        minCani += 1 
    if k == ord('s'):
        minCani -= 1 
    if k == ord('z'):
        maxCani += 1 
    if k == ord('x'):
        maxCani -= 1 
    if k == ord('c'):
        savedPoints = []
        savedPointsReserve = [] 


    if k == 27:
        break

image1.release()
