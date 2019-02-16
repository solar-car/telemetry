import json

from threading import Thread

from twisted.internet.protocol import DatagramProtocol, Protocol
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from twisted.internet.error import ConnectionDone
from twisted.internet.endpoints import connectProtocol, TCP4ClientEndpoint

from telemetry.common.network import Packet, AuthenticationResult
from telemetry.common.state_handler import Subscriber
from telemetry.client.client_state import ClientStateHandler


class ClientNetworkingHandler(Thread, Subscriber):
    def __init__(self, event_handler, client_state_handler, settings):
        Thread.__init__(self)
        self.event_handler = event_handler
        self.client_state_handler = client_state_handler
        
        # General networking settings
        self.settings = settings["Networking"]
        self.client_host = self.settings["ClientDebugHost"]
        self.server_host = self.settings["ServerDebugHost"]
        self.connection_tcp_port = self.settings["ClientTCPPort"]
        self.auth_tcp_port = self.settings["ClientTCPAuthPort"]
        self.client_authentication_timeout = self.settings["ClientAuthenticationTimeout"]

        self.authentication_attempts = 0
        self.authentication_state = "not authenticated"

        # Authentication connection
        self.auth_endpoint = TCP4ClientEndpoint(reactor, self.server_host, self.auth_tcp_port)
        self.connection_endpoint = TCP4ClientEndpoint(reactor, self.server_host, self.connection_tcp_port)

    def run(self):
        connectProtocol(self.auth_endpoint, ServerAuth(self))
        connectProtocol(self.connection_endpoint, ServerConnect(self))

        reactor.run(installSignalHandlers=False)

    def external_update(self, updated_state):
        pass


class ServerAuth(Protocol):
    def __init__(self, handler):
        self.handler = handler
        self.authenticated = False

    def connectionMade(self):
        self.handler.event_handler.add_task(self.handler.client_state_handler.update_status, True, False)

    def connectionLost(self, reason=ConnectionDone):
        print("disconnect")
        self.handler.event_handler.add_task(self.handler.client_state_handler.update_status, False, False)

    def dataReceived(self, data):
        if self.authenticated:
            pass

        #  Attempt authentication
        else:
            try:
                authentication_result = Packet.construct_from_encoded_json(data).data
                if authentication_result == AuthenticationResult.AUTHENTICATED.value:
                    print(AuthenticationResult.AUTHENTICATED.value)
                elif authentication_result == AuthenticationResult.NOT_AUTHENTICATED.value:
                    print(AuthenticationResult.NOT_AUTHENTICATED.value)
            except json.JSONDecodeError:
                print("Authentication packet was corrupted or in incorrect format")


class ServerConnect(Protocol):
    def __init__(self, handler):
        self.handler = handler

    def connectionMade(self):
        pass

    def connectionLost(self, reason=ConnectionDone):
        pass

    def dataReceived(self, data):
        pass
