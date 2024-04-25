from tkinter import *
from tkinter import ttk
import cv2
import numpy as np
import math

# Código lobby
lobby = Tk()
lobby.title("Primera lobby")
lobby.geometry("450x200")
lobby.resizable(1, 1)

def camaraRapida(opcion_grilla, opcion_tiempo, opcion_probeta):
    opcion_probeta = int(opcion_probeta)  # Convertir opcion_probeta a entero

    if opcion_probeta < 0:
        print("Error al seleccionar la probeta")
        exit()
        
    # Escribir los valores en un archivo de texto
    with open("datos_romper.txt", "w") as archivo:
        archivo.write("Tamaño de la grilla seleccionado: {}\n".format(opcion_grilla))
        archivo.write("Tiempo de muestreo seleccionado: {}\n".format(opcion_tiempo))
        archivo.write("Probeta seleccionada: {}\n".format(opcion_probeta))

    print("Datos guardados en 'datos_romper.txt'")

    #Camara parte 3 ventana


def camaraLenta(opcion_grilla, opcion_tiempo, opcion_probeta):
    opcion_probeta = int(opcion_probeta)  # Convertir opcion_probeta a entero

    if opcion_probeta < 0:
        print("Error al seleccionar la probeta")
        exit()
        
    # Escribir los valores en un archivo de texto
    with open("datos_crecer.txt", "w") as archivo:
        archivo.write("Tamaño de la grilla seleccionado: {}\n".format(opcion_grilla))
        archivo.write("Tiempo de muestreo seleccionado: {}\n".format(opcion_tiempo))
        archivo.write("Probeta seleccionada: {}\n".format(opcion_probeta))

    print("Datos guardados en 'datos_crecer.txt'")

    ventanaCrecer = Toplevel(lobby)
    ventanaCrecer.title("Crecer")
    ventanaCrecer.geometry("300x400")

def abrir_ventanaCrecer():
    ventanaCrecer = Toplevel(lobby)
    ventanaCrecer.title("Crecer")
    ventanaCrecer.geometry("300x400")

    # Texto 1
    texto1 = Label(ventanaCrecer, text="Tamaño de la grilla")
    texto1.grid(row=0, column=5, padx=(75,0), pady=15)

    # Combobox 1
    combobox1 = ttk.Combobox(ventanaCrecer, values=["Opción 1", "Opción 2", "Opción 3", "Opción 4"])

    combobox1.grid(row=1, column=5, padx=(75,0), pady=15)

    # Texto 2
    texto2 = Label(ventanaCrecer, text="Tiempo de Muestreo")
    texto2.grid(row=2, column=5, padx=(75,0), pady=15)

    # Combobox 2
    combobox2 = ttk.Combobox(ventanaCrecer, values=["Opción A", "Opción B", "Opción C", "Opción D"])
    combobox2.grid(row=3, column=5, padx=(75,0), pady=15)

    etiqueta_probeta = Label(ventanaCrecer, text="Probeta")
    etiqueta_probeta.grid(row=4, column=5, padx=(75,0), pady=15)

    entrada_probeta = Entry(ventanaCrecer)
    entrada_probeta.grid(row=5, column=5, padx=(75,0), pady=15)

    siguiente_button = Button(ventanaCrecer, text="Siguiente", command=lambda: camaraLenta(combobox1.get(), combobox2.get(), entrada_probeta.get()))
    siguiente_button.grid(row=6, column=5, padx=(75,0), pady=15)

def abrir_ventanaRomper():
    ventanaRomper = Toplevel(lobby)
    ventanaRomper.title("Romper")
    ventanaRomper.geometry("300x400")

    # Texto 1
    texto1 = Label(ventanaRomper, text="Tamaño de la grilla")
    texto1.grid(row=0, column=0, padx=(75,0), pady=15)

    # Combobox 1
    combobox1 = ttk.Combobox(ventanaRomper, values=["Opción 1", "Opción 2", "Opción 3", "Opción 4"])
    combobox1.grid(row=1, column=0, padx=(75,0), pady=15)

    # Texto 2
    texto2 = Label(ventanaRomper, text="Tiempo de Muestreo")
    texto2.grid(row=2, column=0, padx=(75,0), pady=15)

    # Combobox 2
    combobox2 = ttk.Combobox(ventanaRomper, values=["Opción A", "Opción B", "Opción C", "Opción D"])
    combobox2.grid(row=3, column=0, padx=(75,0), pady=15)

    etiqueta_probeta = Label(ventanaRomper, text="Probeta")
    etiqueta_probeta.grid(row=4, column=0, padx=(75,0), pady=15)

    entrada_probeta = Entry(ventanaRomper)
    entrada_probeta.grid(row=5, column=0, padx=(75,0), pady=15)

    siguiente_button = Button(ventanaRomper, text="Siguiente", command=lambda: camaraRapida(combobox1.get(), combobox2.get(), entrada_probeta.get()))
    siguiente_button.grid(row=6, column=0, padx=(75,0), pady=15)

def abrir_siguiente_ventana(ventana_actual, siguiente_ventana=None):
    if siguiente_ventana:
        ventana_actual.withdraw()  # Ocultar la ventana actual
        siguiente_ventana.deiconify()  # Mostrar la siguiente ventana
        
# Botones lobby
botonCrecer = Button(lobby, text="Crecer", width=15, height=2, command=abrir_ventanaCrecer)
botonRomper = Button(lobby, text="Romper", width=15, height=2, command=abrir_ventanaRomper)
botonCrecer.grid(row=5, column=50, padx=50, pady=75)
botonRomper.grid(row=5, column=250, padx=50, pady=75)
    
lobby.mainloop()
