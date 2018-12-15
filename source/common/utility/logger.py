import datetime

class Logger:
    @staticmethod
    def log_data(data):
        log_file_path = "../../Data/log.txt"

        with open(log_file_path, 'a') as file:
            timestamp = datetime.datetime.now()
            file.write(f"{data} :: {timestamp}" + '\n')

