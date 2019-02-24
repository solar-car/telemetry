from telemetry.common.file import Parser


class ServiceStateHandler:
    def __init__(self):
        self.settings = Parser.parse_xml("Settings")
