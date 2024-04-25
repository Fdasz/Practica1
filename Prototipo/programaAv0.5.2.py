import cv2
import numpy as np
import math
#import date
# Función para dibujar puntos en los vértices de los contornos
def dibujar_puntos(image, contours):
    for contour in contours:
        for vertex in contour:
            x, y = vertex[0]
            cv2.circle(image, (x, y), 5, (0, 0, 255), -1)

# Iniciar la captura de video desde la cámara predeterminada
cap = cv2.VideoCapture(0)

block_size = 2
aperture_size = 3
k = 0.04

savedPoints = []
savedPointsReserve = []
copySavedPoints = []
distancias = []
liness = 0

def calcular_distancia(punto1, punto2):
        x1, y1 = punto1
        x2, y2 = punto2
        distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distancia

def dibujando(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            for contour in corners:
                esquina = contour.ravel()
                distance = calcular_distancia((x,y),esquina)
                if distance >= -5 and distance <= 5:  # Tolerancia de 10 unidades
                    savedPointsReserve.append(esquina)
                    break

def dibujarLineas(image_copy3,copySavedPoint):
    perimetro = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    if len(copySavedPoint) == 2:
        distancia = calcular_distancia(copySavedPoint[0], copySavedPoint[1])
        perimetro = perimetro + distancia  
        cv2.line(image_copy3,copySavedPoint[0],copySavedPoint[1],(0,255,255),2)
        cv2.putText(image_copy3,"{:.3f}".format(distancia),copySavedPoint[0],font,1,(0,0,255),2,cv2.LINE_AA)
        if len(distancias) <= 3:
            distancias.append((copySavedPoint[0],copySavedPoint[1]))
def dibujarLineasciclo(image_copy3, dist):
    font = cv2.FONT_HERSHEY_SIMPLEX
    for line in dist:
        punto1,punto2,diss = line 
        cv2.line(image_copy3,punto1,punto2,(0,255,255),2)
        cv2.putText(image_copy3,"{:.3f}".format(diss),punto1,font,1,(0,0,255),2,cv2.LINE_AA)
def lineas4(event, x, y, flags, param):
    if liness < 4:
        dibujarLineas(event, x, y, flags, param)
        i+=1



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
    cv2.setMouseCallback('Shi-tomasi Detecction',lineas4)
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

# Liberar recursos
cap.release()
cv2.destroyAllWindows()