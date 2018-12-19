from source.common.data_parser import DataParser
from source.service.module import Module


class ModuleHandler:
    def __init__(self):
        self.modules = []
        self.create_modules()
    
    def create_modules(self):
        module_data = DataParser.parse_file("module")
        for module_data_list in module_data:
            new_module = Module(module_data_list)
            self.modules.append(new_module)
