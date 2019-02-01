import json

from threading import Thread

from twisted.internet.protocol import DatagramProtocol, Protocol, Factory, ClientFactory
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from twisted.internet.defer import Deferred
import twisted.internet.error as error
from twisted.internet.endpoints import clientFromString, connectProtocol, TCP4ClientEndpoint

from telemetry.network import Packet


class ClientNetworkingHandler(Thread):
    def __init__(self, state_handler):
        Thread.__init__(self)
        self.state_handler = state_handler
        
        # General networking settings
        self.settings = self.state_handler.settings["Networking"]
        self.client_host = self.settings["ClientDebugHost"]
        self.server_host = self.settings["ServerDebugHost"]
        self.tcp_authentication_port = self.settings["TCPAuthPort"]
        self.client_authentication_timeout = self.settings["ClientAuthenticationTimeout"]

        self.authentication_attempts = 0
        self.authentication_state = "not authenticated"
        self.passcode = "hello"

        # Authentication connection
        self.endpoint = TCP4ClientEndpoint(reactor, self.server_host, self.tcp_authentication_port)

    def authentication_connection_failed(self, deferred_result):
        self.authentication_attempts += 1
        print(deferred_result)

    def run(self):
        deferred = connectProtocol(self.endpoint, AttemptAuthentication(self))
        deferred.addErrback(self.authentication_connection_failed)
        reactor.run(installSignalHandlers=False)


class AttemptAuthentication(Protocol):
    def __init__(self, context):
        self.context = context

    def connectionMade(self):
        p = Packet(self.context.passcode)
        self.transport.write(p.convert_to_encoded_json())

    def dataReceived(self, data):
        print(Packet.construct_from_encoded_json(data).data)


# Sends heartbeat datagrams to the server to let it know the client is still listening
class MaintainConnection(DatagramProtocol):
    def __init__(self, handler):
        self.handler = handler
        self.settings = handler.settings
        self.send_heartbeat_loop = None

    def startProtocol(self):
        self.send_heartbeat_loop = LoopingCall(self.send_heartbeat)
        self.send_heartbeat_loop.start(self.settings["ClientHeartbeatSendInterval"], now=False)

    def datagramReceived(self, packet, addr):
        deserialized_packet = Packet().construct_from_encoded_json(packet)

        self.handler.update_data(deserialized_packet)

    def send_heartbeat(self):
        self.transport.write(self.settings["HeartbeatMessage"].encode(), (self.service_host, self.settings["UDPPort"]))

