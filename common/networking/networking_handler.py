from twisted.internet import reactor
from common.networking.protocol import Client, Service

class NetworkingHandler:
    def __init__(self, key):
        self.recv_data = {}
        self.host_data = {"service": "127.0.0.1", "client":"127.0.0.2"}
        self.port = 1776

        if key == "client":
            self.protocol = Client(self, self.host_data[key], self.port)
        elif key == "service":
            self.protocol = Service(self, self.host_data[key], self.port)

        reactor.listenUDP(self.port, self.protocol, interface=self.host_data[key])
        reactor.run()