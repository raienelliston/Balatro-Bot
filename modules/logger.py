import logging
import os

class Logger:
    def __init__(self, log_folder_path):
        # Sets up files for logging
        if log_folder_path != None:
            if not os.path.exists(log_folder_path):
                os.makedirs(log_folder_path)
            self.log_folder_path = log_folder_path
        # Sets up logging, connecting to the same logger as the main running file
        self.logger = logging.getLogger(__name__)
        hdlr = logging.FileHandler(f'{log_folder_path}/myapp.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.DEBUG)

    def log(self, message):
        self.logger.debug(message)
        print(message)

if __name__ == "__main__":
    None