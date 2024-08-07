import cv2
import numpy as np
import math
import time 
import threading
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Inicia la captura de la cámara
cap = cv2.VideoCapture(0)
# Medidas de grilla, pixeles x distancia ,proximamente modificar
espacioGrilla = 10
pxm = 0
# Variables para guardar
savedPoints = []
distancias = []
inicialPoint = []
tiempoInicial = time.time()
# Flags de comprobación

complete = True
d1 = True
d2 = True
d3 = True
d4 = True
experimento = False

# Calcula la relación pixeles por milímetro en base a una distancia inicial
def pixelsXmilimetros(d):
    global espacioGrilla, pxm
    pxm = espacioGrilla/d

# Calcula la distancia en milímetros
def calcularMM(d):
    global pxm
    mm = pxm * d
    return mm

# Calcula la distancia entre 2 puntos
def calcularDistancia(punto1, punto2):
    x1, y1 = punto1
    x2, y2 = punto2
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia

# Guarda la posición de los puntos (x, y) más cercano donde se hace click, máximo 8
def guardarPuntos(event, x, y, flags, param):
    global inicialPoint, savedPoints
    if event == cv2.EVENT_LBUTTONDOWN:
        for contour in corners:
            esquina = contour.ravel()
            distance = calcularDistancia((x, y), esquina)            
            if distance >= -5 and distance <= 5:  # Tolerancia de 10 unidades                
                if len(savedPoints) < 8:        
                    savedPoints.append(esquina)
                    break

    if event == cv2.EVENT_RBUTTONDOWN:
        for contour in corners:
            esquina = contour.ravel()
            distance = calcularDistancia((x, y), esquina)            
            if distance >= -5 and distance <= 5: 
                if len(inicialPoint) < 2:
                    inicialPoint.append((x, y))
                    if len(inicialPoint) == 2:
                        distancia = calcularDistancia(inicialPoint[0], inicialPoint[1])
                        pixelsXmilimetros(distancia)
                        break
                    break
                elif len(inicialPoint) == 3:
                    inicialPoint = []
                    inicialPoint.append((x, y))
                    break

# Calcula los extremos de los puntos junto con la distancia en milímetros
def calculaLineas(puntos):
    global d1, d2, d3, d4, complete, distancias
    arrlenght = len(puntos)
    if arrlenght == 2 and d1:
        distancia = calcularDistancia(puntos[0], puntos[1])
        distancia = calcularMM(distancia)
        distancias.append((puntos[0], puntos[1], distancia))
        d1 = False
    elif arrlenght == 4 and d2:
        distancia = calcularDistancia(puntos[2], puntos[3])
        distancia = calcularMM(distancia)
        distancias.append((puntos[2], puntos[3], distancia))
        d2 = False
    elif arrlenght == 6 and d3:
        distancia = calcularDistancia(puntos[4], puntos[5])
        distancia = calcularMM(distancia)
        distancias.append((puntos[4], puntos[5], distancia))
        d3 = False
    elif arrlenght == 8 and d4:
        distancia = calcularDistancia(puntos[6], puntos[7])
        distancia = calcularMM(distancia)
        distancias.append((puntos[6], puntos[7], distancia))
        complete = False
        d4 = False

# Dibuja líneas con los extremos de los puntos
def dibujarLineas(img):
    font = cv2.FONT_HERSHEY_SIMPLEX
    global distancias
    if distancias:
        for lineas in distancias:
            x1, x2, distancia = lineas
            cv2.line(img, x1, x2, (0, 255, 255), 2)
            cv2.putText(img, "{:.1f}".format(distancia), x1, font, 1, (0, 0, 255), 2, cv2.LINE_AA)

# Dibuja en cámara la posición marcada
def dibujarCirculos(pintados, img):
    for circle in pintados:
        cv2.circle(img, circle, 5, (0, 0, 255), -1)

def iniciarExperimento(cruces):
    global experimento, distancias, tiempoInicial
    experimento = True
    tiempoActual = time.time() - tiempoInicial
    minutos, segundos = divmod(tiempoActual, 60)
    x1,y1,dis1 = distancias[0]
    x1,y1,dis2 = distancias[1]
    x1,y1,dis3= distancias[2]
    x1,y1,dis4= distancias[3]
    with open("datosResumidos.txt", "a") as archivo:
        archivo.write(f"{dis1} {dis2} {dis3} {dis4} {int(minutos)}:{segundos:.2f}\n")

    with open("datosRaw.txt", "a") as archivo1:
        archivo1.write(f"{distancias[0]} {distancias[1]} {distancias[2]} {distancias[3]} {int(minutos)}:{segundos:.2f}\n")  

