import time


class Packet:
    def __init__(self, data):
        self.data = data
        self.timestamp = time.time()


class Connection:
    def __init__(self, addr, uptime_tick_at_creation):
        self.addr = addr
        self.last_packet_sent_tick = uptime_tick_at_creation
