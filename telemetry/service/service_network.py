import copy
from threading import Thread

from twisted.internet.protocol import DatagramProtocol
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

from telemetry.common.network import Packet, Connection


class ServiceNetworkingHandler(Thread):
    def __init__(self, state_handler):
        Thread.__init__(self)
        self.state_handler = state_handler
        self.settings = self.state_handler.settings["Networking"]
        self.debug_host = self.settings["ServiceDebugHost"]
        self.send_buffer = []

        self.connected_hosts = {}
        self.protocol = None

    def run(self):
        reactor.listenUDP(self.settings["UDPPort"], self.protocol, interface=self.debug_host)
        reactor.run(installSignalHandlers=False)

    def update_data(self, data):
        print(data)
