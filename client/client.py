import sys

from common.networking.networking_handler import NetworkingHandler
from gui.user_interface import UserInterface


class Client:
    def __init__(self):
        self.name_key = "client"
        self.user_interface = UserInterface()
        self.networking_handler = NetworkingHandler("client")

client = Client()
