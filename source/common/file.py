import datetime
from enum import Enum
from xml.etree import ElementTree


class Parser:
    # Specifies the form in which the data from the parser will be returned
    class ReturnType(Enum):
        STRING = 0  # Returns data as a string even if it can be further converted into an int
        VALUE = 1  # Returns the data as an int if it can be converted and as a string otherwise

    class SectionKey(Enum):
        MODULES = "Modules"
        SETTINGS = "Settings"

    def __init__(self):
        self.path = "../../Data/Parameters.xml"

    def parse_xml(self, section_key, return_type):
        xml_tree = ElementTree.parse(self.path)
        root = xml_tree.getroot()

        if section_key == self.SectionKey.MODULES:
            return self.parse_modules(root.find("Modules"), return_type)
        elif section_key == self.SectionKey.SETTINGS:
            return self.parse_settings(root.find("Settings"), return_type)
        else:
            raise ValueError("Section key not supported")

    def parse_modules(self, tree, return_type):
        for module in tree:
            print(list(module))

    def parse_settings(self, tree, return_type):
        settings = {}
        for setting in tree:
            settings[setting.text] = ([list(setting))

        print(settings)


class Logger:
    """
    Writes received data to the disk
    """
    def __init__(self):
        self.path = "../../Data/Log.txt"

    def log_data(self, data):
        with open(self.path, 'a') as file:
            timestamp = datetime.datetime.now()
            file.write(f"{data} :: {timestamp}" + '\n')

