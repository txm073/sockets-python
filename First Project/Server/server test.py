import socket 
import threading
from datetime import datetime

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
clients_online = []
addresses = []
clients_lock = threading.Lock()
now = datetime.now()
date = now.strftime("%d/%m/%Y"+":")
time = now.strftime("%H:%M:%S"+":")

def sendtoall(client, msg, addr):
    print(msg)
    encoded_message = msg.encode(FORMAT)
    encoded_message_length = encoded_message + b' ' * (HEADER - len(encoded_message))
    client.sendto(encoded_message_length,addr)

def send_header(client, msg, addr):
    encoded_message = msg.encode(FORMAT)
    encoded_message = encoded_message + b' ' * (HEADER - len(encoded_message))
    client.sendto(encoded_message,addr)

def security(username, clients_online):
    #if username == "ADMIN":
        
    
    for client in clients_online:
        if username == client:
            return False
    with open("server whitelist.txt","r") as perms:
        whitelist = perms.read()
        members = whitelist.split() 
        if not username in members:
            return False
        
def handle_client(client, addr):
    try:
        username_length = int(client.recv(HEADER).decode(FORMAT))
        username = client.recv(username_length).decode(FORMAT)
        #security(username, clients_online)      
        with clients_lock:
            clients_online.append(username)
            addresses.append(addr)
        print(f"[NEW CONNECTION] {username} connected.")
        connected = True
        while connected:
            msg_length = int(client.recv(HEADER).decode(FORMAT))
            msg = client.recv(msg_length).decode(FORMAT)
            if msg != username:
                if msg == DISCONNECT_MESSAGE:
                    print(f"[DISCONNECTION] {username} disconnected.")
                    del(addresses[clients_online.index(username)]) 
                    break
                elif msg == "CURRENTLY ONLINE?":
                    str(clients_online).replace("'","")
                    print(f"[CURRENTLY ONLINE] {str(clients_online)[1:-1]}")
                    online_info = f"[CURRENTLY ONLINE] {str(clients_online)}".encode(FORMAT)
                    online_info_length = online_info + b" " * (HEADER - len(online_info))
                    client.send(online_info_length)
                message = f"<{username}> {msg}"
                for addr in addresses:
                    send_header(client, message, addr)
                    sendtoall(client, message, addr)
            else:
                welcome = f"[NEW CONNECTION] {username} connected.".encode(FORMAT)
                for addr in addresses:
                    sendtoall(client, welcome, addr)    
            #if len(clients_online) == 0:
            
    except ConnectionResetError:
        user_left = clients_online.index(username)
        print(f"[DISCONNECTION] {clients_online[user_left]} disconnected.")
        del(addresses[clients_online.index(username)]) 
        del(clients_online[user_left])

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()

print("[STARTING] server is starting...")
start()
