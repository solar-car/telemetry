from threading import Lock

from source.common.network import NetworkingHandler
from source.client.gui import UserInterfaceHandler
from source.common.data import DataHandler
from source.common.file import Parser, ParserReturnType


class Client:
    def __init__(self):
        self.name = "Client"
        self.thread_lock = Lock()

        self.parser = Parser()
        module_data = self.parser.parse_xml_as_dictionary("Modules")
        settings_data = self.parser.parse_xml_as_dictionary("Settings", ParserReturnType.CONVERTED_STRING)

        self.data_handler = DataHandler(module_data, settings_data)
        self.networking_handler = NetworkingHandler(self.name, self.data_handler.settings["Networking"])
        self.networking_handler.start()

        self.user_interface_handler = UserInterfaceHandler(self.data_handler.modules)
        print(self.user_interface_handler)


client = Client()
