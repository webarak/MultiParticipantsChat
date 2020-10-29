import socket
import threading

IP = '127.0.0.1'
PORT = 5000


class Client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((IP, PORT))
        self.client.send((input("enter your user name")).encode())

    def run(self):
        while True:
            data = self.client.recv(1024).decode()
            print(data)
            if (data == 'close socket'):
                self.client.close()
                break

    def send_maasage(self):
        while True:
            data = ""
            command = input("please enter your desire command:\n1 - general massage\n2 - private massage\n3 - change username\n4 - quit\n")
            if command == '1':
                data = input()
                data = data + "⛔" + command
            if command == '2':
                data = input()
                another_name = input("enter the name of the client that you want to send it to")
                data = another_name + "⛔" + data + "⛔" + command
            if command == '3':
                new_username = input("enter your new desire username")
                data = new_username + "⛔" + command
            if command == '4':
                data = "quit"

            self.client.send(data.encode())
            if data == 'quit':
                break



C = Client()
C.start()
C.send_maasage()
input()