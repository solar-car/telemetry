import copy

from common.state_handler import ThreadHandler
from service.service_network import ServiceNetworkingHandler
from service.service_state import ServiceStateHandler


class Service:
    def __init__(self):
        self.state_handler = ServiceStateHandler()
        self.event_handler = ThreadHandler(self.state_handler)

        self.networking_handler = ServiceNetworkingHandler(self)
        self.networking_handler.start()


Service = Service()
