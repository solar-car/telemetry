import datetime
import json
from enum import Enum


class AuthenticationResult(Enum):
    AUTHENTICATED = "authenticated"
    NOT_AUTHENTICATED = "not authenticated"


class Packet:
    def __init__(self, data=""):
        self.data = data
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
