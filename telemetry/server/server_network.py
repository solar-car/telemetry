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
        self.tcp_authentication_port = self.settings["TCPAuthPort"]

    def run(self):
        auth_endpoint = TCP4ServerEndpoint(reactor, 1776)
        auth_endpoint.listen(HandleAuthenticationAttemptFactory())
        reactor.run(installSignalHandlers=False)


class HandleAuthenticationAttemptFactory(Factory):
    def __init__(self):
        self.passphrase = "hello"

    def buildProtocol(self, addr):
        return HandleAuthenticationAttempt(self)


class HandleAuthenticationAttempt(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        print("connection")

    def connectionLost(self, reason=ConnectionDone):
        print("disconnect")

    def dataReceived(self, data):
        try:
            passphrase = Packet.construct_from_encoded_json(data).data
            print(passphrase)
            if passphrase == self.factory.passphrase:
                self.transport.write(Packet("authenticated").convert_to_encoded_json())
            else:
                self.transport.write(Packet("not authenticated").convert_to_encoded_json())
        except json.JSONDecodeError:
            print("Packet corrupted or in incorrect format")
        finally:
            self.transport.loseConnection()  # Close out the connection
