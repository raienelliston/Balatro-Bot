import pygetwindow as gw
import pyautogui as pag
from modules.logger import Logger
import cv2 as cv
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

        self.settings = default_settings

        # logger = Logger()

        # Setup Settings
        for setting in required_settings:
            if setting not in self.settings:
                print(f"Setting {setting} not found in config.txt")
                exit()
        
        self.get_window()

        # Get all the file paths for get_type and get_info
        self.cvTypeFiles = []
        for f in os.listdir("opencvData/types"):
            self.cvTypeFiles.append(f"opencvData/types/{f}")

        self.cvInfoFiles = []
        for f in os.listdir("opencvData/parts"):
            self.cvInfoFiles.append(f"opencvData/info/{f}")

        print(self.cvTypeFiles)
        print(self.cvInfoFiles)

    # Gets the first window selected with the window name equal to window_name
    def get_window(self):
        self.balatro = None
        while self.balatro == None:
            active = gw.getActiveWindow()
            try:
                if active.title == window_name:
                    self.balatro = active
            except AttributeError:
                pass

        print(self.balatro)

    def get_screenshot(self):
        try:
            self.get_window()
            screenshot = pag.screenshot(region=(self.balatro.left, self.balatro.top, self.balatro.width, self.balatro.height), imageFilename="screenshot.png")
            return screenshot
        except Exception as e:
            print(e)
            return None
    
    # Checks the entire screen for the matching screen type in openCVData/types
    def get_screen_type(self):
        screenshot = self.get_screenshot()
        screenshot.save("screenshot.png")
        confidence = []
        for f in self.cvTypeFiles:
            print(f)
            img = cv.imread(f, 0)
            check = cv.imread("screenshot.png", 0)
            result = cv.matchTemplate(img, check, cv.TM_CCOEFF_NORMED).max() #Causing issue
            confidence.append(result)
        print(confidence)
        best = self.cvTypeFiles[confidence.index(max(confidence))]
        return best[best.rfind("/") + 1:best.rfind(".")]

    # Checks specific parts of the screen for matching images in openCVData/parts
    def get_screen_part(self, parts):
        screenshot = self.get_screenshot()




if __name__ == "__main__":
    controller = Controller()