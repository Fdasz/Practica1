import cv2
import numpy as np
import math
import time 
#Inicia la captura de la camara
cap = cv2.VideoCapture(0)
#Medidas de grilla, pixeles x distancia ,proximamente modificar
espacioGrilla = 10
pxm = 0
#arr de variables a guardar
savedPoints = []
distancias = []
inicialPoint = []
#flag de comprobacion
complete = True
experimento = False

#Calcula la relacion pixeles por milimetro en base a una distancia inicial
def pixelsXmilimetros(d):
    global espacioGrilla, pxm
    pxm = espacioGrilla/d

#Calcula la distancia en milimetros
def calcularMM(d):
    global pxm
    mm = pxm * d
    return mm
#Calcula la distancia entre 2 puntos
def calcularDistancia(punto1, punto2):
    x1, y1 = punto1
    x2, y2 = punto2
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia
#Guarda la posicion de los puntos(x,y) mas cercano donde se hace click max: 8
def guardarPuntos(event, x, y, flags, param):
    global inicialPoint,savedPoints
    if event == cv2.EVENT_LBUTTONDOWN:
        for contour in corners:
            esquina = contour.ravel()
            distance = calcularDistancia((x,y),esquina)            
            if distance >= -5 and distance <= 5:  # Tolerancia de 10 unidades                
                if len(savedPoints) < 8:        
                    savedPoints.append(esquina)
                    break

    if event == cv2.EVENT_RBUTTONDOWN:
        for contour in corners:
            esquina = contour.ravel()
            distance = calcularDistancia((x,y),esquina)            
            if distance >= -5 and distance <= 5: 
                if len(inicialPoint) < 2:
                    inicialPoint.append((x,y))
                    if len(inicialPoint) == 2:
                        distancia = calcularDistancia(inicialPoint[0], inicialPoint[1])
                        pixelsXmilimetros(distancia)
                        break
                    break
                elif len(inicialPoint) == 3:
                    inicialPoint = []
                    inicialPoint.append((x,y))
                    break
#Calcula los extremos de los puntos junto con la distancia en milimetros
def calculaLineas(puntos):
    global complete
    if len(puntos) % 2 == 0 and len(puntos) <= 8:
        for i in range(0, len(puntos), 2):
            punto_inicio = puntos[i]
            punto_fin = puntos[i + 1]
            distancia = calcularDistancia(punto_inicio, punto_fin)
            mm = calcularMM(distancia)
            distancias.append((punto_inicio, punto_fin, mm))
        
        if len(distancias) == 4:
            complete = False
#Dibuja lineas con los extremos de los puntos
def dibujarLineas(img, diss):
    font = cv2.FONT_HERSHEY_SIMPLEX
    if diss:        
        for lineas in arr:
        x1,x2,distancia = lineas
        cv2.line(img,x1,x2,(0,255,255),2)
        cv2.putText(img,"{:.1f}".format(distancia),x1,font,1,(0,0,255),2,cv2.LINE_AA)
#Dibuja en camara la posicion marcada
def dibujarCirculos(pintados,img):
    for circle in pintados:
        cv2.circle(img, circle, 5, (0, 0, 255), -1)

def iniciarExperimento(cruces):
    global experimento
    experimento = True
    with open("datosModa.txt", "a") as archivo:
        archivo.write(f"{time.time()}}\n")
        for puntos in cruces:
            punto1,punto2 = puntos.ravel()
            archivo.write(f"{punto1},{punto2}\n")

#Ciclo de fotogramas camara programa 
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir el cuadro a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Calculas las esquinas del cuadro
    corners = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.01, minDistance=10)

    # Convertir las coordenadas de los puntos a números enteros
    corners = np.int0(corners)

    # Dibujar círculos alrededor de las esquinas detectadas
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

    cv2.namedWindow('Grilla')
    cv2.setMouseCallback('Grilla',guardarPuntos)
    if complete:
        calcularLineas(frame, savedPoints)
    # Ciclo de dibujo
    dibujarLineas(frame,distancias)
    dibujarCirculos(savedPoints, frame)
    # Mostrar las esquinas detectadas
    cv2.imshow('Grilla', frame)

    # Salir del bucle si se presiona 'q'
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break
    
    #inicia la toma de muestras y las guarda en un archivo
    if tecla == ord('i') or experimento:
        iniciarExperimento(corners)
    # Limpia variables si apretas 'c'
    if tecla == ord('c'):
        savedPoints = []
        distancias = []
        inicialPoint = []
        complete = True

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
