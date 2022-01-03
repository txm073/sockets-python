import re
import socket
import threading 
import os

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
USERS = {}
PATH = os.path.join("E:\\","Python","Socket Server","Assets")

main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_server.bind(ADDR)

def check_login(user,password):
    with open(os.path.join(PATH,"users.txt"),"r") as file:
        users = re.split(", ",str(file.read()))
    with open(os.path.join(PATH,"passwords.txt"),"r") as file:
        passwords = re.split(", ",str(file.read()))
    for x in range(len(users)):
        if users[x] == user:
            break
    if passwords[x] == password:
        return True
    return False

def send_to(user, msg):
    conn = USERS.get(user)
    enc_msg = (msg+"+from:"+user).encode(FORMAT)
    enc_msg_len = str(len(enc_msg)).encode(FORMAT)
    enc_msg_len += b" " * (HEADER - len(enc_msg_len))
    conn.send(enc_msg_len)
    conn.send(enc_msg)

def receive(conn):    
    msg_len = len(conn.recv(HEADER).decode(FORMAT))
    msg = conn.recv(msg_len).decode(FORMAT)
    return msg

def broadcast(clients, msg):
    enc_msg = msg.encode(FORMAT)
    enc_msg_len = str(len(enc_msg)).encode(FORMAT)
    enc_msg_len += b" " * (HEADER - len(enc_msg_len))
    for index, client in enumerate(clients): 
        print("Sending to:",list(clients.keys())[index])
        conn = clients.get(client)
        print("Sending to connection:",conn)
        conn.send(enc_msg_len)
        conn.send(enc_msg)
    
def handle_client(conn, addr):
    try:
        credentials = receive(conn)
        print(credentials)
        credentials = re.split("   ",credentials)
        user = credentials[0]
        password = credentials[1]
        USERS[user] = conn
        valid = check_login(user,password)
        if valid == False:
            send_to(user, "NO")
        else:
            send_to(user, "YES")
            new_user_msg = f"[NEW CONNECTION] {user} is online."
            broadcast(USERS, new_user_msg)
            print(new_user_msg)
            connected = True
            while connected:
                msg = receive(conn)
                print(msg)
                if msg == "DISCONNECT":
                    print(f"[DISCONNECTION] {user} disconnected")
                    del USERS[user]
                    break
                client_msg = f"<{user}> {msg}"
                print(client_msg)
                broadcast(USERS, client_msg)           
    except ConnectionResetError:
        print(f"[DISCONNECTION] {user} disconnected")
        del(USERS[user])
    conn.close()

print("[STARTING] server is starting...")
main_server.listen()
print(f"[LISTENING] Server is listening on {SERVER}")
while True:
    conn, addr = main_server.accept()
    main = threading.Thread(target=handle_client, args=(conn, addr)).start()




