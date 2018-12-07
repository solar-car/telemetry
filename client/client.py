import sys

from common.networking.networking_handler import NetworkingHandler


class Client:
    def __init__(self):
        self.key = "client"
        self.networking_handler = NetworkingHandler(self.key)

client = Client()
