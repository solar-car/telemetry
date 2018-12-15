from threading import Thread

from twisted.internet import reactor
from source.common.networking.protocol import Client, Service
from source.common.utility.data_parser import DataParser


class NetworkingHandler(Thread):
    def __init__(self, master):
        Thread.__init__(self)
        self.settings = DataParser.load_as_dictionary("settings", "Networking")
        self.buffer = []
        self.master = master

        self.recv_data = {}
        self.host_data = {"service": "127.0.0.1", "client": "127.0.0.3"}

        if self.master.name == "client":  # Client specific code
            self.protocol = Client(self, "127.0.0.1", self.settings)

        elif self.master.name == "service":  # Service specific code
            self.connected_hosts = {}
            self.protocol = Service(self, self.settings)

    def run(self):
        reactor.listenUDP(self.settings["UDPport"], self.protocol, interface=self.host_data[self.master.name])
        reactor.run(installSignalHandlers=False)






