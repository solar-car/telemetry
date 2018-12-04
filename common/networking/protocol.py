from twisted.internet.protocol import DatagramProtocol


class Communicate(DatagramProtocol):
    def datagramReceived(self, data, addr):
        print("received %r from %s" % (data, addr))
        self.transport.write(data, addr)
