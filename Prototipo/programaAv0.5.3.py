import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0)

#Medidas de grilla, pixeles x distancia ,proximamente modificar
espacioGrilla = 10
pxm = 0
#arr de variables a guardar
savedPoints = []
distancias = []
#flags de comprobacion
liness = 0
complete = True


def pixelsxmilimetros(d):
    global espacioGrilla, pxm
    pxm = espacioGrilla/d
    return pxm

def calcularMM(d):
    global pxm
    mm = pxm * d
    return mm
#Calcula la distancia entre 2 puntos
def calcular_distancia(punto1, punto2):
    x1, y1 = punto1
    x2, y2 = punto2
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia
#Guarda la posicion de los puntos(x,y) mas cercano donde se hace click 
def dibujando(event, x, y, flags, param):
    global liness
    if event == cv2.EVENT_LBUTTONDOWN:
        for contour in corners:
            esquina = contour.ravel()
            distance = calcular_distancia((x,y),esquina)            
            if distance >= -5 and distance <= 5:  # Tolerancia de 10 unidades                
                if liness < 8:        
                    savedPoints.append(esquina)
                    liness += 1
                    break

def dibujarLineas(puntos):
    global complete
    if len(puntos) % 2 == 0 and len(puntos) <= 8:
        for i in range(0, len(puntos), 2):
            punto_inicio = puntos[i]
            punto_fin = puntos[i + 1]
            distancia = calcular_distancia(punto_inicio, punto_fin)
            mm = calcularMM(distancia)
            distancias.append((punto_inicio, punto_fin, mm))
        
        if len(distancias) == 4:
            complete = False
    
def dibujarLineasciclo(img, diss):
    font = cv2.FONT_HERSHEY_SIMPLEX
    if diss:        
        for lineas in arr:
        x1,x2,distancia = lineas
        cv2.line(img,x1,x2,(0,255,255),2)
        cv2.putText(img,"{:.1f}".format(distancia),x1,font,1,(0,0,255),2,cv2.LINE_AA)

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
        dibujarLineas(frame, savedPoints)

    dibujarLineasciclo(frame,distancias)
    dibujar_circulos(savedPoints, frame)
    # Mostrar las esquinas detectadas
    cv2.imshow('Shi-tomasi Detecction', frame)

    # Salir del bucle si se presiona 'q'
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break
    
    # Limpia variables si apretas 'c'
    if tecla == ord('c'):
        savedPoints = []
        distancias = []
        liness = 0
        complete = True

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
