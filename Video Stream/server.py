import cv2
import socket
import numpy as np
import base64
import time
from PIL import ImageGrab

res = (1280, 720)
bufsize = (res[0] * res[1]) // 4
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, bufsize)
host = socket.gethostbyname(socket.gethostname())
port = 5555
server.bind((host, port))

msg, addr = server.recvfrom(bufsize)
print(f"Connected to client at '{addr}'")

while True:
    sc = ImageGrab.grab(bbox=(0, 0, 1366, 768))

    sc = np.array(sc.resize(res))
    chunk_size = res[1] // 4
    for i in range(0, 4):
        chunk = sc[i*chunk_size:(i+1)*chunk_size]
        _, chunk = cv2.imencode(".jpg", chunk, [cv2.IMWRITE_JPEG_QUALITY, 80])
        encoded = base64.b64encode(chunk)
        server.sendto(encoded, addr)
    if (cv2.waitKey(1) & 0xFF) == ord("q"):
        client.close()
        break