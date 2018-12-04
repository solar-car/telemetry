from intermediary.module_handler import ModuleHandler
from common.networking.networking_handler import NetworkingHandler
import time

class TelemetryService:
    def __init__(self):
        self.key = "service"
        self.module_handler = ModuleHandler()
        self.networking_handler = NetworkingHandler(self.key)


telemetry_service = TelemetryService()
