import json
from enum import Enum

from threading import Thread

from twisted.internet.protocol import DatagramProtocol, Protocol, Factory
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
import twisted.internet.error as error
from twisted.internet.endpoints import serverFromString, TCP4ServerEndpoint

from telemetry.network import Packet


class ServerNetworkingHandler(Thread):
    def __init__(self, state_handler):
        Thread.__init__(self)
        self.state_handler = state_handler

        # General networking settings
        self.settings = self.state_handler.settings["Networking"]
        self.client_host = self.settings["ClientDebugHost"]
        self.server_host = self.settings["ServerDebugHost"]
        self.tcp_authentication_port = self.settings["TCPAuthPort"]

    def run(self):
        auth_endpoint = TCP4ServerEndpoint(reactor, 1776)
        auth_endpoint.listen(HandleAuthenticationAttemptFactory(self))
        reactor.run(installSignalHandlers=False)


class HandleAuthenticationAttemptFactory(Factory):
    def __init__(self, handler):
        self.passphrase = "hello"

    def buildProtocol(self, addr):
        return HandleAuthenticationAttempt(self)


class HandleAuthenticationAttempt(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        print("connection")

    def dataReceived(self, data):
        try:
            passphrase = Packet.construct_from_encoded_json(data).data
            print(passphrase)
            if passphrase == self.factory.passphrase:
                self.transport.write(Packet("authenticated").convert_to_encoded_json())
            else:
                self.transport.write(Packet("not authenticated").convert_to_encoded_json())
        except:
            print("Packet corrupted or in incorrect format")


