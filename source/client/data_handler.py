class DataHandler:
    def __init__(self, master):
        self.master = master
        self.server_recieved_data = []
        self.most_recent_data_packet = None

    def append_data(self, data_list):
        self.server_recieved_data.extend(data_list)
        self.most_recent_data_packet = data_list[-1]  # Last item in the list
        self.master.user_interface_handler.user_interface.populate_data_table(self.server_recieved_data)
