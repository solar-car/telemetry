import datetime
from xml.etree import ElementTree


class Parser:
    """
    Loads application data from the disk
    """
    def __init__(self):
        self.path = "../../Data/Parameters.xml"

    def parse_xml_as_dictionary(self, section_key):
        parsed_data = {}
        root = ElementTree.parse(self.path).getroot()
        test = root.iter(section_key)
        for element in test:
            for subelement in element:
                subelement_data = {}
                for attribute in subelement:
                    data = attribute.text.split(",") if attribute.text else None
                    if data:
                        try:
                            data = [int(data) for data in data]
                        except ValueError:
                            pass
                    subelement_data[attribute.tag] = data

                parsed_data[subelement.tag] = subelement_data

        return parsed_data


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

