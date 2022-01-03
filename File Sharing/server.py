import socket
import threading
import time
import shutil
import os, sys


class Server:

    bufsize = 32768
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, bufsize)

    def __init__(self, host=None, port=5555):
        self.host = host
        self.port = port
        self.receiving = True
        if not self.host:
            self.host = socket.gethostbyname(socket.gethostname())
        self.server.bind((self.host, self.port))

    def start(self):
        self.recv_thread = threading.Thread(target=self.receive_file)
        self.recv_thread.start()

    def receive_file():
        while self.receiving:    
            msg, addr = server.recvfrom(bufsize)
            print(msg)

    def send_file(file, dstpath, addr):
        pass

if __name__ == "__main__":
    server = Server()
    server.start()