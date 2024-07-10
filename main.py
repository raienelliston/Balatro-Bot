import modules.game_controller as gc
from PIL import Image
from time import sleep

def main():
    isDone = False
    controller = gc.Controller()
    print(controller.get_screen_type())
    state = "before_game"

    # Main Loop
    while not isDone:
        screenshot = controller.get_screenshot()
        match state:
            case "before_game":
                match controller.get_screen_type(screenshot):
                    case "mainMenu":
                        xy = controller.get_specific_part(screenshot, "playButton.png")
                        if xy != None:
                            controller.click(xy[0], xy[1])
                    case "newRunMenu":
                        print("New Run")
                    case "continueRunMenu":
                        print("Continue Run")
                    case _:
                        print("Unknown Screen")
                        # isDone = True
            case "in_game":
                match controller.get_screen_type(screenshot):
                    case "bind_selection":
                        print("Bind Selection")
                    case "inBind":
                        print("In Bind")
                    case "shop":
                        print("Shop")
                    case _:
                        print("Unknown Screen")
                        # isDone = True
        # Sleep for 1 second for testing purposes
        sleep(1)


main()