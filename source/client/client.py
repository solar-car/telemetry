from source.common.networking_handler import NetworkingHandler
from user_interface import UserInterfaceHandler
from data_handler import DataHandler


class Client:
    def __init__(self):
        self.name = "client"

        self.data_handler = DataHandler(self)

        self.user_interface_handler = UserInterfaceHandler(self)
        self.user_interface_handler.start()

        self.networking_handler = NetworkingHandler(self)
        self.networking_handler.start()


client = Client()
