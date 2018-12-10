import sys

from common.networking.networking_handler import NetworkingHandler
from gui.user_interface import UserInterface

class Client:
    def __init__(self):
        self.name = "client"

        self.user_interface = UserInterface()
        self.user_interface.start()

        self.networking_handler = NetworkingHandler(self)
        self.networking_handler.start()


client = Client()
