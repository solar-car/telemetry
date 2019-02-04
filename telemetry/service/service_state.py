from telemetry.common.file import Parser
from telemetry.common.state_handler import StateHandler


class ServiceStateHandler(StateHandler):
    def __init__(self):
        self.settings = Parser.parse_xml("Settings")
        StateHandler.__init__(self)