def calcularLineasLoop():
    global savedPoints, distancias
    distancias = []
    if savedPoints:
        
        distancia = calcularDistancia(savedPoints[0], savedPoints[1])
        distancia = calcularMM(distancia)
        distancias.append((savedPoints[0],savedPoints[1],distancia))

        distancia = calcularDistancia(savedPoints[2], savedPoints[3])
        distancia = calcularMM(distancia)
        distancias.append((savedPoints[2],savedPoints[3],distancia))

        distancia = calcularDistancia(savedPoints[4], savedPoints[5])
        distancia = calcularMM(distancia)
        distancias.append((savedPoints[4],savedPoints[5],distancia))

        distancia = calcularDistancia(savedPoints[6], savedPoints[7])
        distancia = calcularMM(distancia)
        distancias.append((savedPoints[6],savedPoints[7],distancia))

def seguirPunto(corners):
    global savedPoints
    if savedPoints:
        for i in range(len(savedPoints)):
            for point in corners:
                dis = calcularDistancia(tuple(point[0]), tuple(savedPoints[i]))
                if dis <=13:
                    savedPoints[i] = point[0]
                    break

# Ciclo de fotogramas cámara programa 
def iniciarCaptura():
    global corners, savedPoints, distancias, inicialPoint, complete, pxm, d1, d2, d3, d4, experimento, tiempoInicial
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir el cuadro a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Calcular las esquinas del cuadro
        corners = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.01, minDistance=20)

        if corners is not None:
            # Convertir las coordenadas de los puntos a números enteros
            corners = np.intp(corners)

            # Dibujar círculos alrededor de las esquinas detectadas
            for corner in corners:
                x, y = corner.ravel()
                cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

        cv2.namedWindow('Grilla')
        cv2.setMouseCallback('Grilla', guardarPuntos)
        if complete:
            calculaLineas(savedPoints)
        # Ciclo de dibujo
        if not complete:
            print("entro")
            calcularLineasLoop()

        # Ciclo de dibujo
        dibujarLineas(frame)
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
        
        # Inicia la toma de muestras y las guarda en un archivo
        if tecla == ord('i'):
            experimento = True
            tiempoInicial = time.time()
            archivo = open("datosResumidos.txt", "w")
            archivo.close()
            archivo = open("datosRaw.txt", "w")
            archivo.close()

        if tecla == ord('w'):
            experimento = False

        # Limpia variables si apretas 'c'
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
import tkinter as tk
import tkinter.messagebox as messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


