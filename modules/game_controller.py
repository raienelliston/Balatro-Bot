import pygetwindow as gw
from modules.logger import Logger
import os

window_name = "Balatro"
required_settings = [
    
]
default_settings = {
    "window_name": "Balatro",
    "resolution": { 
        "width": 1920,
        "height": 1080
    }
}

class Controller:
    def __init__(self):
        # Create config if not exists
        # if not os.path.exists("config.txt"):
        #     with open("config.txt", "w") as f:
        #         for setting in default_settings:
        #             f.write(f"{setting}={default_settings[setting]}\n")
        # # Opens and copies config
        # with open("config.txt") as f:
        #     self.settings = {}
        #     for line in f:
        #         key, value = line.split("=")
        #         self.settings[key] = value

        self.setting = default_settings

        # logger = Logger()

        for setting in required_settings:
            if setting not in self.settings:
                print(f"Setting {setting} not found in config.txt")
                exit()
        self.balatro = gw.getWindowsWithTitle(window_name)
        if len(self.balatro) == 0:
            print("Balatro window not found")
            return False
        
        self.balatro.resize(self.settings.resolution["width"], self.settings.resolution["height"])

if __name__ == "__main__":
    controller = Controller()