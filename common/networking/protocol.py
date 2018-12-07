from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall


class Client(DatagramProtocol):
    def __init__(self, handler, host, port):
        self.handler = handler
        self.host = host
        self.port = port

    def datagramReceived(self, datagram, addr):
        host = addr[0]
        try:
            self.handler.recv_data[host].append(datagram.decode())
        except:
            self.handler.recv_data[host] = []
            self.handler.recv_data[host].append(datagram.decode())

        print(self.handler.recv_data)

    def startProtocol(self):
        pass

    def stopProtocol(self):
        pass


class Service(DatagramProtocol):
    def __init__(self, handler, host, port):
        self.handler = handler
        self.host = host
        self.port = port
        self.loopObj = None

    def startProtocol(self):
        self.loopObj = LoopingCall(self.sendMessage)
        self.loopObj.start(2, now=False)

    def stopProtocol(self):
        pass

    def sendMessage(self):
        i = input("Message: ")
        if i:
            self.transport.write(i.encode(), ("127.0.0.2", self.port))
        else:
            pass

    def datagramReceived(self, datagram, addr):
        print(datagram, addr)
