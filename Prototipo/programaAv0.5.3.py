import cv2
import numpy as np
import math


cap = cv2.VideoCapture(0)

block_size = 2
aperture_size = 3
k = 0.04

espacioGrilla = 10

savedPoints = []
savedPointsReserve = []
copySavedPoints = []
distancias = []
liness = 0
d1 = True
d2 = True
d3 = True
d4 = True
complete = True
pxm = 0

def pixelsxmilimetros(d):
    global espacioGrilla, pxm
    pxm = espacioGrilla/d
    return pxm

def calcularMM(d):
    global pxm
    mm = pxm * d
    return mm

def calcular_distancia(punto1, punto2):
    x1, y1 = punto1
    x2, y2 = punto2
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia

def dibujando(event, x, y, flags, param):
    global liness
    if event == cv2.EVENT_LBUTTONDOWN:
        for contour in corners:
            esquina = contour.ravel()
            distance = calcular_distancia((x,y),esquina)            
            if distance >= -5 and distance <= 5:  # Tolerancia de 10 unidades                
                if liness < 8:        
                    savedPointsReserve.append(esquina)
                    liness += 1
                    break

def dibujarLineas(image_copy3,copySavedPoint):
    font = cv2.FONT_HERSHEY_SIMPLEX
    global d1,d2,d3,d4,complete
    if len(copySavedPoint) == 2 and d1:
        distancia = calcular_distancia(copySavedPoint[0], copySavedPoint[1])        
        ancho = pixelsxmilimetros(distancia)
        mm = calcularMM(distancia)
        distancias.append((copySavedPoint[0],copySavedPoint[1],mm))
        print(ancho)
        d1 = False
    elif len(copySavedPoint) == 4 and d2:
        distancia = calcular_distancia(copySavedPoint[2], copySavedPoint[3])
        mm = calcularMM(distancia)
        distancias.append((copySavedPoint[2],copySavedPoint[3],mm))
        d2 = False
    elif len(copySavedPoint) == 6 and d3:
        distancia = calcular_distancia(copySavedPoint[4], copySavedPoint[5])
        mm = calcularMM(distancia)
        distancias.append((copySavedPoint[4],copySavedPoint[5],mm))
        d3 = False
    elif len(copySavedPoint) == 8 and d4:
        distancia = calcular_distancia(copySavedPoint[6], copySavedPoint[7])
        mm = calcularMM(distancia)
        distancias.append((copySavedPoint[6],copySavedPoint[7],mm))
        complete = False
        d4 = False

def dibujarLineasciclo(image_copy3, diss):
    font = cv2.FONT_HERSHEY_SIMPLEX
    if diss:
        if len(diss) == 1:
            x1,x2,distancia = diss[0]
            cv2.line(image_copy3,x1,x2,(0,255,255),2)
            cv2.putText(image_copy3,"{:.1f}".format(distancia),x1,font,1,(0,0,255),2,cv2.LINE_AA)
        elif len(diss) == 2:
            x1,x2,distancia = diss[0]
            cv2.line(image_copy3,x1,x2,(0,255,255),2)
            cv2.putText(image_copy3,"{:.1f}".format(distancia),x1,font,1,(0,0,255),2,cv2.LINE_AA)
            x1,x2,distancia = diss[1]
            cv2.line(image_copy3,x1,x2,(0,255,255),2)
            cv2.putText(image_copy3,"{:.1f}".format(distancia),x1,font,1,(0,0,255),2,cv2.LINE_AA)
        elif len(diss) == 3:
            x1,x2,distancia = diss[0]
            cv2.line(image_copy3,x1,x2,(0,255,255),2)
            cv2.putText(image_copy3,"{:.1f}".format(distancia),x1,font,1,(0,0,255),2,cv2.LINE_AA)
            x1,x2,distancia = diss[1]
            cv2.line(image_copy3,x1,x2,(0,255,255),2)
            cv2.putText(image_copy3,"{:.1f}".format(distancia),x1,font,1,(0,0,255),2,cv2.LINE_AA)
            x1,x2,distancia = diss[2]
            cv2.line(image_copy3,x1,x2,(0,255,255),2)
            cv2.putText(image_copy3,"{:.1f}".format(distancia),x1,font,1,(0,0,255),2,cv2.LINE_AA)
        elif len(diss) == 4:
            x1,x2,distancia = diss[0]
            cv2.line(image_copy3,x1,x2,(0,255,255),2)
            cv2.putText(image_copy3,"{:.1f}".format(distancia),x1,font,1,(0,0,255),2,cv2.LINE_AA)
            x1,x2,distancia = diss[1]
            cv2.line(image_copy3,x1,x2,(0,255,255),2)
            cv2.putText(image_copy3,"{:.1f}".format(distancia),x1,font,1,(0,0,255),2,cv2.LINE_AA)
            x1,x2,distancia = diss[2]
            cv2.line(image_copy3,x1,x2,(0,255,255),2)
            cv2.putText(image_copy3,"{:.1f}".format(distancia),x1,font,1,(0,0,255),2,cv2.LINE_AA)
            x4,y4,distancia = diss[3]
            cv2.line(image_copy3,x4,y4,(0,255,255),2)  
            cv2.putText(image_copy3,"{:.1f}".format(distancia),x4,font,1,(0,0,255),2,cv2.LINE_AA)      


         

def dibujar_circulos(pintados,img):
    for circle in pintados:
        cv2.circle(img, circle, 5, (0, 0, 255), -1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir el cuadro a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.01, minDistance=10)

    # Convertir las coordenadas de los puntos a números enteros
    corners = np.int0(corners)

    # Dibujar círculos alrededor de las esquinas detectadas
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

    cv2.namedWindow('Shi-tomasi Detecction')
    cv2.setMouseCallback('Shi-tomasi Detecction',dibujando)
    if complete:
        dibujarLineas(frame, savedPointsReserve)

    dibujarLineasciclo(frame,distancias)
    dibujar_circulos(savedPointsReserve, frame)
    # Mostrar las esquinas detectadas
    cv2.imshow('Shi-tomasi Detecction', frame)

    # Salir del bucle si se presiona 'q'
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    if k == ord('c'):
        savedPoints = []
        savedPointsReserve = []
        copySavedPoints = []
        distancias = []
        liness = 0
        d1 = True
        d2 = True
        d3 = True
        d4 = True
        complete = True

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
