import datetime
from xml.etree import ElementTree


class Parser:
    @staticmethod
    def parse_xml(section_key):
        path = "Parameters.xml"
        xml_tree = ElementTree.parse(path)
        root = xml_tree.getroot()

        if section_key == "Modules":
            return Parser.parse_modules(root.find(section_key))
        elif section_key == "Settings":
            return Parser.parse_settings(root.find(section_key))
        else:
            raise ValueError("Section key not supported")

    @staticmethod
    def parse_modules(tree):
        module_data = {}
        for module in tree:
            module_specific_data = {}
            for sensor in module:
                sensor_data = sensor.attrib
                sensor_data["gpio_pin"] = int(sensor.text)
                module_specific_data[sensor.tag] = sensor_data
            module_data[module.tag] = module_specific_data
        return module_data

    @staticmethod
    def parse_settings(tree):
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
    @staticmethod
    def log_data(data):
        path = "Data/ClientLog.txt"
        with open(path, 'a') as file:
            timestamp = datetime.datetime.now()
            file.write(f"{data} :: {timestamp}" + '\n')

