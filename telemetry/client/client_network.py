import json

from threading import Thread

from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.error import ConnectionDone
from twisted.internet.endpoints import connectProtocol, TCP4ClientEndpoint

from common.network import Packet, AuthenticationResult
from common.thread_handler import Subscriber


class ClientNetworkingHandler(Thread, Subscriber):
    def __init__(self, context):
        Thread.__init__(self)
        self.context = context
        self.thread_handler = context.thread_handler
        self.state_handler = context.state_handler
        
        # General networking settings
        self.settings = self.state_handler.settings["Networking"]
        self.client_host = self.settings["ClientDebugHost"]
        self.service_host = self.settings["ServiceDebugHost"]
        self.connection_tcp_port = self.settings["ConnectionPort"]
        self.auth_tcp_port = self.settings["AuthenticationPort"]

        # Authentication connection
        self.auth_endpoint = TCP4ClientEndpoint(reactor, self.service_host, self.auth_tcp_port)
        self.connection_endpoint = TCP4ClientEndpoint(reactor, self.service_host, self.connection_tcp_port)

    def run(self):
        connectProtocol(self.auth_endpoint, Authentication(self))
        connectProtocol(self.connection_endpoint, Connection(self))

        reactor.run(installSignalHandlers=False)

    def external_update(self, updated_state):
        pass


class Authentication(Protocol):
    def __init__(self, handler):
        self.handler = handler
        self.authenticated = False

    def connectionMade(self):
        self.handler.thread_handler.add_task(self.handler.state_handler.update_status, True, False)

    def connectionLost(self, reason=ConnectionDone):
        print("disconnect")
        self.handler.thread_handler.add_task(self.handler.state_handler.update_status, False, False)

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


class Connection(Protocol):
    def __init__(self, handler):
        self.handler = handler

    def connectionMade(self):
        pass

    def connectionLost(self, reason=ConnectionDone):
        pass

    def dataReceived(self, data):
        pass
