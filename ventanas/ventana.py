import tkinter as tk
from tkinter import *
from tkinter import ttk
import cv2
import numpy as np
import math

# Código lobby
lobby = Tk()
lobby.title("Primer lobby")
lobby.geometry("450x200")
lobby.resizable(0, 0)

def camaraRapida(opcion_grilla, opcion_tiempo, opcion_probeta):
    probeta = int(opcion_probeta)  # Convertir opcion_probeta a entero

    if probeta < 0:
        print("Error al seleccionar la probeta")
        exit()
        
    # Escribir los valores en un archivo de texto
    with open("datos_romper.txt", "w") as archivo:
        archivo.write("Tamaño de la grilla seleccionado: {}\n".format(opcion_grilla))
        archivo.write("Tiempo de muestreo seleccionado: {}\n".format(opcion_tiempo))
        archivo.write("Probeta seleccionada: {}\n".format(probeta))

    print("Datos guardados en 'datos_romper.txt'")

    ventanaRapida = Toplevel(lobby)
    ventanaRapida.title("Rapida")
    ventanaRapida.geometry("1200x800")

    botonTerminar = Button(ventanaRapida, text="Terminar", width=15, height=2, command=abrir_ventanaCrecer)
    botonTerminar.grid(row=20, column=250, padx=50, pady=(400, 15))


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

    ventanaCrecer2 = Toplevel(lobby)
    ventanaCrecer2.title("Crecer")
    ventanaCrecer2.geometry("1200x800")
    
    #Botones // cambiar comando a funcion del programa
    botonPunto1 = Button(ventanaCrecer2, text="Asignar", width=15, height=2, command=abrir_ventanaCrecer)
    botonPunto2 = Button(ventanaCrecer2, text="Asignar", width=15, height=2, command=abrir_ventanaRomper)
    botonPunto3 = Button(ventanaCrecer2, text="Asignar", width=15, height=2, command=abrir_ventanaCrecer)
    botonPunto4 = Button(ventanaCrecer2, text="Asignar", width=15, height=2, command=abrir_ventanaRomper)
    botonSiguienteV = Button(ventanaCrecer2, text="Siguiente", width=15, height=2, command=muestraCrecer(ventanaCrecer2))
    botonPunto1.grid(row=200, column=50, padx=10, pady=(0, 15))
    botonPunto2.grid(row=200, column=100, padx=50, pady=(0, 15))
    botonPunto3.grid(row=200, column=150, padx=50, pady=(0, 15))
    botonPunto4.grid(row=200, column=200, padx=50, pady=(0, 15))
    botonSiguienteV.grid(row=20, column=250, padx=50, pady=(400, 15))
    
    #Texto que cambia segun los puntos elegidos
    textoPunto1 = tk.Text(ventanaCrecer2, wrap="word", height=5, width=30)
    textoPunto2 = tk.Text(ventanaCrecer2, wrap="word", height=5, width=30)
    textoPunto3 = tk.Text(ventanaCrecer2, wrap="word", height=5, width=30)
    textoPunto4 = tk.Text(ventanaCrecer2, wrap="word", height=5, width=30)
    #Posicion del texto
    textoPunto1.grid(row=199, column=50,padx=10, pady=(100, 15))
    textoPunto2.grid(row=199, column=100,padx=20, pady=(100, 15))
    textoPunto3.grid(row=199, column=150,padx=20, pady=(100, 15))
    textoPunto4.grid(row=199, column=200,padx=20, pady=(100, 15))
    
    textoPunto1.configure(state="disabled")
    textoPunto2.configure(state="disabled")
    textoPunto3.configure(state="disabled")
    textoPunto4.configure(state="disabled")
    
    #añadir el def que haga que se escriban segun los puntos

def muestraCrecer(ventanaActual):
    ventanaActual.withdraw()
    ventanaMuestraC = Toplevel(lobby)
    ventanaMuestraC.title("Crecer Muestra")
    ventanaMuestraC.geometry("1200x800")
    
    
    #boton
    #cambiar a funcion siguiente
    botonTerminar = Button(ventanaMuestraC, text="Terminar", width=15, height=2, command=graficosLento)
    botonTerminar.grid(row=20, column=250, padx=50, pady=(400, 15))
    
    #textos
    textoPunto1 = tk.Text(ventanaMuestraC, wrap="word", height=5, width=30)
    textoPunto2 = tk.Text(ventanaMuestraC, wrap="word", height=5, width=30)
    textoPunto3 = tk.Text(ventanaMuestraC, wrap="word", height=5, width=30)
    textoPunto4 = tk.Text(ventanaMuestraC, wrap="word", height=5, width=30)
    #Posicion del texto
    textoPunto1.grid(row=199, column=50,padx=10, pady=(100, 15))
    textoPunto2.grid(row=199, column=100,padx=20, pady=(100, 15))
    textoPunto3.grid(row=199, column=150,padx=20, pady=(100, 15))
    textoPunto4.grid(row=199, column=200,padx=20, pady=(100, 15))
    
    textoPunto1.configure(state="disabled")
    textoPunto2.configure(state="disabled")
    textoPunto3.configure(state="disabled")
    textoPunto4.configure(state="disabled")

    
