import pygetwindow as gw
import pyautogui as pag
import pytesseract
# from modules.logger import Logger
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

        self.checks = {}


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
    
    # Checks specific parts of the screen for matching images in openCVData/parts
    def get_screen_part(self, screenshot, path):
        screenshot.save("screenshot.png")
        if path.isFile():
            img = cv.imread(path, 0)
            check = cv.imread("screenshot.png", 0)
            result = cv.matchTemplate(img, check, cv.TM_CCOEFF_NORMED).max()
            if result > 0.8:
                pass
            else:
                return None
        else:
            pass
            return None

    def find_closest_match(self, screenshot, type, path="/"):
        # Loads the checks if not already loaded
        try:
            self.checks[type]
        except KeyError:
            self.checks[type] = None
            if self.checks[type] == None: 
                self.checks[type] = []
                for f in os.listdir(path):
                    self.checks[type].append({
                        "img": cv.imread(path + "/" + f, 0),
                        "name": f
                        })

        # Checks the screenshot against all the checks
        screenshot.save("screenshot.png")
        confidence = []
        for f in self.checks[type]:
            check = cv.imread("screenshot.png", 0)
            result = cv.matchTemplate(f['img'], check, cv.TM_CCOEFF_NORMED).max()
            confidence.append(result)
        print("confidence: ", str(confidence))
        best = max(confidence)
        print(self.checks[type][confidence.index(best)]['name'])
        return self.checks[type][confidence.index(best)]['name'][:-4]

    def ocr_scan(self, screenshot, area=None):
        if area == None:
            area = (0, 0, self.balatro.width, self.balatro.height)

        

    def click(self, x, y, absolute=False):
        # Changes the coordinats to account for different window sizes and locations
        if not absolute:
            x = self.balatro.width / 1920 * x
            y = self.balatro.height / 1080 * y
        x = self.balatro.left + x
        y = self.balatro.top + y

        pag.moveTo(x, y)
        # Commented for testing purposes
        pag.click(x, y) 
    
    def resize_window(self, width, height):
        self.balatro.resizeTo(width, height)
        self.balatro.moveTo(0, 0)


if __name__ == "__main__":
    controller = Controller()
    controller.resize_window(1920, 1080)