import socket
import threading
import tkinter as tk

HOST = '192.168.50.128'
PORT = 8888
MAX_CONNECTIONS = 2 
global Server_Socket, connections


def iniciar_Servidor():
    Servidor_Thread = threading.Thread(target=correr_Servidor)
    Servidor_Thread.start()

    Start_button.config(state=tk.DISABLED)
    Stop_Button.config(state=tk.NORMAL)
    mensaje_Text.config(state=tk.NORMAL)
    Enviar_Button.config(state=tk.NORMAL)

    EstadoLabel.config(text='Servidor corriendo')

def correr_Servidor():
    global Server_Socket
    Server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    Server_Socket.bind((HOST, PORT))
    log(f'Servidor corriendo en el puerto {PORT}')

    Server_Socket.listen(MAX_CONNECTIONS)

    global connections
    connections = []
    names = []

    while True:
        conn , addr = Server_Socket.accept()
        connections.append(conn)

        data = conn.recv(1024)
        name = data.decode().strip()
        names.append(name)

        t = threading.Thread(target=Manejar_Conexion, args=(conn, addr, name))
        t.start()

def detener_Servidor():
    Server_Socket.close()

    Start_button.config(state=tk.NORMAL)
    Stop_Button.config(state=tk.DISABLED)
    mensaje_Text.config(state=tk.DISABLED)
    Enviar_Button.config(state=tk.DISABLED)

    EstadoLabel.config(text='Servidor Detenido')

def log(mensaje):
    Log_Text.insert(tk.END, mensaje + '\n')
    Log_Text.see(tk.END)


def Manejar_Conexion(conn, addr, name):
    log(f'{name} conectado por {addr}')

    while True:
        data = conn.recv(1024)
        mensaje = data.decode().strip()

        if not mensaje:
            break
        
        log(f'Datos recibidos de {name}: {mensaje}')

        respuesta = f'Recibido: {mensaje}'.encode()
        enviar_Mensaje(f'Enviado Por{name} : {mensaje}')
        #conn.sendall(respuesta)
    
    conn.close()
    log(f'Conexion cerrada con {name}')


def enviar_Mensaje(mensage):
    #mensaje = mensaje_Text.get(1.0, tk.END).strip()
    #mensaje_Text.delete(1.0, tk.END)
    log(f'Mensaje enviado a los clientes: {mensage}')
    for conn in connections:
        conn.sendall(mensage.encode())
    pass#y esto pa que??


ventana = tk.Tk()
ventana.title("Servidor")

EstadoLabel = tk.Label(ventana, text='Servidor detenido')
EstadoLabel.pack()

Log_Text = tk.Text(ventana, height=10,width=50)
Log_Text.pack()

Start_button = tk.Button(ventana, text='Iniciar' , command=iniciar_Servidor)
Start_button.pack()

Stop_Button = tk.Button(ventana, text='Detener', command=detener_Servidor, state=tk.DISABLED)
Stop_Button.pack()

mensaje_Text = tk.Text(ventana, height=3, width=50)
mensaje_Text.pack()

Enviar_Button = tk.Button(ventana, text='enviar' , command=enviar_Mensaje)
Enviar_Button.pack()

ventana.mainloop()