class DataHandler:
    """
    Manages the data and state of the application
    """
    def __init__(self, module_data):
        self.modules = []
        self.server_connection_status = False
        self.raspberry_pi_connection_status = False

        self.create_modules(module_data)

    def create_modules(self, module_data):
        for module_data_list in module_data:
            new_module = Module(module_data_list)
            self.modules.append(new_module)


class Module:
    def __init__(self, module_data):
        self.name = module_data[0]
        self.gpio_inputs = module_data[1]
        self.gpio_outputs = module_data[2]
