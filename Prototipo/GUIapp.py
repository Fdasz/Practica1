import tkinter as tk


ventana = tk.Tk()
ventana.title("Deformacion de materiales")
ventana.minsize(1000, 600)
ventana.resizable(0,0)

def exportar():
    print("me has encontrado")

BSeleccionar = tk.Button(ventana, text="Iniciar Camaras", bg="#d3dbde", fg="black")
BSeleccionar.place(x=440, y=25,width=120,height=23)

BExportar = tk.Button(ventana, text="Exportar",command=exportar , bg="#d3dbde", fg="black")
BExportar.place(x=999, y=590,width=100,height=23)

BBorrar = tk.Button(ventana, text='Calcular Angulo', bg="#d3dbde", fg="black")
BBorrar.place(x=530, y=415,width=200,height=23)

lienzoOG = tk.Canvas(ventana, width=480, height=360, background="grey")
lienzoOG.place(x=20,y=50) # 1

lienzo = tk.Canvas(ventana, width=480, height=360, background="grey")
lienzo.place(x=500,y=50) # 2

vector_count = 0


ventana.mainloop()