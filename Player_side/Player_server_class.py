import socket
import threading

class Server_isuue(object):
    def __init__(self):
        self.header = 2048
        self.port = 5050
        self.format = 'utf-8'
        self.R_we_listening = True
        self.server_msg = ''


        self.server_IP = '192.168.1.114'  # "178.79.150.181
        self.address = (self.server_IP, self.port)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.address)

        self.thread_server = threading.Thread(target=self.server_listener)
        self.thread_server.start()

    def server_comunication(self, commend):
        encoded_commend = commend.encode(self.format)
        server_msg_lenght = len(encoded_commend)
        send_lenght = str(server_msg_lenght).encode()
        send_lenght += b" " * (self.header - len(send_lenght))
        self.client.send(send_lenght)
        self.client.send(encoded_commend)
        self.server_msg = ''

    def server_listener(self):

        while self.R_we_listening :
            self.server_msg = self.client.recv(self.header).decode(self.format)


    def thread_killer(self):
        self.R_we_listening = False
