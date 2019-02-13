import json

from threading import Thread

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.internet.error import ConnectionDone
from twisted.internet.endpoints import TCP4ServerEndpoint

from telemetry.common.network import Packet
from telemetry.common.state_handler import Subscriber


class ServerNetworkingHandler(Thread, Subscriber):
    def __init__(self, event_handler, settings):
        Thread.__init__(self)
        self.event_handler = event_handler
        self.settings = settings

        # General networking settings
        self.settings = self.settings["Networking"]
        self.client_host = self.settings["ClientDebugHost"]
        self.server_host = self.settings["ServerDebugHost"]
        self.client_tcp_port = self.settings["ClientTCPPort"]
        self.service_tcp_port = self.settings["ServiceTCPPort"]

        self.client_connection_endpoint = TCP4ServerEndpoint(reactor, self.client_tcp_port)
        self.service_connection_endpoint = TCP4ServerEndpoint(reactor, self.service_tcp_port)

    def run(self):
        self.client_connection_endpoint.listen(ClientConnectionFactory())
        self.service_connection_endpoint.listen(ClientConnectionFactory())
        reactor.run(installSignalHandlers=False)


class ClientConnectionFactory(Factory):
    def buildProtocol(self, addr):
        return ClientConnection(self)


class ClientConnection(Protocol):
    def __init__(self, factory):
        self.factory = factory
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


class ServiceConnection(Protocol):
    def connectionMade(self):
        pass

    def connectionLost(self, reason=ConnectionDone):
        pass

    def dataReceived(self, data):
        pass
