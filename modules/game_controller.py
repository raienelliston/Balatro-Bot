import pygetwindow as gw
import pyautogui as pag
import pytesseract
import keyboard
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

    def select_cards(self, hand, type, click=False, hand_size=0):
        
        match type:
            case "hand_bind":
                start = 546
                interval = 978 / hand_size
                start += interval / 2
                for i in hand:
                    print(hand, i)
                    self.move_mouse(start + interval * i, 778)
                    if click:
                        self.click(start + interval * i, 778)
                    print(i)

    def click(self, x, y, absolute=False):
        # Changes the coordinats to account for different window sizes and locations
        if not absolute:
            x = self.balatro.width / 1920 * x
            y = self.balatro.height / 1080 * y
        x = self.balatro.left + x
        y = self.balatro.top + y

        pag.moveTo(x, y)
        # pag.click(x, y) 

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

        # Check for the current round score

        text = self.read_text((236, 410, 488, 465))
        print(text)

        text = text.split(" ")[-1]
        text = text.replace("#", "")
        text = text.replace("\n", "")
        text = text.replace("*", "")
        text = text.replace("N", "0")
        if not text[0].isnumeric():
            text = text[1:]
        current_score = int(text)

        print(current_score)

        return {
            "current_score": current_score,
        }

    def identify_hand(self, hand_size):

        if hand_size == 0:
            return []

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
            card = ["", "", "N", "N", "N"]
            
            self.move_mouse(start + interval * (i + 0.5), 778)
            time.sleep(0.07)

            screenshot = pag.screenshot(region=(check_area[0], check_area[1], check_area[2] - check_area[0], check_area[3] - check_area[1]))
            screenshot.save("screenshot.png")


            best = ["", 0]
            for f in os.listdir("openCVData/suits"):
                img = cv.imread("openCVData/suits/" + f, 0)
                check = cv.imread("screenshot.png", 0)
                result = cv.matchTemplate(img, check, cv.TM_CCOEFF_NORMED).max()
                if result > best[1]:
                    best = [f[:-4], result]
            card[0] = best[0]

            best = ["", 0]
            for f in os.listdir("openCVData/values"):
                img = cv.imread("openCVData/values/" + f, 0)
                check = cv.imread("screenshot.png", 0)
                result = cv.matchTemplate(img, check, cv.TM_CCOEFF_NORMED).max()
                if result > best[1]:
                    best = [f[:-4], result]
            card[1] = best[0]

            for f in os.listdir("openCVData/enchantments"):
                img = cv.imread("openCVData/enchantments/" + f, 0)
                check = cv.imread("screenshot.png", 0)
                result = cv.matchTemplate(img, check, cv.TM_CCOEFF_NORMED).max()
                if result > 0.85:
                    card[2] = f[:-4]
                    break

            for f in os.listdir("openCVData/editions"):
                img = cv.imread("openCVData/editions/" + f, 0)
                check = cv.imread("screenshot.png", 0)
                result = cv.matchTemplate(img, check, cv.TM_CCOEFF_NORMED).max()
                if result > 0.85:
                    card[3] = f[:-4]
                    break
            
            for f in os.listdir("openCVData/seals"):
                img = cv.imread("openCVData/seals/" + f, 0)
                check = cv.imread("screenshot.png", 0)
                result = cv.matchTemplate(img, check, cv.TM_CCOEFF_NORMED).max()
                if result > 0.85:
                    card[4] = f[:-4]
                    break

            card = str(card[0]) + str(card[1]) + str(card[2]) + str(card[3] + str(card[4]))

            if card[3] == "R": # Special case for the stone cards
                card = "R0R" + card[3:]

            hand.append(card)
        print(hand)
        return hand

    def identify_jokers(self, joker_amount):

        if joker_amount == 0:
            return []

        check_area = (int(self.balatro.width / 1920 * 456), int(self.balatro.width / 1920 * 284), int(self.balatro.width / 1920 * 1470), int(self.balatro.width / 1920 * 560))
        start = 0
        end = 0
        interval = (end - start) / joker_amount

        jokers = []
        for i in len(joker_amount):
            joker = {
                "name": "",
                "enchantment": "",
                "value": 1
            }

            self.move_mouse(start + interval * (i + 0.5), 778)
            time.sleep(0.07)

            screenshot = pag.screenshot(region=(check_area[0], check_area[1], check_area[2] - check_area[0], check_area[3] - check_area[1]))
            screenshot.save("screenshot.png")

            best = ["", 0]
            for f in os.listdir("openCVData/jokers"):
                img = cv.imread("openCVData/jokers/" + f, 0)
                check = cv.imread("screenshot.png", 0)
                result = cv.matchTemplate(img, check, cv.TM_CCOEFF_NORMED).max()
                if result > best[1]:
                    best = [f[:-4], result]
            joker["name"] = best[0]

            for f in os.listdir("openCVData/joker_enchantments"):
                img = cv.imread("openCVData/joker_enchantments/" + f, 0)
                check = cv.imread("screenshot.png", 0)
                result = cv.matchTemplate(img, check, cv.TM_CCOEFF_NORMED).max()
                if result > 0.85:
                    joker[1] = f[:-4]
                    break
            joker["enchantment"] = f[:-4]

            jokers.append(joker)
        return jokers

    def identify_consumables(self, consumable_amount):

        if consumable_amount == 0:
            return []

        check_area = (int(self.balatro.width / 1920 * 1332), int(self.balatro.width / 1920 * 284), int(self.balatro.width / 1920 * 1902), int(self.balatro.width / 1920 * 506))
        start = 0
        end = 0
        interval = (end - start) / consumable_amount

        consumables = []
        for i in len(consumable_amount):
            consumable = {
                "name": "",
                "enchantment": "",
                "value": 1
            }

            self.move_mouse(start + interval * (i + 0.5), 778)
            time.sleep(0.07)

            screenshot = pag.screenshot(region=(check_area[0], check_area[1], check_area[2] - check_area[0], check_area[3] - check_area[1]))
            screenshot.save("screenshot.png")

            best = ["", 0]
            for f in os.listdir("openCVData/consumables"):
                img = cv.imread("openCVData/consumables/" + f, 0)
                check = cv.imread("screenshot.png", 0)
                result = cv.matchTemplate(img, check, cv.TM_CCOEFF_NORMED).max()
                if result > best[1]:
                    best = [f[:-4], result]
            consumable["name"] = best[0]

            for f in os.listdir("openCVData/consumable_enchantments"):
                img = cv.imread("openCVData/consumable_enchantments/" + f, 0)
                check = cv.imread("screenshot.png", 0)
                result = cv.matchTemplate(img, check, cv.TM_CCOEFF_NORMED).max()
                if result > 0.85:
                    consumable[1] = f[:-4]
                    break
            consumable["enchantment"] = f[:-4]

            consumables.append(consumable)
        return consumables

    def identify_boss(self):
        check_area = (int(self.balatro.width / 1920 * 82), int(self.balatro.width / 1920 * 240), int(self.balatro.width / 1920 * 216), int(self.balatro.width / 1920 * 360))

        boss = ""

        screenshot = pag.screenshot(region=(check_area[0], check_area[1], check_area[2] - check_area[0], check_area[3] - check_area[1]))
        screenshot.save("screenshot.png")

        best = ["", 0]
        for f in os.listdir("openCVData/boss_binds"):
            img = cv.imread("openCVData/boss_binds/" + f, 0)
            check = cv.imread("screenshot.png", 0)
            result = cv.matchTemplate(img, check, cv.TM_CCOEFF_NORMED).max()
            if result > best[1]:
                best = [f[:-4], result]
        boss = best[0]

        return boss

    def use_consumable(self, consumable, index):
        pass

    def get_bind_data(self, hand_size=0, joker_amount=0, consumable_amount=0):
        info = self.analyze_in_bind()
        hand = self.identify_hand(hand_size)
        jokers = self.identify_jokers(joker_amount)
        consumables = self.identify_consumables(consumable_amount)
        return {
            "current_score": info["current_score"],
            "hand": hand,
            "jokers": jokers,
            "consumables": consumables,
        }

    def get_shop_items(self, bonuses):
        self.consumable = []
        self.vouchers = []
        self.packs = []

        consumable_amount = bonuses["consumables"]
        voucher_amount = bonuses["vouchers"]
        pack_amount = 2

        # Screenshot
        area = (int(self.balatro.width / 1920 * 370), int(self.balatro.width / 1920 * 400), int(self.balatro.width / 1920 * 1920), int(self.balatro.width / 1920 * 1080))
        screenshot = pag.screenshot(region=area)
        screenshot.save("screenshot.png")

        # Get consumables
        best = []
        for consum in os.listdir("openCVData/consumables"):
            img = cv.imread("openCVData/consumables/" + consum, 0)
            check = cv.imread("screenshot.png", 0)
            result = cv.matchTemplate(img, check, cv.TM_CCOEFF_NORMED).max()
            best.append([consum, result])
        best.sort(key=lambda x: x[1]).reverse()
        self.consumable.append(best[:consumable_amount])
        
        # Get vouchers
        best = []
        for vouch in os.listdir("openCVData/vouchers"):
            img = cv.imread("openCVData/vouchers/" + vouch, 0)
            check = cv.imread("screenshot.png", 0)
            result = cv.matchTemplate(img, check, cv.TM_CCOEFF_NORMED).max()
            best.append([vouch, result])
        best.sort(key=lambda x: x[1]).reverse()
        self.vouchers.append(best[:voucher_amount])

        # Get packs
        best = []
        for pack in os.listdir("openCVData/packs"):
            img = cv.imread("openCVData/packs/" + pack, 0)
            check = cv.imread("screenshot.png", 0)
            result = cv.matchTemplate(img, check, cv.TM_CCOEFF_NORMED).max()
            best.append([pack, result])
        best.sort(key=lambda x: x[1]).reverse()
        self.packs.append(best[:pack_amount])
    
        return self.consumable + self.vouchers + self.packs

    def select_shop_item(self, item, index):
        
        start = [916, 554]
        distance = 1416 - 916
        if len(self.consumable) % 1 == 0:
            start[0] += distance / self.consumable
        for index, value in enumerate(self.consumable):
            if value in item:
                self.move_mouse(start[0] + (distance + index), start[1])
                self.click(start[0] + (distance + index), start[1])
                item.remove(value)

        start = [752, 894]
        distance = 944 - 752
        if len(self.vouchers) % 1 == 0:
            start[0] += distance / self.vouchers
        for index, item in enumerate(self.vouchers):
            if value in item:
                self.move_mouse(start[0] + (distance + index), start[1])
                self.click(start[0] + (distance + index), start[1])
                item.remove(value)

        start = [1184, 882]
        distance = 1372 - 1184
        if len(self.packs) % 1 == 0:
            start[0] += distance / self.packs
        for index, value in enumerate(self.packs):
            if value in item:
                self.move_mouse(start[0] + (distance + index), start[1])
                self.click(start[0] + (distance + index), start[1])
                item.remove(value)

if __name__ == "__main__":
    controller = Controller()
    # controller.resize_window(1920, 1080)
