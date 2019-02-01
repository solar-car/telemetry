from telemetry.file import Parser


class DebugStateHandler:
    def __init__(self):
        self.settings = Parser.parse_xml("Settings")
