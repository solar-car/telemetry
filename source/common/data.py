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
        self.attributes = module_data.keys()
        self.gpio_inputs = module_data["GPIO_Input"]
        self.gpio_outputs = module_data["GPIO_Output"]
