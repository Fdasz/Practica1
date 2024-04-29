import socket
import tkinter as tk 
from threading import Thread
import tkinter.messagebox as messagebox
import time

HOST = '192.168.50.128'
PORT = 8888

class CLientGUI:
    def __init__(self, master):
        self.master = master
        master.title('Cliente')

        self.name = tk.StringVar()
        self.name.set("USUARIO2")

        self.received_messages_text = tk.Text(master, height=10, width=50)
        self.received_messages_text.pack()

        self.message_entry = tk.Entry(master, width=50)
        self.message_entry.pack()

        self.name_entry = tk.Entry(master, width=50, textvariable=self.name)
        self.name_entry.pack()

        self.send_button = tk.Button(master, text='Enviar', command=self.send_message)
        self.send_button.pack()

        self.connected = False
        self.connect_to_server()

    def connect_to_server(self):
        while True:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                self.socket.connect((HOST, PORT))

                self.connected = True

                self.socket.sendall(self.name.get().encode())

                self.recived_thread = Thread(target=self.received_messages)
                self.recived_thread.start()
                
                break

            except Exception as e:
                print(e)

                self.connected = False

                time.sleep(5)

    def received_messages(self):
        while self.connected:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break

                self.received_messages_text.insert(tk.END, data.decode() + '\n')
                self.received_messages_text.see(tk.END)

            except Exception as e:
                print(e)
                self.connected = False
                self.socket.close()
                break
            
    def send_message(self):
        message = self.message_entry.get()

        if not self.connected:
            messagebox.showerror('Error', 'No se pudo enviar el mensaje: no hay conexcion con el servidor.')
            return
        
        if not self.socket._closed:
            self.socket.sendall(message.encode())

            self.message_entry.delete(0, tk.END)
        else:
            messagebox.showerror('Error', 'No se pudo enviar el mensaje: la conexion con el servidor se ha perdido.')

        
if __name__ == "__main__":
    root = tk.Tk()
    client_gui = CLientGUI(root)
    root.mainloop()