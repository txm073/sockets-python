import socket
import threading
import re
import os

HEADER = 64
IP = socket.gethostbyname(socket.gethostname())
FORMAT = "utf-8"
SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
PATH = os.path.join(os.path.abspath(__file__)[:-10],"Assets")

class Server:
    
    def __init__(self,username,conn,address):
        PORT = 5050
        ADDR = (SERVER,PORT)
 
    def connect(self):
        pass

    def send_to(self):
        pass

    def broadcast(self):
        pass

    def receive(self):
        pass

    

class LoginServer(Server):
    
    def __init__(self,port):
        Server.__init__(self)
        ADDR = (SERVER,port)

  
        while True:
            self.conn, self.address = self.server.accept()
            self.main = threading.Thread(
                target=self.new_login,
                args=(self.conn,self.address)).start()
    
    def new_login(self,conn):
        try:
            self.credentials = self.receive(conn)
            self.credentials = re.split("   ",self.credentials)
            self.user = self.credentials[0]
            self.password = self.credentials[1]
            if self.check_login(self.user,self.password) == True:
                self.send("Log In Accepted")
        except ConnectionResetError:
            conn.close()
        
    def check_login(self,user,password):
        with open(os.path.join(PATH,"users.txt"),"r") as file:
            self.users = re.split(", ",str(file.read()))
        with open(os.path.join(PATH,"passwords.txt"),"r") as file:
            self.passwords = re.split(", ",str(file.read()))
        for user in range(len(self.users)):
            if self.users[user] == user:
                break
        if self.passwords[user] == password:
            return True
        return False
