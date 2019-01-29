import pickle
from threading import Thread

from twisted.internet.protocol import DatagramProtocol
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

from telemetry.common_network import Packet, Connection


class ClientNetworkingHandler(Thread):
    def __init__(self, state_handler):
        Thread.__init__(self)
        self.state_handler = state_handler
        self.settings = self.state_handler.settings["Networking"]
        self.debug_host = self.settings["ClientDebugHost"]
        self.send_buffer = []

        self.protocol = ClientUDP(self)

    def run(self):
        reactor.listenUDP(self.settings["UDPPort"], self.protocol, interface=self.debug_host)
        reactor.run(installSignalHandlers=False)

    def update_data(self, data):
        print(data)


class ClientUDP(DatagramProtocol):
    def __init__(self, handler):
        self.handler = handler
        self.settings = handler.settings
        self.send_heartbeat_loop = None

        self.service_host = self.settings["ServiceDebugHost"]

    def startProtocol(self):
        self.send_heartbeat_loop = LoopingCall(self.send_heartbeat)
        self.send_heartbeat_loop.start(self.settings["ClientHeartbeatSendInterval"], now=False)

    def datagramReceived(self, packet, addr):
        deserialized_packet = pickle.loads(packet)
        self.handler.update_data(deserialized_packet)

    def send_heartbeat(self):
        self.transport.write(self.settings["HeartbeatMessage"].encode(), (self.service_host, self.settings["UDPPort"]))
