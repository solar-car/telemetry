from enum import Enum

from telemetry.file import Parser


class ClientStateHandler:
    """
    Maintains the persistent state and data of the application
    """
    def __init__(self):
        # Data storage
        self.modules = []

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
