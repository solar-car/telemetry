from telemetry.client.client_network import *
from telemetry.unit_tests.debug import *


debug_state_handler = DebugStateHandler()

passphrase = "hello"
a = ClientNetworkingHandler(debug_state_handler)
a.start()
