from twisted.internet.protocol import DatagramProtocol
from twisted.internet.protocol import Factory
import time


class Client(DatagramProtocol):
    def __init__(self, factory):
        self.factory = factory
        self.transport.connect(self.factory.host, self.factory.port)

    def datagramReceived(self, data, addr):
        self.factory.packets += data

    def connect(self):
        self.transport.write(b"connecting")

class Service(DatagramProtocol):
    def __init__(self, factory):
        self.factory = factory

    def datagramReceived(self, data, addr):
        if addr not in self.factory.clients:
            self.factory.clients += addr
            print(addr)

    def sendData(self, data):
        for client in self.factory.clients:
            self.transport.write(bytes(data), ())


class ClientFactory(Factory):
    protocol = Client
    host = "192.168.1.1"
    port = 1777

    def __init__(self):
        self.packets = []

    def buildProtocol(self, addr):
        return Client(self)

class ServiceFactory(Factory):
    protocol = Service
    host = "192.168.1.1"
    port = 1776

    def __init__(self):
        self.clients = []

    def buildProtocol(self, addr):
        return Service(self)
