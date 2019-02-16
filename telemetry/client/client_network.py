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
        self.server_tcp_port = self.settings["ClientTCPPort"]
        self.client_authentication_timeout = self.settings["ClientAuthenticationTimeout"]

        self.authentication_attempts = 0
        self.authentication_state = "not authenticated"

        # Authentication connection
        self.endpoint = TCP4ClientEndpoint(reactor, self.server_host, self.server_tcp_port)

    def run(self):
        deferred = connectProtocol(self.endpoint, ServerConnection(self))
        deferred.addErrback(lambda result: print(result))
        reactor.run(installSignalHandlers=False)

    def external_update(self, updated_state):
        pass


class ServerConnection(Protocol):
    def __init__(self, context):
        self.context = context

    def connectionMade(self):
        pass

    def connectionLost(self, reason=ConnectionDone):
        print("disconnect")
        self.context.event_handler.add_task(self.context.client_state_handler.update_status, False, False)

    def dataReceived(self, packet):
        try:
            packet = Packet.construct_from_encoded_json(packet)
            if packet.type == Packet.PacketType.AUTHENTICATION:
                self.handle_authentication_response(packet)
            elif packet.type == Packet.PacketType.DATA:
                self.handle_new_data(packet)

        except json.JSONDecodeError:
            print("Authentication packet was corrupted or in incorrect format")

    def handle_authentication_response(self, packet):
        authentication_result = packet.data["server"]
        if authentication_result == AuthenticationResult.AUTHENTICATED.value:
            self.context.event_handler.add_task(
                self.context.client_state_handler.update_connection_status, True, packet.data["service_status"])

        elif authentication_result == AuthenticationResult.NOT_AUTHENTICATED.value:
            self.context.event_handler.add_task(
                self.context.client_state_handler.update_connection_status, False, False)

    def handle_new_data(self, packet):
        pass


