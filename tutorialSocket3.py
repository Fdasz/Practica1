import tkinter as tkk
from tkinter import ttk, messagebox
import serial
import time

comboBoxx1 = ttk.Combobox(state="readonly", values= ["COM1"])
comboBoxx1.set("COM1")
comboBoxx1.place(x=160,y=40,width=140, height=22)

def click_rojo():
    SerialPort1.write(b"rojo")
    time.sleep(2)
    Recibir = SerialPort1.read_all()
    TextRecibidos

#Serial
SerialPort1 = serial.Serial()