from telemetry.unit_tests.debug import *
from telemetry.server.server_network import ServerNetworkingHandler

debug_state_handler = DebugStateHandler()

a = ServerNetworkingHandler(debug_state_handler)
a.start()