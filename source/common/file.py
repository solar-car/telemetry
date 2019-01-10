import datetime
from enum import Enum
from xml.etree import ElementTree

from source.common.data import Sensor


class Parser:
    # Specifies the form in which the data from the parser will be returned

    class SectionKey(Enum):
        MODULES = "Modules"
        SETTINGS = "Settings"

    def __init__(self):
        self.path = "../../Data/Parameters.xml"

    def parse_xml(self, section_key):
        xml_tree = ElementTree.parse(self.path)
        root = xml_tree.getroot()

        if section_key == self.SectionKey.MODULES:
            return self.parse_modules(root.find("Modules"))
        elif section_key == self.SectionKey.SETTINGS:
            return self.parse_settings(root.find("Settings"))
        else:
            raise ValueError("Section key not supported")

    def parse_modules(self, tree):
        module_data = {}
        for module in tree:
            module_specific_data = {}
            for sensor in module:
                sensor_data = sensor.attrib
                sensor_data["gpio_pin"] = int(sensor.text)
                module_specific_data[sensor.tag] = sensor_data
            module_data[module.tag] = module_specific_data
        return module_data

    def parse_settings(self, tree):
        settings = {}
        for section in tree:
            section_dict = {}
            for setting in section:
                setting_value = setting.text if setting.text else ""
                try:
                    setting_value = int(setting_value)
                except ValueError:
                    pass

                section_dict[setting.tag] = setting_value
            settings[section.tag] = section_dict
        return settings


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

