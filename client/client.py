import sys

from common.networking.networking_handler import NetworkingHandler


class Client:
    def __init__(self):
        self.name = "client"
        self.networking_handler = NetworkingHandler(self)
        self.networking_handler.start()

client = Client()
