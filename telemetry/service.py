from common.thread_handler import ThreadHandler
from service.service_network import ServiceNetworkingHandler
from service.service_state import ServiceStateHandler


class TelemetryService:
    def __init__(self):
        self.state_handler = ServiceStateHandler()
        self.thread_handler = ThreadHandler()

        self.networking_handler = ServiceNetworkingHandler(self.state_handler)
        self.networking_handler.start()

        while True:
            i = input("Message: ")
            if i:
                self.networking_handler.send_buffer.append(i)


s = TelemetryService()