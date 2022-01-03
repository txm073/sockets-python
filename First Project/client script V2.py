import socket
import sys
import threading
import time
import tkinter as tk
import re

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.0.93"
ADDR = (SERVER, PORT)
CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
    try:
        CLIENT.connect(ADDR)
    except ConnectionRefusedError:
        print("The server is not currently online.")
        sys.exit()

print(" ")
USERNAME = input("Enter a username: ")

def donothing():
    pass

def pick_up():
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
            break

def send(msg):
    enc_msg = msg.encode(FORMAT)
    enc_msg_len = str(len(enc_msg)).encode(FORMAT)
    enc_msg_len += b" " * (HEADER - len(enc_msg_len))
    CLIENT.send(enc_msg_len)
    CLIENT.send(enc_msg)       

def send_msg():
    send(USERNAME)
    time.sleep(2)
    connected = True
    while connected == True:
        time.sleep(2)
        user_msg = input("Enter a message: ")
        send(user_msg)

def main():
    pass

main_thread = threading.Thread(target=main)
check_thread = threading.Thread(target=pick_up)
#gui_thread = threading.thread(target=GUI)
main_thread.start()
#gui_thread.start()
if USERNAME:
    check_thread.start()

