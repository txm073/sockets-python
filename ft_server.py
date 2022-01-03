import socket
import threading
import os
from tqdm import tqdm

try:
    os.chdir(os.path.dirname(__file__))
except OSError:
    pass

host = socket.gethostbyname(socket.gethostname())
port = 5055
buffer = 1024
codec = "ascii"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

def handle_client(conn, addr):
    while True:
        try:
            try:
                msg = conn.recv(buffer).decode(codec)
                print(f"{addr}: {msg}")
            except UnicodeError:
                msg = None

            if msg == "***transfer***":
                filename = conn.recv(buffer).decode(codec)
                n_chunks = int(conn.recv(buffer).decode(codec))
                byte_string = b""
                for i in tqdm(range(n_chunks)):
                    chunk = conn.recv(buffer)
                    if i == n_chunks - 1:
                        try:
                            if chunk.decode(codec) == "***finished***":
                                break
                        except UnicodeError:
                            pass
                    byte_string += chunk

                with open(filename, "wb") as f:
                    f.write(byte_string)

                conn.send("***transfer-finished***".encode(codec))

        except ConnectionResetError:
            print(f"{addr} disconnected")
            break

print(f"Server listening on {host}")
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
