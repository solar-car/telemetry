import copy

from telemetry.common.state_handler import EventHandler
from telemetry.server.server_network import ServerNetworkingHandler
from telemetry.server.server_state import ServerStateHandler


class Server:
    def __init__(self):
        self.state_handler = ServerStateHandler()
        self.event_handler = EventHandler(self.state_handler)

        self.networking_handler = ServerNetworkingHandler(self.event_handler, copy.deepcopy(self.state_handler.settings))
        self.networking_handler.start()


server = Server()
