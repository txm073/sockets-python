import cv2
import socket
import numpy as np
import base64
from PIL import Image
import threading
import pygame
import time
import os


class Client:

    def __init__(self, host, port, res):
        self.host = host
        self.port = port
        self.res = res
        self.bufsize = (self.res[0] * self.res[1]) // 4
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.bufsize)

        pygame.display.init()
        self.win = pygame.display.set_mode(self.res)
        pygame.display.set_caption(f"Input Broadcast From '{self.host}'")
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.image = np.concatenate([np.zeros([*self.res, 2]), np.array([255] * np.prod(self.res)).reshape(*self.res, 1)], axis=2)

    def receive(self):
        while True:
            chunks = []
            for i in range(4):
                packet, _ = self.client.recvfrom(self.bufsize)
                data = base64.b64decode(packet, " /")
                imgdata = np.frombuffer(data, dtype=np.uint8)
                chunk = cv2.imdecode(imgdata, flags=1)
                chunks.append(chunk)

            self.image = np.vstack(chunks)

    def start(self):
        self.client.sendto("Connected".encode(), (self.host, self.port)) 
        print(f"Connected to server at '{self.host}'")
        self.recv_thread = threading.Thread(target=self.receive)
        self.recv_thread.start()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    os._exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    button_types = ["LEFT", "MIDDLE", "RIGHT", "UP", "DOWN"]
                    pos = pygame.mouse.get_pos()
                    msg = button_types[event.button - 1] + ":" + str(pos[0]) + "," + str(pos[1])
                    self.client.sendto(msg.encode(), (self.host, self.port))
                elif event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    msg = "MOVE:" + str(pos[0]) + "," + str(pos[1])
                    self.client.sendto(msg.encode(), (self.host, self.port))                   

            surface = pygame.transform.flip(pygame.transform.rotate(pygame.surfarray.make_surface(self.image), 270), True, False)
            self.win.blit(surface, (0, 0))

            self.clock.tick(self.fps)
            pygame.display.update()


if __name__ == "__main__":
    client = Client("192.168.0.70", 5555, (1280, 720))
    client.start()
