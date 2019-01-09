import datetime
from enum import Enum
from xml.etree import ElementTree


# Specifies the form in which the data from the parser will be returned
class ParserReturnType(Enum):
    STRING_LIST = 0  # List of strings
    STRING = 1  # Singular string
    CONVERTED_STRING = 2  # Singular string or integer value as appropriate, used for settings


class Parser:
    """
    Loads application data from the disk
    """
    def __init__(self):
        self.path = "../../Data/Parameters.xml"

    def parse_xml_as_dictionary(self, section_key, return_type=ParserReturnType.STRING_LIST):
        parsed_data = {}
        root = ElementTree.parse(self.path).getroot()
        test = root.iter(section_key)
        for element in test:
            for subelement in element:
                parsed_data[subelement.tag] = self.parse_xml_subelement(subelement, return_type)

        return parsed_data

    def parse_xml_subelement(self, subelement, return_type):
        subelement_data = {}
        for attribute in subelement:
            data = attribute.text.split(",") if attribute.text else None
            if data:
                data = self.restructure_data(data, return_type)

            subelement_data[attribute.tag] = data

        return subelement_data

    def restructure_data(self, data, return_type):
        if return_type == ParserReturnType.STRING_LIST:
            data = data  # Return as a list of strings
        elif return_type == ParserReturnType.STRING:
            data = data[0]
        elif return_type == ParserReturnType.CONVERTED_STRING:
            try:
                data = int(data[0])
            except ValueError:
                data = data[0]
        else:
            raise ValueError("Enumerate value not defined")

        return data


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

