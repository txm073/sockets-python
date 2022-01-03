import socket
import threading
import sys
import time
import re

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
    try:
        CLIENT.connect(ADDR)
        print("connected")
    except ConnectionRefusedError:
        print("The server is not currently online.")
        sys.exit()
    except TimeoutError:
        print("Connection to the server timed out.")
        sys.exit()

def send(msg):
    enc_msg = msg.encode(FORMAT)
    enc_msg_len = str(len(enc_msg)).encode(FORMAT)
    enc_msg_len += b" " * (HEADER - len(enc_msg_len))
    try:
        CLIENT.send(enc_msg_len)
        CLIENT.send(enc_msg)     
    except ConnectionAbortedError:
        pass

def pick_up():
    time.sleep(1)
    while True:
        try:
            time.sleep(1)
            msg_len = len(CLIENT.recv(HEADER).decode(FORMAT))
            msg = CLIENT.recv(msg_len).decode(FORMAT)
            priv_msg = re.search("\+from:.*",msg)
            if priv_msg:
                message = msg[:priv_msg.span()[0]]
                sender = msg[priv_msg.span()[0]+6:]
                print(f"Message from {sender}: {message}")
            if msg:
                if not priv_msg:
                    print(msg)
        except ConnectionResetError:
            print("[SERVER] The server has closed.")
            time.sleep(1)
            break

