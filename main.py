import modules.game_controller as gc
from PIL import Image
from time import sleep
import keyboard

run_deck = "red_deck"

def main():
    isDone = False
    controller = gc.Controller()
    state = "before_game"

    # Main Loop
    while not isDone:
        screenshot = controller.get_screenshot()
        match state:
            case "before_game":
                match controller.find_closest_match(screenshot, "screen_type", "openCVData/screens"):
                    case "mainMenu":
                        print("Main Menu")
                        controller.click(568, 932)
                    case "newRunMenu":
                        print("New Run")
                        
                        decks = ["red_deck", "blue_deck", "yellow_deck", "green_deck", "black_deck", "magic_deck", "nebula_deck"]

                        current_deck = controller.get_screen_part(screenshot, "openCVData/parts/newRunMenu/continue.png")

                        index_difference = decks.index(run_deck) - decks.index(current_deck)
                        print("difference: " + str(index_difference))

                        # controller.click(952, 840)
                    case "continueRunMenu":
                        print("Continue Run")
                        controller.click(740, 182)
                    case _:
                        print("Unknown Screen")
                        # isDone = True
            case "in_game":
                match controller.find_closest_match(screenshot, "screen_type", "openCVData/screens"):
                    case "bind_selection":
                        print("Bind Selection")
                    case "inBind":
                        print("In Bind")
                    case "shop":
                        print("Shop")
                    case _:
                        print("Unknown Screen")
                        # isDone = True

        # User Control
        while not keyboard.is_pressed("q"):
            if keyboard.is_pressed("e"):
                exit()

        # Sleep for 1 second for testing purposes
        sleep(1)


main()