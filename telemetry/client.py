import copy
import time

from client.client_network import ClientNetworkingHandler
from client.client_state import ClientStateHandler
from client.gui import UserInterface
from common.state_handler import EventHandler


class Client:
    def __init__(self):

        self.state_handler = ClientStateHandler()  # Should be initialized first
        # All access to state_handler in non-main threads should happen through event_handler
        self.event_handler = EventHandler(self.state_handler)

        self.user_interface = UserInterface(self.event_handler, self.state_handler, self.state_handler.modules,
                                            self.state_handler.settings)
        self.user_interface.start()
        self.event_handler.subscriptions.append(self.user_interface)

        time.sleep(3)

        self.networking_handler = ClientNetworkingHandler(self.event_handler, self.state_handler,
                                                          copy.deepcopy(self.state_handler.settings))
        self.event_handler.subscriptions.append(self.networking_handler)
        self.networking_handler.start()


client = Client()
