import time
import pickle
import copy

from twisted.internet.protocol import DatagramProtocol
from twisted.internet.task import LoopingCall


class Packet:
    def __init__(self, data):
        self.timestamp = time.time()
        self.data = data


class Connection:
    def __init__(self, addr, uptime_tick_at_creation):
        self.addr = addr
        self.last_packet_sent_tick = uptime_tick_at_creation


class ClientUDP(DatagramProtocol):
    def __init__(self, handler, service_host):
        self.handler = handler
        self.settings = self.handler.settings

        self.service_host = service_host
        self.send_heartbeat_loop = None

    def startProtocol(self):
        self.send_heartbeat_loop = LoopingCall(self.send_heartbeat)
        self.send_heartbeat_loop.start(self.settings["ClientHeartbeatSendInterval"], now=False)

    def datagramReceived(self, packet, addr):
        deserialized_packet = pickle.loads(packet)
        self.handler.update_data(deserialized_packet)

    def send_heartbeat(self):
        self.transport.write(self.settings["HeartbeatMessage"].encode(), (self.service_host, self.settings["UDPPort"]))


class ServiceUDP(DatagramProtocol):
    def __init__(self, handler):
        self.handler = handler
        self.settings = handler.settings

        self.uptime = 0

        self.send_data_loop = None
        self.increment_uptime_loop = None
        self.drop_inactive_connections_loop = None

    def startProtocol(self):

        self.send_data_loop = LoopingCall(self.send_data)
        self.send_data_loop.start(self.settings["PacketSendInterval"], now=False)

        self.increment_uptime_loop = LoopingCall(self.increment_uptime)
        self.increment_uptime_loop.start(1, now=False)  # Increment uptime every second

        self.drop_inactive_connections_loop = LoopingCall(self.drop_inactive_connections)
        self.drop_inactive_connections_loop.start(self.settings["CheckInactiveConnectionsInterval"], now=False)

    def stopProtocol(self):
        pass

    def datagramReceived(self, datagram, addr):
        if addr not in self.handler.connected_hosts.keys():
            self.handler.connected_hosts[addr] = Connection(addr, self.uptime)

        if datagram == self.settings["HeartbeatMessage"]:  # If datagram is a heartbeat
            self.handler.connected_hosts[addr].last_packet_sent_tick = self.uptime

    def send_data(self):
        packet = Packet(copy.deepcopy(self.handler.send_buffer))  # Make a deep copy of the data

        if len(packet.data) > 0 and len(self.handler.connected_hosts) > 0: # If there is buffered data and listening hosts
            serialized_packet = pickle.dumps(packet)
            for connected_host in self.handler.connected_hosts:
                self.transport.write(serialized_packet, connected_host)
            self.handler.send_buffer.clear()

    def drop_inactive_connections(self):
        for connection in list(self.handler.connected_hosts):
            if self.uptime - self.handler.connected_hosts[connection].last_packet_sent_tick > self.settings["MaxTimeBeforeDisconnect"]:
                del self.handler.connected_hosts[connection]

    def increment_uptime(self):
        self.uptime += 1
