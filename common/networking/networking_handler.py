from common.networking.protocol import ClientFactory, ServiceFactory
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, TCP4ServerEndpoint

class NetworkingHandler:
    def __init__(self, key):
        if key == "client":
            self.factory = ClientFactory()
        elif key == "service":
            self.factory = ServiceFactory()

        self.endpoint = TCP4ServerEndpoint(reactor, self.factory.port)
        self.endpoint.listen(self.factory)
        reactor.run()


