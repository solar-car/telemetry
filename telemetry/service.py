from telemetry.service import ServiceNetworkingHandler
from telemetry.service import ServiceStateHandler


class TelemetryService:
    def __init__(self):
        self.state_handler = ServiceStateHandler()

        self.networking_handler = ServiceNetworkingHandler(self.state_handler)
        self.networking_handler.start()

        while True:
            i = input("Message: ")
            if i:
                self.networking_handler.send_buffer.append(i)


s = TelemetryService()