import modules.game_controller as gc
from PIL import Image
from time import sleep

def main():
    controller = gc.Controller()
    screenshot = controller.get_screenshot()
    for i in range(10):
        screenshot.save("screenshot.png")
        sleep(1)

main()