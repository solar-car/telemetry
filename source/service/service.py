from source.common.network import NetworkingHandler
from source.common.data import DataHandler
from source.common.file import Parser


class TelemetryService:
    def __init__(self):
        self.name = "Service"
        self.parser = Parser()

        self.module_data = self.parser.parse_xml("Modules")
        self.settings = self.parser.parse_xml("Settings")
        print(self.settings)

        self.data_handler = DataHandler(self.module_data, self.settings)
        self.networking_handler = NetworkingHandler(self.name, self.settings["Networking"])
        self.networking_handler.start()
        while True:
            i = input("Message: ")
            if i:
                self.networking_handler.send_buffer.append(i)


s = TelemetryService()