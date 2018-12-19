from source.common.networking.networking_handler import NetworkingHandler
from user_interface import UserInterfaceHandler


class Client:
    def __init__(self):
        self.name = "client"

        self.user_interface_handler = UserInterfaceHandler()
        self.user_interface_handler.start()

        self.networking_handler = NetworkingHandler(self)
        self.networking_handler.start()


client = Client()
