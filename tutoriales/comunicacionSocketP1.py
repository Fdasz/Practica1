import tkinter as tk 
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename
import serial
import time

ventana = tk.Tk()
ventana.geometry("485x354")
ventana.resizable(0,0)
ventana.title("Socktutopa1")

comboBox1 = ttk.Combobox(
    state="readonly",
    values=["COM1","COM2","COM3","COM4","COM5","COM6","COM7"])
comboBox1.set("COM1")
comboBox1.place(x = 160, y=40, width=140, height=22)

def click_pcplc():
    SerialPort1.write(b"Run pcplc")
    time.sleep(2)
    Recibir = SerialPort1.read_all()
    TextRecibidos.insert(1.0, Recibir)
def click_a():
    SerialPort1.write(b"a")
    time.sleep(2)
    Recibir = SerialPort1.read_all()
    TextRecibidos.insert(1.0, Recibir)
def click_ttsib():
    SerialPort1.write(b"Run ppnb")
    time.sleep(2)
    Recibir = SerialPort1.read_all()
    TextRecibidos.insert(1.0, Recibir)
def click_coff():
    SerialPort1.write(b"coff")
    time.sleep(2)
    Recibir = SerialPort1.read_all()
    TextRecibidos.insert(1.0, Recibir)
def click_move():
    SerialPort1.write(b"move 0")
    time.sleep(2)
    Recibir = SerialPort1.read_all()
    TextRecibidos.insert(1.0, Recibir)
def click_open():
    SerialPort1.write(b"open\n")
def click_close():
    SerialPort1.write(b"close"+b"\r")
    time.sleep(2)
    Recibir = SerialPort1.read_all()
    TextRecibidos.insert(1.0, Recibir)

def click_conectar():
    if SerialPort1.isOpen() == False:
        SerialPort1.baudrate = 9600
        SerialPort1.bytesize = 8
        SerialPort1.parity = "N"
        SerialPort1.stopbits = serial.STOPBITS_ONE
        SerialPort1.port = comboBox1.get()
        SerialPort1.open()
        TextoEstado["state"] = "normal"
        TextoEstado.delete(1.0, tk.END)
        TextoEstado.insert(1.0, "Conectado")
        TextoEstado.configure(background="LIME")
        messagebox.showinfo(message="Puerto Conectado")
        TextoEstado["state"]="disable"

def click_desconectar():
    if SerialPort1.isOpen() == True:
        SerialPort1.close()
        TextoEstado["state"] = "normal"
        TextoEstado.delete(1.0, tk.END)
        TextoEstado.insert(1.0, "Desconectado")
        TextoEstado.configure(background="red")
        messagebox.showinfo(message="Puerto Desconectado")
        TextoEstado["state"]="disable"

def click_enviar():
    SerialPort1.write(TextEnviar.get().encode()+b"\r")
    time.sleep(2)
    messagebox.showinfo(message="enviado Correctamente", title="Resultado")
    aux = SerialPort1.read_all()
    if b"Done" in aux:
        TextRecibidos.insert(1.0, b"Done. \n")

def click_guardar():
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files", "*.txt"), ("All Files","*.*")]
    )
    if not filepath:
        return
    with open(filepath, "w") as outpu_files:
        text = TextEnviar.get(1.0, tk.END)
        outpu_files.write(text)
        
#Label
LDatosEnviados = tk.Label(ventana, text="Datos Enviados")
LDatosEnviados.place(x= 180, y=100, width=80, height=15)
LDatosRecibidos = tk.Label(ventana, text="Datos Recibidos")
LDatosRecibidos.place(x= 345, y=100, width=85, height=16)
#Botones
BotonConectar = tk.Button(ventana, text="Conectar", command=click_conectar)
BotonDesconectar = tk.Button(ventana, text="Desconectar", command=click_desconectar)
BotonEnviar = tk.Button(ventana, text="Enviar", command=click_enviar)
BotonGuardar = tk.Button(ventana, text="Guardar", command=click_guardar)
BotonRunpclpc = tk.Button(ventana, text="Run pcplc", command=click_pcplc)
BotonAbortar = tk.Button(ventana, text="Abortar", command=click_a)
BotonRunttsib = tk.Button(ventana, text="Run ppnb",command=click_ttsib)
BotonCoff = tk.Button(ventana, text="Coff",command=click_coff)
BotonMove = tk.Button(ventana, text="Move 0", command=click_move)
BotonOpen = tk.Button(ventana, text="Open", command=click_open)
BotonClose = tk.Button(ventana, text="Close", command=click_close)
BotonConectar.place(x = 70, y=40, width=75, height=23)
BotonDesconectar.place(x = 310, y= 40, width=75, height=23)
BotonRunpclpc.place(x = 40, y= 100, width=75, height=23)
BotonAbortar.place(x = 40, y= 130, width=75, height=23)
BotonRunttsib.place(x = 40, y= 160, width=75, height=23)
BotonCoff.place(x = 40, y= 190, width=75, height=23)
BotonMove.place(x = 40, y= 220, width=75, height=23)
BotonOpen.place(x = 40, y= 250, width=75, height=23)
BotonClose.place(x = 40, y= 280, width=75, height=23)
BotonEnviar.place(x = 170, y= 190, width=75, height=23)
BotonGuardar.place(x = 340, y= 270, width=75, height=23)
#Combobox
comboBox1 = ttk.Combobox(
    state="readonly",
    values = ["COM1","COM2","COM3","COM4","COM5","COM6","COM7","COM8"],
    )
comboBox1.set("COM1")
comboBox1.place(x = 160, y=40, width=140, height=22)
#Cajas De texto
TextEnviar = tk.Entry(ventana)
TextEnviar.place(x = 140, y=120, width=160, height=60)
TextRecibidos = tk.Text(ventana)
TextRecibidos.place(x = 310, y=120, width=160, height=140)
TextoEstado = tk.Text(ventana)
TextoEstado.place(x= 170, y= 10, width=110, height=20)
TextoEstado.insert(1.0,"DESCONECTADO")
TextoEstado["state"] = "disabled"
#Serial
SerialPort1 = serial.Serial()




ventana.mainloop()