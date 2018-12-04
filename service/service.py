from service.intermediary.module_handler import ModuleHandler
from common.networking.networking_handler import NetworkingHandler

class TelemetryService:
    def __init__(self):
        self.name_key = "service"
        self.module_handler = ModuleHandler()
        self.networking_handler = NetworkingHandler()

telemetry_service = TelemetryService()
