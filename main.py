import modules.game_controller as gc
from PIL import Image
from time import sleep

def main():
    isDone = False
    controller = gc.Controller()
    while not isDone:
        getInfo = controller.get_screen_info()

main()