from threading import Lock

from source.common.network import NetworkingHandler
from source.client.gui import UserInterfaceHandler
from source.common.data import DataHandler
from source.common.file import Parser


class Client:
    def __init__(self):
        self.name = "Client"
        self.thread_lock = Lock()

        self.parser = Parser()

        self.data_handler = DataHandler(self.parser.load_as_dictionary("Modules"))

        self.user_interface_handler = UserInterfaceHandler(self.data_handler.modules)

        self.networking_handler = NetworkingHandler(self.name, self.parser.load_as_dictionary("Networking"))

        # Start threads
        self.user_interface_handler.start()
        self.networking_handler.start()


client = Client()
