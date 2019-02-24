import json

from threading import Thread

from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.error import ConnectionDone
from twisted.internet.endpoints import TCP4ServerEndpoint, connectProtocol

from telemetry.common.network import Packet
from telemetry.common.state_handler import Subscriber


class ServiceNetworkingHandler(Thread, Subscriber):
    def __init__(self, context):
        Thread.__init__(self)
        self.context = context

        # General networking settings
        self.settings = context.state_handler.settings["Networking"]
        self.client_host = self.settings["ClientDebugHost"]
        self.service_host = self.settings["ServiceDebugHost"]
        self.authentication_port = self.settings["AuthenticationPort"]
        self.connection_port = self.settings["ConnectionPort"]

        # References
        self.event_handler = context.event_handler

        # Data
        self.authentication_endpoint = TCP4ServerEndpoint(reactor, self.authentication_port)
        self.connection_endpoint = TCP4ServerEndpoint(reactor, self.connection_port)
        self.active_connections = []  # Connections spawned through connection_endpoint

    def run(self):
        connectProtocol(self.connection_endpoint, Connection)
        connectProtocol(self.authentication_endpoint, Authentication(self))
        reactor.run(installSignalHandlers=False)


class Authentication(Protocol):
    def __init__(self, handler):
        self.handler = handler

    def connectionMade(self):
        pass

    def connectionLost(self, reason=ConnectionDone):
        pass

    def dataReceived(self, data):
        pass


class Connection(Protocol):
    def __init__(self, handler):
        self.handler = handler
        self.authenticated = False

    def connectionMade(self):
        print("connection")

    def connectionLost(self, reason=ConnectionDone):
        print("disconnect")

    def dataReceived(self, data):
        if self.authenticated:
            pass

        #  Attempt authentication
        else:
            try:
                passphrase = Packet.construct_from_encoded_json(data).data
                print(passphrase)
                if passphrase == self.factory.passphrase:
                    self.authenticated = True
                    self.transport.write(Packet("authenticated").convert_to_encoded_json())
                else:
                    self.transport.write(Packet("not authenticated").convert_to_encoded_json())
                    self.transport.loseConnection()
            except json.JSONDecodeError:
                print("Packet corrupted or in incorrect format")