def mostrarDatos():
    try:
        # Leer el archivo y extraer los datos
        with open('datosResumidos.txt', 'r') as file:
            lines = file.readlines()

        # Separar los datos de posición y tiempo
        tiempos = []
        distancias1 = []
        distancias2 = []
        distancias3 = []
        distancias4 = []

        # Procesar las líneas para extraer tiempo en segundos y posición
        for line in lines:
            parts = line.split()
            try:
                if len(parts) >= 5:
                    distancia1 = float(parts[0])
                    distancia2 = float(parts[1])
                    distancia3 = float(parts[2])
                    distancia4 = float(parts[3])
                    tiempo_str = parts[4]
                    minutos, segundos = map(float, tiempo_str.split(':'))
                    tiempo_total_segundos = minutos * 60 + segundos

                    # Agregar los datos a las listas
                    tiempos.append(tiempo_total_segundos)
                    distancias1.append(distancia1)
                    distancias2.append(distancia2)
                    distancias3.append(distancia3)
                    distancias4.append(distancia4)
                else:
                    print(f"Línea con datos insuficientes: {line}")
            except Exception as e:
                print(f"Error al procesar la línea: {line}. Error: {e}")
                continue

        # Verificar que las listas no estén vacías
        if not tiempos or not distancias1:
            messagebox.showerror("Error", "No hay datos suficientes para mostrar el gráfico.")
            return

        # Crear una nueva ventana para los gráficos
        grafico_ventana = tk.Toplevel()
        grafico_ventana.title("Gráfico de Datos")

        # Crear figura de Matplotlib
        fig = plt.figure(figsize=(10, 6))
        plot = fig.add_subplot(1, 1, 1)

        # Graficar los datos
        plot.plot(tiempos, distancias1, marker='o', linestyle='-', color='b', label='Distancia 1')
        plot.plot(tiempos, distancias2, marker='o', linestyle='-', color='g', label='Distancia 2')
        plot.plot(tiempos, distancias3, marker='o', linestyle='-', color='r', label='Distancia 3')
        plot.plot(tiempos, distancias4, marker='o', linestyle='-', color='c', label='Distancia 4')

        plot.set_title('Distancias vs Tiempo')
        plot.set_xlabel('Tiempo (s)')
        plot.set_ylabel('Distancia (mm)')
        plot.grid(True)
        plot.legend()

        # Ajustar los límites de los ejes
        plot.set_xlim(0, max(tiempos))  # Empieza el tiempo desde 0
        plot.set_ylim(min(min(distancias1), min(distancias2), min(distancias3), min(distancias4)) - 1,
                      max(max(distancias1), max(distancias2), max(distancias3), max(distancias4)) + 1)

        # Mostrar el gráfico en la nueva ventana
        canvas = FigureCanvasTkAgg(fig, master=grafico_ventana)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo datosResumidos.txt no se encontró.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

# Llamada a la función (asegúrate de llamarla en el lugar adecuado de tu programa)
# mostrarDatos()

def mostrarAyuda():
    # Crear una nueva ventana de ayuda
    ayuda_ventana = tk.Toplevel()
    ayuda_ventana.title("Ayuda")
    ayuda_ventana.geometry("1100x500")

    # Crear un widget Text para mostrar el texto de ayuda
    text_ayuda = tk.Text(ayuda_ventana, wrap='word')
    text_ayuda.pack(expand=True, fill='both')

    # Agregar una barra de desplazamiento
    scroll = ttk.Scrollbar(ayuda_ventana, command=text_ayuda.yview)
    scroll.pack(side='right', fill='y')
    text_ayuda['yscrollcommand'] = scroll.set

    # Texto de ayuda
    ayuda_texto = """
        Esta es la ventana de ayuda.
        
        1.Para poder usar el programa, al iniciar la camara debera hacer click derecho para
        establecer la distancia de 10 mm.
        
        2.Una vez hecho esto debera determinar los puntos a examinar, haciendo click izquierdo sobre los puntos verdes.

        3.Una vez tengo los 4 pares de puntos, al apretar la tecla "i" se empezara a guardar los datos en un archivo txt
        el cual quedara guardado en la locacion del programa.

        3,5.Si se equivoco al momento de elegir los puntos o al momento de establecer la distancia la tecla "c" devuelve todo a los
        valores a cero.

        4.Al terminar la prueba la ventana de la camara se cierra con apretar la tecla "esc".

        5.Si quiere checkear los datos en forma de grafico, apretar el bóton mostrar datos.
        """
    
    # Insertar el texto de ayuda en el widget Text
    text_ayuda.insert('1.0', ayuda_texto)
    # Hacer que el texto no sea editable
    text_ayuda.config(state='disabled')

# Crear ventana principal con Tkinter
root = tk.Tk()
root.geometry("500x300")
root.title("Lobby")

# Crear un marco para la cámara y el botón
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

# Etiqueta para mostrar la cámara
label = ttk.Label(frame)
label.pack()

# Botón para iniciar la captura de la cámara
boton_iniciar = ttk.Button(frame, text="Iniciar Cámara", width=15, command=iniciarCapturaThread)
boton_iniciar.pack(padx=10, pady=20)

# Botón para abrir el archivo y mostrar los gráficos
boton_mostrar_datos = ttk.Button(frame, text="Mostrar Datos", width=15, command=mostrarDatos)
boton_mostrar_datos.pack(padx=10, pady=20)

boton_ayuda = ttk.Button(frame, text="Ayuda", width=15, command=mostrarAyuda)
boton_ayuda.pack(padx=10, pady=20)

# Iniciar el bucle principal de Tkinter
root.mainloop()
