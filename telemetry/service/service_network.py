import copy
from threading import Thread

from twisted.internet.protocol import DatagramProtocol
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from twisted.internet.endpoints import connectProtocol, TCP4ClientEndpoint

from common.network import Packet, AuthenticationResult


class ServiceNetworkingHandler(Thread, Subscriber):
    def __init__(self, thread_handler, service_state_handler):
        Thread.__init__(self)
        self.thread_handler = thread_handler
        self.service_state_handler = service_state_handler
        
        # General networking settings
        self.settings = self.state_handler.settings["Networking"]
        self.server_host = self.settings["ServerDebugHost"]
        self.service_host = self.settings["ServiceDebugHost"]
        self.connection_tcp_port = self.settings["ServiceTCPPort"]
        self.auth_tcp_port = self.settings["ServiceTCPAuthPort"]

    def run(self):
        
        reactor.run(installSignalHandlers=False)

    def external_update(self, updated_state):
        pass
        
class ServerAuth(Protocol):
    def __init__(self, handler):
        self.handler = handler
        self.authenticated = False

    def connectionMade(self):
        self.handler.thread_handler.add_task(self.handler.client_state_handler.update_status, True, False)

    def connectionLost(self, reason=ConnectionDone):
        print("disconnect")
        self.handler.thread_handler.add_task(self.handler.client_state_handler.update_status, False, False)

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
                

class ServerConnection(Protocol):
    def __init__(self, handler):
        self.handler = handler
        
    def connectionMade(self):
        print("connection made")
    def connectionLost(self):
        print("connection lost")
    def dataRecieved(self, data):
        print(data)
