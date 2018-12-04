from common.networking.protocol import Communicate
from twisted.internet import reactor

class NetworkingHandler:
    def __init__(self, name_key):

        port_info = {"service": 1776, "client": 1777}

        reactor.listenUDP(port_info[name_key], Communicate())
        reactor.run()

