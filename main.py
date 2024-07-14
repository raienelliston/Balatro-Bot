import modules.game_controller as gc
import modules.algorithms as alg
from PIL import Image
from time import sleep
import traceback
import keyboard

run_deck = "red_deck"
stake = "white_stake"

def main():
    isDone = False
    controller = gc.Controller()
    state = "in_game"
    algorithm = alg.Algorithm(run_deck, stake, controller)

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
                        controller.click(700, 385)
                    case "blind_select_big":
                        print("Bind Selection")
                        controller.click(1040, 385)
                    case "blind_select_boss":
                        print("Bind Selection")
                        controller.click(1390, 385)
                    case "in_bind":
                        print("In Bind")

                        try:
                            if algorithm.current_bind_type == "boss":
                                algorithm.boss = controller.identify_boss()
                            hand_size = algorithm.hand_size
                            bind_data = controller.get_bind_data(hand_size, len(algorithm.jokers), len(algorithm.consumables))
                            algorithm.pre_bind_logic(bind_data)
                            print(bind_data)
                            action = algorithm.handle_bind(bind_data)
                            
                            print(action)
                            match action["action"]:
                                case "play":
                                    controller.select_cards(action["hand"], "hand_bind", click=True, hand_size=hand_size)
                                    controller.click(800, 975)
                                case "discard":
                                    controller.select_cards(action["hand"], "hand_bind", click=True, hand_size=hand_size)
                                    controller.click(1250, 975)
                                case "comsume":
                                    controller.use_consumable(action["consumable"], action["index"])
                                case _:
                                    print("Unknown Action")
                                    pass
                        except Exception as e:
                            print("Error getting bind data")
                            print(traceback.format_exc())


                    case "shop":
                        print("Shop")

                        get_shop_bonuses = algorithm.get_shop_bonuses()
                        shop_items = controller.get_shop_items(get_shop_bonuses)
                        shop_changes = algorithm.handle_shop(shop_items)
                        
                        for item in shop_changes:
                            if item["action"] == "buy":
                                controller.buy(item["name"], shop_items)
                            elif item["action"] == "skip":
                                controller.sell(item["name"], shop_items)
                            else:
                                print("Unknown Shop Action")
                        
                        controller.click(800, 975)
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