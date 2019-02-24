import copy

from client.client_network import ClientNetworkingHandler
from client.client_state import ClientStateHandler
from client.gui import UserInterface
from common.thread_handler import ThreadHandler


class Client:
    def __init__(self):

        self.state_handler = ClientStateHandler()  # Should be initialized first
        # All access to state_handler in non-main threads should happen through event_handler
        self.thread_handler = ThreadHandler(self.state_handler)

        self.user_interface = UserInterface(self, self.state_handler.modules)
        self.user_interface.start()
        self.thread_handler.subscriptions.append(self.user_interface)

    def initialize_networking(self):
        self.networking_handler = ClientNetworkingHandler(self)
        self.thread_handler.subscriptions.append(self.networking_handler)
        self.networking_handler.start()


client = Client()
