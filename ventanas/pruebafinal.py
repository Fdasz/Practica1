import cv2
import numpy as np
import math
import time
import threading
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
#Inicia la captura de la camara
cap = cv2.VideoCapture(0)
#Medidas de grilla, pixeles x distancia ,proximamente modificar
espacioGrilla = 10
pxm = 0
#arr de variables a guardar
savedPoints = []
distancias = []
inicialPoint = []
tiempoInicial = 0
#flag de comprobacion
complete = True
d1 = True
d2 = True
d3 = True
d4 = True
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
    global d1,d2,d3,d4,complete,distancias
    arrlenght = len(puntos)
    if arrlenght == 2 and d1:
        distancia = calcularDistancia(puntos[0], puntos[1])
        distancia = calcularMM(distancia)
        distancias.append((puntos[0],puntos[1],distancia))
        d1 = False
    elif arrlenght == 4 and d2:
        distancia = calcularDistancia(puntos[2], puntos[3])
        distancia = calcularMM(distancia)
        distancias.append((puntos[2],puntos[3],distancia))
        d2 = False
    elif arrlenght == 6 and d3:
        distancia = calcularDistancia(puntos[4], puntos[5])
        distancia = calcularMM(distancia)
        distancias.append((puntos[4],puntos[5],distancia))
        d3 = False
    elif arrlenght == 8 and d4:
        distancia = calcularDistancia(puntos[6], puntos[7])
        distancia = calcularMM(distancia)
        distancias.append((puntos[6],puntos[7],distancia))
        complete = False
        d4 = False
#Dibuja lineas con los extremos de los puntos
def dibujarLineas(img):
    font = cv2.FONT_HERSHEY_SIMPLEX
    global distancias
    if distancias:
        for lineas in distancias:
            x1, x2, distancia = lineas
            cv2.line(img,x1,x2,(0,255,255),2)
            cv2.putText(img,"{:.1f}".format(distancia),x1,font,1,(0,0,255),2,cv2.LINE_AA)
#Dibuja en camara la posicion marcada
def dibujarCirculos(pintados,img):
    for circle in pintados:
        cv2.circle(img, circle, 5, (0, 0, 255), -1)

def seguirPunto(corners):
    global savedPoints
    if savedPoints:
        for point in corners:
            dis = calcularDistancia(tuple(point[0]), tuple(savedPoints[0]))
            if dis <=13:
                savedPoints[0] = point[0]
                break

def iniciarExperimento(cruces):
    global savedPoints, tiempoInicial
    tiempoActual = time.time() - tiempoInicial
    minutos, segundos = divmod(tiempoActual, 60)
    dis = calcularDistancia(savedPoints[0], savedPoints[1])
    with open("datosModa.txt", "a") as archivo:
        archivo.write(f"{savedPoints[0]} {savedPoints[1]} {dis} {int(minutos)}:{segundos:.2f}\n")

#Ciclo de fotogramas camara programa 
def iniciarCaptura():
    global corners, savedPoints, distancias, inicialPoint, complete, pxm, d1, d2, d3, d4, experimento,tiempoInicial
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir el cuadro a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Calculas las esquinas del cuadro
        corners = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.01, minDistance=20)

        # Convertir las coordenadas de los puntos a números enteros
    
        # Dibujar círculos alrededor de las esquinas detectadas
        if corners is not None:
            # Convertir las coordenadas de los puntos a números enteros
            corners = np.intp(corners)

            # Dibujar círculos alrededor de las esquinas detectadas
            for corner in corners:
                x, y = corner.ravel()
                cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
                
        cv2.namedWindow('Grilla')
        cv2.setMouseCallback('Grilla',guardarPuntos)
        if complete:
            calculaLineas(savedPoints)
        # Ciclo de dibujo
        #dibujarLineas(frame)

        dibujarCirculos(savedPoints, frame)

        seguirPunto(corners)

        # Mostrar las esquinas detectadas
        cv2.imshow('Grilla', frame)
        if experimento:
            iniciarExperimento(corners)

        # Salir del bucle si se presiona 'q'
        tecla = cv2.waitKey(5) & 0xFF
        if tecla == 27:
            break
        
        #inicia la toma de muestras y las guarda en un archivo
        if tecla == ord('i'):
            experimento = True
            tiempoInicial = time.time()
            archivo = open("datosModa.txt", "w")
            archivo.close()
            
        # Limpia variables si apretas 'c'
        if tecla == ord('w'):
            experimento = False


        if tecla == ord('c'):
            savedPoints = []
            distancias = []
            inicialPoint = []
            complete = True
            pxm = 0
            d1 = True
            d2 = True
            d3 = True
            d4 = True
    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()




def iniciarCapturaThread():
    thread = threading.Thread(target=iniciarCaptura)
    thread.daemon = True
    thread.start()

# Función para mostrar los datos en gráficos
def mostrarDatos():
    # Leer el archivo y extraer los datos
    with open('datosModa.txt', 'r') as file:
        lines = file.readlines()

    # Separar los datos de posición y tiempo
    tiempos = []
    posiciones = []

    # Procesar las líneas para extraer tiempo en segundos y posición
    for line in lines:
        parts = line.split()
        try:
            distancia = float(parts[4])
            tiempo_str = parts[5]
            minutos, segundos = map(float, tiempo_str.split(':'))
            tiempo_total_segundos = minutos * 60 + segundos

            # Agregar los datos a las listas
            tiempos.append(tiempo_total_segundos)
            posiciones.append(distancia)
        except Exception as e:
            print(f"Error al procesar la línea: {line}. Error: {e}")
            continue

    # Crear una nueva ventana para los gráficos
    grafico_ventana = tk.Toplevel()
    grafico_ventana.title("Gráfico de Datos")

    # Crear figura de Matplotlib
    fig = plt.figure(figsize=(10, 6))
    plot = fig.add_subplot(1, 1, 1)

    # Graficar los datos
    plot.plot(tiempos, posiciones, marker='o', linestyle='-', color='b')
    plot.set_title('Posición vs Tiempo')
    plot.set_xlabel('Tiempo (s)')
    plot.set_ylabel('Distancia (mm)')
    plot.grid(True)

    # Ajustar los límites de los ejes
    plot.set_xlim(0, max(tiempos))  # Empieza el tiempo desde 0
    plot.set_ylim(min(posiciones) - 1, max(posiciones) + 1)  # Ajusta la escala dinámicamente

    # Mostrar el gráfico en la nueva ventana
    canvas = FigureCanvasTkAgg(fig, master=grafico_ventana)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Crear ventana principal con Tkinter
root = tk.Tk()
root.geometry("200x200")
root.title("Lobby")

# Crear un marco para la cámara y el botón
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

# Etiqueta para mostrar la cámara
label = ttk.Label(frame)
label.pack()

# Botón para iniciar la captura de la cámara
boton_iniciar = ttk.Button(frame, text="Iniciar Cámara", width=15, command=iniciarCapturaThread)
boton_iniciar.pack(pady=20)

# Botón para abrir el archivo y mostrar los gráficos
boton_mostrar_datos = ttk.Button(frame, text="Mostrar Datos", width=15, command=mostrarDatos)
boton_mostrar_datos.pack(pady=20)

# Iniciar el bucle principal de Tkinter
root.mainloop()
