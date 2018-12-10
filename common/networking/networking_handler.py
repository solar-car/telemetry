from threading import Thread

from twisted.internet import reactor
from common.networking.protocol import Client, Service


class NetworkingHandler(Thread):
    def __init__(self, master):
        Thread.__init__(self)
        self.buffer = []
        self.master = master

        self.recv_data = {}
        self.host_data = {"service": "127.0.0.1", "client": "127.0.0.3"}
        self.port = 1776

        if self.master.name == "client":  # Client specific code
            self.protocol = Client(self, self.host_data[self.master.name], self.port, self.host_data["service"])

        elif self.master.name == "service":  # Service specific code
            self.connected_hosts = {}
            self.protocol = Service(self, self.host_data[self.master.name], self.port)

    def run(self):
        reactor.listenUDP(self.port, self.protocol, interface=self.host_data[self.master.name])
        reactor.run(installSignalHandlers=False)
