class Module:
    def __init__(self, module_data):
        self.name = module_data[0]
        self.gpio_inputs = [module_data[1]]
        self.gpio_outputs = [module_data[2]]

        self.data = {}

        for value in self.gpio_inputs:
            self.data[value] = 0
