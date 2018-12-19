from module_handler import ModuleHandler
from source.common.networking.networking_handler import NetworkingHandler


class TelemetryService:
    def __init__(self):
        self.name = "service"
        self.module_handler = ModuleHandler()
        self.networking_handler = NetworkingHandler(self)
        self.networking_handler.start()
        while True:
            i = input("Message: ")
            if i:
                self.networking_handler.buffer.append(i)


s = TelemetryService()