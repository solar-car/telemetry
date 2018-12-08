import time
import pickle
import copy

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall


class Packet:
    def __init__(self, data):
        self.timestamp = time.time()
        self.data = data

    def decode(self):
        return self.data, self.timestamp


class Client(DatagramProtocol):
    def __init__(self, handler, host, port, service_host):
        self.handler = handler
        self.host = host
        self.port = port
        self.service_host = service_host
        self.loopObj = None

    def datagramReceived(self, datagram, addr):
        host = addr[0]

        deserialized_packet = pickle.loads(datagram)
        print(deserialized_packet.data)
        try:
            self.handler.recv_data[host].append(deserialized_packet)

        except KeyError:
            self.handler.recv_data[host] = []
            self.handler.recv_data[host].append(deserialized_packet)

    def startProtocol(self):
        self.loopObj = LoopingCall(self.send_heartbeat)
        self.loopObj.start(1, now=False)
        self.transport.connect(self.service_host, self.port)

    def send_heartbeat(self):
        self.transport.write(b".")


class Service(DatagramProtocol):
    def __init__(self, handler, host, port):
        self.handler = handler
        self.host = host
        self.port = port
        self.loopObj = None

    def startProtocol(self):

        self.loopObj = LoopingCall(self.send_data)
        self.loopObj.start(1, now=False)

        self.loopObj = LoopingCall(self.sendMessage)
        self.loopObj.start(2, now=False)

    def stopProtocol(self):
        pass

    def datagramReceived(self, datagram, addr):
        if addr not in self.handler.connected_hosts:
            self.handler.connected_hosts.append(addr)

    def send_data(self):
        packet = Packet(copy.deepcopy(self.handler.buffer))  # Make a deep copy of the data

        if len(packet.data) > 0 and len(self.handler.connected_hosts) > 0: # If there is buffered data and listening hosts
            serialized_packet = pickle.dumps(packet)
            for connected_host in self.handler.connected_hosts:
                self.transport.write(serialized_packet, connected_host)
            self.handler.buffer.clear()

