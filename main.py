import modules.game_controller as gc
import modules.algorithms as alg
from PIL import Image
from time import sleep
import keyboard

run_deck = "red_deck"
stake = "white_stake"

def main():
    isDone = False
    controller = gc.Controller()
    state = "in_game"
    alg.Algorithm(run_deck, stake, controller)

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
                        
                        # Selects the deck
                        decks = ["red_deck", "blue_deck", "yellow_deck", "green_deck", "black_deck", "magic_deck", "nebula_deck"]
                        current_deck = controller.find_closest_match(screenshot, "deck", "openCVData/decks")
                        print(current_deck)
                        index_difference = decks.index(run_deck) - decks.index(current_deck)
                        print("difference: " + str(index_difference))
                        for i in range(abs(index_difference)):
                            if index_difference < 0:
                                controller.click(630, 386)
                            else:
                                controller.click(1292, 386)

                        # Selects the stake
                        stakes = ["white_stake", "red_stake"]
                        current_stake = controller.find_closest_match(screenshot, "stake", "openCVData/stakes")
                        print(current_stake)
                        index_difference = stakes.index(stake) - stakes.index(current_stake)
                        print("difference: " + str(index_difference))
                        for i in range(abs(index_difference)):
                            if index_difference < 0:
                                controller.click(630, 634)
                            else:
                                controller.click(1286, 634)

                        controller.click(952, 840)
                        state = "in_game"
                    case "continueRunMenu":
                        print("Continue Run")
                        controller.click(740, 182)
                    case _:
                        print("Unknown Screen")
                        # isDone = True
            case "in_game":
                match controller.find_closest_match(screenshot, "screen_type", "openCVData/screens"):
                    case "blind_select_small":
                        print("Bind Selection")
                    case "blind_select_big":
                        print("Bind Selection")
                    case "blind_select_boss":
                        print("Bind Selection")
                    case "in_bind":
                        print("In Bind")


                        bind_data = controller.handle_bind()
                        print(bind_data)
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