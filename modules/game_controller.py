import pygetwindow as gw
from modules.logger import Logger

window_name = "Balatro"

class Controller:
    def __init__(self):
        balatro = gw.getWindowsWithTitle(window_name)
        print(balatro)
        if len(balatro) == 0:
            print("Balatro window not found")
            return False
        # logger = Logger()

if __name__ == "__main__":
    controller = Controller()