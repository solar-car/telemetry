from threading import Thread

from twisted.internet import reactor
from source.common.protocol import ClientUDP, ServiceUDP
from source.common.data_parser import DataParser


class NetworkingHandler(Thread):
    def __init__(self, master):
        Thread.__init__(self)
        self.master = master
        self.settings = DataParser.load_as_dictionary("settings", "Networking")

        self.send_buffer = []

        self.host_data = {"service": "127.0.0.1", "client": "127.0.0.3"}

        if self.master.name == "client":  # Client specific code
            self.protocol = ClientUDP(self, "127.0.0.1")
            self.receive_buffer = self.master.data_handler.server_recieved_data

        elif self.master.name == "service":  # Service specific code

            self.connected_hosts = {}
            self.protocol = ServiceUDP(self)

    def run(self):
        reactor.listenUDP(self.settings["UDPPort"], self.protocol, interface=self.host_data[self.master.name])
        reactor.run(installSignalHandlers=False)




