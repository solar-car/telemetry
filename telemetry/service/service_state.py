from common.file import Parser


class ServiceStateHandler:
    def __init__(self):
        self.settings = Parser.parse_xml("Settings")
        
        # Data storage
        self.modules = []
        self.credentials = None
        
        # Flags that can only be deduced at runtime
        self.server_connection_status = False
        self.raspberry_pi_connection_status = False

class Sensor:
    pass