import pygetwindow as gw
import pyautogui as pag
import pytesseract
import time
# from modules.logger import Logger
import cv2 as cv
import os

window_name = "Balatro"
required_settings = [
    
]
default_settings = {
    "window_name": "Balatro",
    "resolution": { 
        "width": 2544,
        "height": 1431
    },
    "window_bar": True
}

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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

        self.width = self.settings["resolution"]["width"]
        self.height = self.settings["resolution"]["height"]

        # logger = Logger()

        # Setup Settings
        for setting in required_settings:
            if setting not in self.settings:
                print(f"Setting {setting} not found in config.txt")
                exit()
        
        self.get_window()

        if self.balatro.width != self.settings["resolution"]["width"] or self.balatro.height != self.settings["resolution"]["height"]:
            self.resize_window(self.settings["resolution"]["width"], self.settings["resolution"]["height"])

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

    def select_cards(self, hand, type, click=False):
        if click:
            action = self.click
        else:
            action = self.move_mouse
        match type:
            case "hand_bind":
                start = 546
                interval = 978 / (len(hand) + 1)
                for i in range(len(hand)):
                    action(start + interval * (i + 0.5), 778)

    def click(self, x, y, absolute=False):
        # Changes the coordinats to account for different window sizes and locations
        if not absolute:
            x = self.balatro.width / self.width * x
            y = self.balatro.height / self.height * y
        x = self.balatro.left + x
        y = self.balatro.top + y

        pag.click(x, y) 

    def move_mouse(self, x, y, absolute=False):
        if not absolute:
            x = self.balatro.width / 1920 * x
            y = self.balatro.height / 1080 * y
        x = self.balatro.left + x
        y = self.balatro.top + y

        pag.moveTo(x, y)
    
    def resize_window(self, width, height):
        self.balatro.resizeTo(width, height)
        self.balatro.moveTo(0, 0)


    # Give area as a tuple (x1, y1, x2, y2)
    def read_text(self, area=None, absolute=False):
        if area == None:
            area = (0, 0, self.balatro.width, self.balatro.height)
        if not absolute:
            width = area[2] - area[0]
            height = area[3] - area[1]
            width = int(self.balatro.width / 1920 * width)
            height = int(self.balatro.height / 1080 * height)
            print(width, height)
            print("asldkfjasdf")
            print(int(self.balatro.width / 1920 * area[0]), int(self.balatro.height / 1080 * area[1]), width, height)

            area = (int(self.balatro.width / 1920 * area[0]), int(self.balatro.height / 1080 * area[1]), width, height)

        print(area)
        
        screenshot = pag.screenshot(region=area)
        screenshot.save("screenshot.png")
        text = pytesseract.image_to_string(screenshot, lang='eng', config='--psm 6')
        return text
    
    def analyze_in_bind(self):
        
        # Check for the current bind amount
        
        text = self.read_text((256, 231, 484, 286))
        print(text)
        text = text.replace("\n", "")
        text = text.replace("%", "")
        text = text.replace("Y", "4")

        bind_amount = int(text.split(" ")[-1]) #Idk how to deal with e numbers

        print(bind_amount)


        # Check for the current round score

        text = self.read_text((236, 400, 488, 455))
        print(text)

        text = text.split(" ")[-1]
        text = text.replace("#", "")
        text = text.replace("\n", "")
        text = text.replace("*", "")
        if not text[0].isnumeric():
            text = text[1:]
        current_score = int(text)

        print(current_score)

        # Check hand size/amount

        text = self.read_text((1012, 862, 1076, 893))
        text = text.replace("/", " ")
        text = text.replace("\n", "")
        print(text)

        hand_size = int(text[-1])
        hand_amount = int(text[0])

        print(hand_size)
        print(hand_amount)

        # Check deck size/amount

        text = self.read_text((1649, 1013, 1774, 1054))

        print(text)
        text = text.replace("/", " ")
        text = text.replace("\n", "")
        text = text.replace("y", "4")
        text = text.replace("Y", "4")
        text = text.split(" ")
        print(text)

        deck_size = int(text[-1])
        deck_amount = int(text[0])

        if deck_size > deck_amount:
            deck_size = deck_size / 10

        return {
            "bind_amount": bind_amount,
            "current_score": current_score,
            "hand_size": hand_size,
            "hand_amount": hand_amount,
            "deck_size": deck_size,
            "deck_amount": deck_amount
        }

    def identify_hand(self, hand_size):

        check_area = (int(self.balatro.width / 1920 * 505), int(self.balatro.width / 1920 * 358), int(self.balatro.width / 1920 * 1620), int(self.balatro.width / 1920 * 644))

        # 546, 778
        #1542, 778
        farthest_distance = 1542 - 546
        interval = farthest_distance / hand_size
        start = 546
        hand = []
        print(hand_size)
        for i in range(hand_size):
        # for i in range(1):
            card = ["", "N", "N", "N"]
            
            self.move_mouse(start + interval * (i + 0.5), 778)
            time.sleep(0.4)

            screenshot = pag.screenshot(region=(check_area[0], check_area[1], check_area[2] - check_area[0], check_area[3] - check_area[1]))
            screenshot.save("screenshot.png")

            best = ["", 0]
            for f in os.listdir("openCVData/cards"):
                img = cv.imread("openCVData/cards/" + f, 0)
                check = cv.imread("screenshot.png", 0)
                result = cv.matchTemplate(img, check, cv.TM_CCOEFF_NORMED).max()
                if result > best[1]:
                    best = [f[:-4], result]
            if card[0] == "":
                card[0] = best[0]

            for f in os.listdir("openCVData/enchantments"):
                img = cv.imread("openCVData/enchantments/" + f, 0)
                check = cv.imread("screenshot.png", 0)
                result = cv.matchTemplate(img, check, cv.TM_CCOEFF_NORMED).max()
                if result > 0.85:
                    card[1] = f[:-4]
                    break

            for f in os.listdir("openCVData/editions"):
                img = cv.imread("openCVData/editions/" + f, 0)
                check = cv.imread("screenshot.png", 0)
                result = cv.matchTemplate(img, check, cv.TM_CCOEFF_NORMED).max()
                if result > 0.85:
                    card[2] = f[:-4]
                    break
            
            for f in os.listdir("openCVData/seals"):
                img = cv.imread("openCVData/seals/" + f, 0)
                check = cv.imread("screenshot.png", 0)
                result = cv.matchTemplate(img, check, cv.TM_CCOEFF_NORMED).max()
                if result > 0.85:
                    card[2] = f[:-4]
                    break

            card = str(card[0]) + str(card[1]) + str(card[2]) + str(card[3])
            hand.append(card)
        print(hand)
        return hand


    def get_bind_data(self):
        info = self.analyze_in_bind()
        self.hand = self.identify_hand(info["hand_size"])
        info["hand"] = self.hand
        return {
            "bind_amount": info["bind_amount"],
            "current_score": info["current_score"],
            "hand": info["hand"],
        }




if __name__ == "__main__":
    controller = Controller()
    # controller.resize_window(1920, 1080)