def abrir_ventanaCrecer():
    ventanaCrecer = Toplevel(lobby)
    ventanaCrecer.title("Crecer")
    ventanaCrecer.geometry("300x400")

    # Texto 1
    texto1 = Label(ventanaCrecer, text="Tamaño de la grilla")
    texto1.grid(row=0, column=5, padx=(75,0), pady=15)

    # Combobox 1
    combobox1 = ttk.Combobox(ventanaCrecer, values=["Opción 1", "Opción 2", "Opción 3", "Opción 4"])
    combobox1['state'] = 'readonly'
    combobox1.grid(row=1, column=5, padx=(75,0), pady=15)

    # Texto 2
    texto2 = Label(ventanaCrecer, text="Tiempo de Muestreo")
    texto2.grid(row=2, column=5, padx=(75,0), pady=15)

    # Combobox 2
    combobox2 = ttk.Combobox(ventanaCrecer, values=["Opción A", "Opción B", "Opción C", "Opción D"])
    combobox2['state'] = 'readonly'
    combobox2.grid(row=3, column=5, padx=(75,0), pady=15)

    etiqueta_probeta = Label(ventanaCrecer, text="Probeta")
    etiqueta_probeta.grid(row=4, column=5, padx=(75,0), pady=15)

    entrada_probeta = Entry(ventanaCrecer)
    entrada_probeta.grid(row=5, column=5, padx=(75,0), pady=15)
    
    siguiente_button = Button(ventanaCrecer, text="Siguiente", command=lambda: abrirSiguienteVentanaLenta(ventanaCrecer, combobox1.get(), combobox2.get(), entrada_probeta.get()))
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
    combobox1['state'] = 'readonly'
    combobox1.grid(row=1, column=0, padx=(75,0), pady=15)

    # Texto 2
    texto2 = Label(ventanaRomper, text="Tiempo de Muestreo")
    texto2.grid(row=2, column=0, padx=(75,0), pady=15)

    # Combobox 2
    combobox2 = ttk.Combobox(ventanaRomper, values=["Opción A", "Opción B", "Opción C", "Opción D"])
    combobox2['state'] = 'readonly'
    combobox2.grid(row=3, column=0, padx=(75,0), pady=15)

    etiqueta_probeta = Label(ventanaRomper, text="Probeta")
    etiqueta_probeta.grid(row=4, column=0, padx=(75,0), pady=15)

    entrada_probeta = Entry(ventanaRomper)
    entrada_probeta.grid(row=5, column=0, padx=(75,0), pady=15)

    siguiente_button = Button(ventanaRomper, text="Siguiente", command=lambda: camaraRapida(ventanaRomper, combobox1.get(), combobox2.get(), entrada_probeta.get()))
    siguiente_button.grid(row=6, column=0, padx=(75,0), pady=15)


def graficosLento():
    #ventana
    ventanaGraficosL = Toplevel(lobby)
    ventanaGraficosL.title("Graficos")
    ventanaGraficosL.geometry("300x400")
    
    #boton
    botonTerminar = Button(ventanaGraficosL, text="Terminar", width=15, height=2, command=graficosLento)
    botonTerminar.grid(row=20, column=250, padx=50, pady=(400, 15))

def abrirSiguienteVentanaLenta(ventana_actual, opcion_grilla, opcion_tiempo, opcion_probeta):
    ventana_actual.withdraw()  # Ocultar la ventana actual
    camaraLenta(opcion_grilla, opcion_tiempo, opcion_probeta)
    
def abrirSiguienteVentanaRapida(ventana_actual, opcion_grilla, opcion_tiempo, opcion_probeta):
    ventana_actual.withdraw()  # Ocultar la ventana actual
    camaraRapida(opcion_grilla, opcion_tiempo, opcion_probeta)
        
# Botones lobby
botonCrecer = Button(lobby, text="Crecer", width=15, height=2, command=abrir_ventanaCrecer)
botonRomper = Button(lobby, text="Romper", width=15, height=2, command=abrir_ventanaRomper)
botonCrecer.grid(row=5, column=50, padx=50, pady=75)
botonRomper.grid(row=5, column=250, padx=50, pady=75)
    
lobby.mainloop()
