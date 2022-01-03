import socket
import threading
import os
import time

host = "169.254.112.201"
port = 5055
buffer = 1024
codec = "ascii"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def send_file(file):
    with open(file, "rb") as f:
        contents = f.read()
    
    global file_name
    file_name = os.path.basename(file)

    chunk_size = 512
    n_chunks = len(contents) // chunk_size + 1 
    client.send("***transfer***".encode(codec))
    client.send(os.path.basename(file).encode(codec))
    time.sleep(0.5)
    client.send(str(n_chunks).encode(codec))
    time.sleep(0.5)

    for i in range(n_chunks):
        if i == 0:
            chunk = contents[:chunk_size]
        elif i == n_chunks - 1:
            chunk = contents[-len(contents) % chunk_size:]
        else:
            chunk = contents[i * chunk_size: (i + 1) * chunk_size]

        client.send(chunk)

    client.send("***finished***".encode(codec))

try:
    os.chdir(os.path.dirname(__file__))
except OSError:
    pass

def send_file(file):
    with open(file, "rb") as f:
        contents = f.read()
    
    global file_name
    file_name = os.path.basename(file)

    chunk_size = 512
    n_chunks = len(contents) // chunk_size + 1 
    client.send("***transfer***".encode(codec))
    client.send(os.path.basename(file).encode(codec))
    #time.sleep(0.5)
    client.send(str(n_chunks).encode(codec))
    #time.sleep(0.5)

    for i in range(n_chunks):
        if i == 0:
            chunk = contents[:chunk_size]
        elif i == n_chunks - 1:
            chunk = contents[-len(contents) % chunk_size:]
        else:
            chunk = contents[i * chunk_size: (i + 1) * chunk_size]

        client.send(chunk)

    client.send("***finished***".encode(codec))

try:
    os.chdir(os.path.dirname(__file__))
except OSError:
    pass

def receive():
    while True:
        try:
            msg = client.recv(buffer).decode(codec)
            print(f"<Server> {msg}")

        except ConnectionResetError:
            print("The server has closed")
            os._exit(0)

def send():
    while True:
        msg = input("Enter a message: ")
        if msg.startswith("/sendfile"):
            send_file(msg[len("/sendfile"):].strip())
        else:
            client.send(msg.encode(codec))

if __name__ == "__main__":
    t1 = threading.Thread(target=send).start()
    t2 = threading.Thread(target=receive).start()
