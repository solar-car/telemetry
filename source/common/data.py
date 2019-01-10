from enum import Enum


class DataHandler:
    """
    Manages the data and state of the application
    """
    def __init__(self, module_data, settings):
        self.modules = []
        self.server_connection_status = False
        self.raspberry_pi_connection_status = False
        self.settings = settings

        self.create_modules(module_data)

    def create_modules(self, module_data):
        for module_name in module_data:
            self.modules.append(Module(module_name, module_data[module_name]))


class Module:
    def __init__(self, name, module_data):
        self.name = name
        self.sensors = {}
        self.attributes = module_data.keys()

        self.gpio_inputs = module_data["GPIO_Input"]
        self.gpio_outputs = module_data["GPIO_Output"]

        for input in self.gpio_inputs:
            self.sensors[input] = 0

    def get_sensor_data(self):
        for input in self.gpio_inputs:
            self.gpio_inputs[input] = self.get_gpio_pin_data(input)

    def get_gpio_pin_data(self, pin_no):
        #  Placeholder until implementation of interfacing with the Raspberry Pi GPIO pins
        return -1


class Sensor:
    class Mode(Enum):
        INPUT = 0
        OUTPUT = 1

    def __init__(self, gpio_pin, mode, label):
        self.gpio_pin = gpio_pin
        self.mode = mode
        self.label = label
