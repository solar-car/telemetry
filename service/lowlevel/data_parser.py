class DataParser:
    
    @staticmethod
    def parse_file(path_type):
        path_associations = {'module': '../Data/Modules.data'}
        file_parsed_data = []  # List to be returned after the file is parsed
        
        with open(path_associations[path_type], 'r') as file:
            for line in file:
                line_data = DataParser.parse_line(line)
                if line_data:  # If the function does not return 'None'
                    file_parsed_data.append(line_data)
                        
        return file_parsed_data

    @staticmethod
    def parse_line(line):
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

                if section_index > 0:
                    section_data = [int(char) for char in section_data if char != ',']

                line_data.append(section_data)
                
        return line_data
