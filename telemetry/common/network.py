import datetime
import json
from enum import Enum


class Packet:
    class AuthenticationResult(Enum):
        AUTHENTICATED = "authenticated"
        NOT_AUTHENTICATED = "not authenticated"

    class PacketType(Enum):
        DEBUG = 0
        AUTHENTICATION = 1
        DATA = 2

    def __init__(self, packet_type=PacketType.DATA, **kwargs):
        self.data = {"type": packet_type}
        self.data.update(kwargs)
        self.timestamp = str(datetime.datetime.now())

    def convert_to_encoded_json(self):
        return json.dumps(["packet", {"data": self.data, "timestamp": self.timestamp}]).encode()

    @staticmethod
    def construct_from_encoded_json(json_object):
        p = Packet()
        json_data = json.loads(json_object)[1]
        p.data = json_data["data"]
        p.timestamp = json_data["timestamp"]
        return p
