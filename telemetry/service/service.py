from telemetry.network import NetworkingHandler
from telemetry.data import DataHandler
from telemetry.file import Parser


class TelemetryService:
    def __init__(self):
        self.name = "Service"
        self.parser = Parser()

        self.data = self.parser.parse_xml_as_dictionary(self.name)
        self.settings = self.parser.parse_xml_as_dictionary("Settings")
        print(self.settings)

        self.data_handler = DataHandler(self.data, self.settings)
        self.networking_handler = NetworkingHandler(self.name, self.settings["Networking"])
        self.networking_handler.start()
        while True:
            i = input("Message: ")
            if i:
                self.networking_handler.send_buffer.append(i)


s = TelemetryService()