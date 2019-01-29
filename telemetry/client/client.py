from threading import Lock

from telemetry.network import NetworkingHandler
from telemetry.client.gui import UserInterface
from telemetry.data import DataHandler
from telemetry.file import Parser

from telemetry.auth import AuthenticationManager


class Client:
    def __init__(self):
        self.name = "Client"
        self.thread_lock = Lock()

        self.auth_manager = AuthenticationManager()

        self.parser = Parser()
        module_data = self.parser.parse_xml("Modules")
        settings_data = self.parser.parse_xml("Settings")

        self.data_handler = DataHandler(module_data, settings_data)
        self.networking_handler = NetworkingHandler(self.name, self.data_handler.settings["Networking"])
        self.networking_handler.start()

        self.user_interface = UserInterface(self.data_handler.modules)
        self.user_interface.start()

client = Client()
