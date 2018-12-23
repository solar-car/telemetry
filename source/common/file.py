import datetime
from xml.etree import ElementTree


class Parser:
    """
    Loads application data from the disk
    """
    def __init__(self):
        self.path = "../../Data/Parameters.xml"

    def load_as_dictionary(self, section_key):
        data_dict = {}  # Dictionary to be returned
        data_list = self.parse_xml()  # Load the data from the disk as a list
        print(data_list.)

        for line in data_list:
            key = line[1]
            data_dict[key] = []
            for index, section in enumerate(line):
                if index != 1 and index != 0:
                    data_dict[key].append(section)

        print(data_dict)
        return data_dict

    def parse_xml(self):
            return ElementTree.parse(self.path)


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

