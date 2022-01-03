import socket
import threading
from datetime import datetime

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
SERVER = "192.168.0.93"
ADDR = (SERVER, PORT)
now = datetime.now()
date = now.strftime("%d/%m/%Y"+":")
time = now.strftime("%H:%M:%S"+":")

def donothing():
    pass

username = input("Enter username: ")

connected = False
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    connected = True
except ConnectionRefusedError:
    print("The server is currently offline. Please try again later.")
except TimeoutError:
    print("Connection to the server timed out.")



def send(msg):
    message = msg.encode(FORMAT)
    header = str(len(message)).encode(FORMAT)
    header += b" "* (HEADER-len(header))
    client.send(header)
    client.send(message)

try:
    send(username)
    if username == "ADMIN":
        correct_password = False
        while correct_password == False:
            user_password = input("Enter ADMIN password: ")
            send(user_password)
            answer = client.recv(HEADER).decode(FORMAT)
            if answer == "[SERVER] Password accepted.":
                correct_password = True
            else:
                retry = input(answer.rstrip()+" ")
                send(retry)

    welcome_msg_length = len(client.recv(HEADER).decode(FORMAT))
    welcome_msg = client.recv(welcome_msg_length).decode(FORMAT)
    print("\033[F"+welcome_msg)

    connected = False
    while connected == True:
        #client.recv(HEADER).decode(FORMAT)
        msg = input("Enter a message: ")
        send(msg)
        reply = client.recv(HEADER).decode(FORMAT)
        print("\033[F"+reply)
        if msg == DISCONNECT_MESSAGE:
            print("[SERVER] Bye!")
            connected = False

except ConnectionResetError:
    print("You were kicked from the server!")
except TimeoutError:
    print("Connection to the server timed out.")
except OSError:
    donothing()

