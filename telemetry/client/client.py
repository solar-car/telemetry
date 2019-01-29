from telemetry.client.client_network import ClientNetworkingHandler
from telemetry.client.client_state import ClientStateHandler
from telemetry.client.gui import UserInterface
from telemetry.auth import AuthenticationManager


class Client:
    def __init__(self):

        self.state_handler = ClientStateHandler()  # Should be initialized first
        self.auth_manager = AuthenticationManager(self.state_handler)

        self.networking_handler = ClientNetworkingHandler(self.state_handler)
        self.networking_handler.start()

        self.user_interface = UserInterface(self.state_handler)
        self.user_interface.start()


client = Client()
