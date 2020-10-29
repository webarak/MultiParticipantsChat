import socket
import threading
import time

IP = '0.0.0.0'
PORT = 5000
clients_and_threads = []
condition = threading.Condition()


class Chat(threading.Thread):
    def __init__(self, client_socket, name):
        threading.Thread.__init__(self, name = name)
        self.client = client_socket

    def run(self):
        global clients_and_threads
        print(self.name)
        while True:
            try:
                data = self.client.recv(1024).decode()

            except:
                print("the client disconnected")
                for c in clients_and_threads:
                    if c[0] == self.client:
                        clients_and_threads.remove(c)
                break

            if data == 'quit':
                self.client.send("close socket".encode())
                for c in clients_and_threads:
                    if c[0] == self.client:
                        clients_and_threads.remove(c)
                self.client.close()
                break

            condition.acquire()
            lst_of_data = data.split("⛔")
            print(data)
            if lst_of_data[-1] == '1':
                data = self.name + ": " + lst_of_data[0]
                for c in clients_and_threads:
                    if c[0] != self.client:
                        c[0].send(data.encode())
            elif lst_of_data[-1] == '2':
                data = "private massage from "+ self.name + ": " + lst_of_data[1]
                for c in clients_and_threads:
                    if c[1].name == lst_of_data[0]:
                        c[0].send(data.encode())
            elif lst_of_data[-1] == '3':
                self.name = lst_of_data[0]
            condition.release()


class Server(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((IP, PORT))
        self.server_socket.listen(5)

    def run(self):
        global clients_and_threads
        while True:
            client_socket, client_adress = self.server_socket.accept()
            name = client_socket.recv(1024).decode()
            print(client_adress)
            t = Chat(client_socket, name)
            clients_and_threads.append((client_socket, t))
            t.start()





c = Server()
c.start()
