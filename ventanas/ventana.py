from tkinter import *
from tkinter import ttk

# Código lobby
lobby = Tk()
lobby.title("Primera lobby")
lobby.geometry("450x200")
lobby.resizable(1, 1)

def abrir_ventanaCrecer():
    ventanaCrecer = Toplevel(lobby)
    ventanaCrecer.title("Crecer")
    ventanaCrecer.geometry("300x300")

    def seleccionar_opcion(event, combobox):
        seleccion = combobox.get()
        print("Opción seleccionada:", seleccion)

    # Texto 1
    texto1 = Label(ventanaCrecer, text="Tamaño de la grilla")
    texto1.grid(row=0, column=5, padx=(75,0), pady=15)

    # Combobox 1
    combobox1 = ttk.Combobox(ventanaCrecer, values=["Opción 1", "Opción 2", "Opción 3", "Opción 4"])
    combobox1.bind("<<ComboboxSelected>>", lambda event: seleccionar_opcion(event, combobox1))
    combobox1.grid(row=1, column=5, padx=(75,0), pady=15)

    # Texto 2
    texto2 = Label(ventanaCrecer, text="Tiempo de Muestreo")
    texto2.grid(row=2, column=5, padx=(75,0), pady=15)

    # Combobox 2
    combobox2 = ttk.Combobox(ventanaCrecer, values=["Opción A", "Opción B", "Opción C", "Opción D"])
    combobox2.bind("<<ComboboxSelected>>", lambda event: seleccionar_opcion(event, combobox2))
    combobox2.grid(row=3, column=5, padx=(75,0), pady=15)

    siguiente_button = Button(ventanaCrecer, text="Siguiente", command=camaraLenta)
    siguiente_button.grid(row=4, column=5, padx=(75,0), pady=15)

def abrir_ventanaRomper():
    global ventanaRomper
    ventanaRomper = Toplevel(lobby)
    ventanaRomper.title("Romper")
    ventanaRomper.geometry("300x300")

    def seleccionar_opcion(event, combobox):
        seleccion = combobox.get()
        print("Opción seleccionada:", seleccion)

    # Texto 1
    texto1 = Label(ventanaRomper, text="Tamaño de la grilla")
    texto1.grid(row=0, column=0, padx=(75,0), pady=15)

    # Combobox 1
    combobox1 = ttk.Combobox(ventanaRomper, values=["Opción 1", "Opción 2", "Opción 3", "Opción 4"])
    combobox1.bind("<<ComboboxSelected>>", lambda event: seleccionar_opcion(event, combobox1))
    combobox1.grid(row=1, column=0, padx=(75,0), pady=15)

    # Texto 2
    texto2 = Label(ventanaRomper, text="Tiempo de Muestreo")
    texto2.grid(row=2, column=0, padx=(75,0), pady=15)

    # Combobox 2
    combobox2 = ttk.Combobox(ventanaRomper, values=["Opción A", "Opción B", "Opción C", "Opción D"])
    combobox2.bind("<<ComboboxSelected>>", lambda event: seleccionar_opcion(event, combobox2))
    combobox2.grid(row=3, column=0, padx=(75,0), pady=15)
    
    siguiente_button = Button(ventanaRomper, text="Siguiente", command=camaraRapida)
    siguiente_button.grid(row=4, column=0, padx=(75,0), pady=15)

def camaraRapida():
    print("prueba")
    ##codigo de la camara rapida se abre desde romper
    
def camaraLenta():
    print("prueba camara 2")
    ##codigo camara lenta se abre desde crecer
    
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
