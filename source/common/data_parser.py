import string

class DataParser:
    
    @staticmethod
    def parse_file(path_type, line_type=None):
        path_associations = {'module': '../../Data/Modules.data', 'settings': '../../Data/Settings.data'}
        file_parsed_data = []  # List to be returned after the file is parsed
        
        with open(path_associations[path_type], 'r') as file:
            for line in file:
                line_data = DataParser.parse_line(line, line_type)
                if line_data:  # If the function does not return 'None'
                    file_parsed_data.append(line_data)
                        
        return file_parsed_data

    @staticmethod
    def parse_line(line, line_type):
        line_data = []
        left_delimiter = "[" 
        right_delimiter = "]"
        ignore_characters = [" ", "#"]
                
        left_bounds = []
        right_bounds = []
        
        if line[0] in ignore_characters:
            pass

        else:
            for index, char in enumerate(line):
                if char == left_delimiter:
                    left_bounds.append(index)
                elif char == right_delimiter:
                    right_bounds.append(index)

            for section_index in range(len(left_bounds)):
                section_data = line[left_bounds[section_index]+1 : right_bounds[section_index]]
                section_data = ''.join([char for char in section_data if char != ','])

                if section_index == 0:
                    if line_type:
                        if line_type == section_data:
                            line_data.append(section_data)
                        else:
                            break
                    else:
                        line_data.append(section_data)
                else:
                    try:
                        line_data.append(int(section_data))
                    except:
                        line_data.append(section_data)

        return line_data

    @staticmethod
    def load_as_dictionary(path_type, line_type):
        dict = {}
        data = DataParser.parse_file(path_type, line_type)

        for setting in data:
            key = setting[1]
            dict[key] = None
            for index, section in enumerate(setting):
                if index != 1 and index != 0:
                    dict[key] = section
        return dict.copy()
