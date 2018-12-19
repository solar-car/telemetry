class DataHandler:
    def __init__(self, master):
        self.master = master
        self.server_recieved_data = []
        self.most_recent_data_packet = None

    def append_data(self, data_list):
        print(data_list)
        for packet in data_list:
            self.server_recieved_data.extend(packet)
            self.most_recent_data_packet = data_list[-1]  # Last item in the list
