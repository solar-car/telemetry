from enum import Enum
import time

from telemetry.common.file import Parser
from telemetry.common.auth import Credentials, Authentication
from telemetry.common.state_handler import *


class ClientStateHandler(StateHandler):
    """
    Maintains the persistent "global" state and data of the application
    """
    def __init__(self):
        StateHandler.__init__(self)
        # Data storage
        self.modules = []
        self.credentials = None

        # Flags and other settings in XML form
        self.module_data = Parser.parse_xml("Modules")
        self.settings = Parser.parse_xml("Settings")

        # Flags that can only be deduced at runtime
        self.server_connection_status = False
        self.raspberry_pi_connection_status = False
        self.rsa_key_exists = False

        self.create_modules(self.module_data)

    def create_modules(self, module_data):
        for module_name in module_data:
            self.modules.append(Module(module_name, module_data[module_name]))

    def create_credentials(self, passphrase):
        salt, salted_hash = Authentication.convert_to_salted_hash(passphrase)
        self.credentials = Credentials(salt, salted_hash)

    def update_credentials(self, new_credentials):
        print("started")
        self.credentials = new_credentials
        print(self.credentials)


class Module:
    def __init__(self, name, module_data):
        self.name = name
        self.sensors = self.create_sensors(module_data)

    def create_sensors(self, module_data):
        sensors = []
        for sensor in module_data:
            sensor_data = module_data[sensor]
            sensor_gpio_pin = sensor_data["gpio_pin"]
            sensor_mode = sensor_data["mode"]
            if sensor_mode == "input":
                sensor_mode = Sensor.Mode.INPUT
            elif sensor_mode == "output":
                sensor_mode = Sensor.Mode.OUTPUT
            sensor_unit = sensor_data["unit"]
            sensors.append(Sensor(sensor, sensor_gpio_pin, sensor_mode, sensor_unit))
        return sensors


class Sensor:
    class Mode(Enum):
        INPUT = 0
        OUTPUT = 1

    class Status(Enum):
        OPERATIONAL = "Operational"
        NON_OPERATIONAL = "?"

    def __init__(self, name, gpio_pin, mode, unit):
        self.name = name
        self.gpio_pin = gpio_pin
        self.mode = mode
        self.unit = unit
        self.status = "Operational"

        self.value = 0
        self.gui_reference = None

    def get_current_pin_value(self):
        pass
