from enum import Enum
from copy import deepcopy

from common.file import Parser
from common.auth import Credentials, Authentication


# None of the methods of this class should be called by a non-main thread, but rather queued up in EventHandler
class ClientStateHandler:
    """
    Maintains data that needs to be accessed across threads
    """
    def __init__(self):
        # Data storage
        self.modules = []
        self.credentials = None

        # Flags and other settings in XML form
        self.module_data = Parser.parse_xml("Modules")
        self.settings = Parser.parse_xml("Settings")

        # Flags that can only be deduced at runtime
        self.server_connection_status = False
        self.raspberry_pi_connection_status = False

        self.create_modules(self.module_data)

    def create_modules(self, module_data):
        for module_name in module_data:
            self.modules.append(Module(module_name, module_data[module_name]))
        print("z")

    def create_credentials(self, passphrase):
        salt, salted_hash = Authentication.convert_to_salted_hash(passphrase)
        self.credentials = Credentials(salt, salted_hash)

    def update_credentials(self, new_credentials):
        self.credentials = new_credentials
        print("new credentials: {0}".format(self.credentials))

    def update_status(self, server_connection, raspberry_pi_connection):
        self.raspberry_pi_connection_status = raspberry_pi_connection
        self.server_connection_status = server_connection

    def quit(self):
        exit()


class Module:
    def __init__(self, name, module_data):
        self.name = name
        self.sensors = self.create_sensors(module_data)

    def create_sensors(self, module_data):
        sensors = []
        for sensor in module_data:
            sensor_data = module_data[sensor]
            sensor_gpio_pin = sensor_data["gpio_pin"]
            sensor_unit = sensor_data["unit"]
            sensors.append(Sensor(sensor, sensor_gpio_pin, sensor_unit))
        return sensors


class Sensor:
    class Status(Enum):
        OPERATIONAL = "Operational"
        NON_OPERATIONAL = "?"

    def __deepcopy__(self, memo):
        copy = type(self)()
        memo[id(self)] = copy
        copy.name = deepcopy(self.name)
        copy.gpio_pin = deepcopy(self.gpio_pin, memo)
        copy.unit = deepcopy(self.unit, memo)
        copy.status = deepcopy(self.status, memo)
        copy.value = deepcopy(self.value, memo)
        copy.gui_reference = self.gui_reference
        return copy

    def __init__(self, name="", gpio_pin=0, unit="",
                 status="Operational", value=0, gui_reference=None):
        self.name = name
        self.gpio_pin = gpio_pin
        self.unit = unit
        self.status = status
        self.value = value
        self.gui_reference = gui_reference

