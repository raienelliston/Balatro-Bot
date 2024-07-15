import pandas as pd
from itertools import combinations
from collections import Counter

stake_list = [
    "white_stake",
    "red_stake",
    "green_stake",
    "black_stake",
    "blue_stake",
    "purple_stake",
    "orange_stake",
    "yellow_stake",
]

bind_base_amount = [100, 300, 800, 2000, 5000, 11000, 20000, 35000, 50000]

class Algorithm:
    def __init__(self, deck, stake, controller):
        self.controller = controller

        # Pandas setup
        self.sheet = pd.read_csv("preferences.csv")

        # All of the defualt variables
        self.deck = ["CA", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "CJ", "CQ", "CK", "DA", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "DJ", "DQ", "DK", "HA", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "HJ", "HQ", "HK", "SA", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "SJ", "SQ", "SK"]
        self.current_deck = self.deck
        self.discarded = []
        self.money = 4
        self.hands = 4
        self.hand_size = 8
        self.discards = 4
        self.current_hands = 4
        self.current_discards = 4
        self.jokers = []
        self.max_jokers = 5
        self.consumables = []
        self.max_consumables = 2
        self.vouchers = []
        self.current_bind = 1
        self.current_bind_type = "small"
        self.current_bind_amount = 300
        self.boss = None
        self.deck_type = deck
        self.stake = stake_list.index(stake)
        self.buying_preference = []
        self.hand_values = [
            {"name": "flush_five", "value": 160, "multiplier": 16, "played": 0},
            {"name": "flush_house", "value": 140, "multiplier": 14, "played": 0},
            {"name": "five_of_a_kind", "value": 120, "multiplier": 12, "played": 0},
            {"name": "straight_flush", "value": 100, "multiplier": 8, "played": 0},
            {"name": "four_of_a_kind", "value": 60, "multiplier": 7, "played": 0},
            {"name": "full_house", "value": 40, "multiplier": 4, "played": 0},
            {"name": "flush", "value": 35, "multiplier": 4, "played": 0},
            {"name": "straight", "value": 30, "multiplier": 4, "played": 0},
            {"name": "three_of_a_kind", "value": 30, "multiplier": 3, "played": 0},
            {"name": "two_pair", "value": 20, "multiplier": 2, "played": 0},
            {"name": "pair", "value": 10, "multiplier": 2, "played": 0},
            {"name": "high_card", "value": 5, "multiplier": 1, "played": 0}
        ]

        match deck:
            case "red_deck":
                self.discards += 1
            case "blue_deck":
                self.hands += 1
            case "yellow_deck":
                self.money += 10
            case "green_deck":
                None
            case "black_deck":
                self.max_jokers += 1
            case "magic_deck":
                self.max_consumables += 1
                self.vouchers.append("crystal_ball")
                self.consumables.append("fool")
                self.consumables.append("fool")
            case "nebula_deck":
                self.max_consumables -= 1
                self.consumables.append("telescope")
            case "ghost_deck":
                self.consumables.append("hex")
            case "abondoned_deck":
                self.deck = ["CA","C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "DA", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "HA", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "SA", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"]
            case "checkered_deck":
                self.deck = ["HA", "HA", "H2", "H2", "H3", "H3", "H4", "H4", "H5", "H5", "H6", "H6", "H7", "H7", "H8", "H8", "H9", "H9", "H10", "H10", "HK", "HK", "HQ", "HQ", "HJ", "HJ", "SA", "SA", "S2", "S2", "S3", "S3", "S4", "S4", "S5", "S5", "S6", "S6", "S7", "S7", "S8", "S8", "S9", "S9", "S10", "S10", "SK", "SK", "SQ", "SQ", "SJ", "SJ"]
            case "zodiac_deck":
                self.vouchers.append("tarot_merchant")
                self.vouchers.append("plant_merchant")
                self.vouchers.append("overstock")
            case "painted_deck":
                self.hand_size += 2
                self.max_jokers -= 1
            case "anaglyph_deck":
                None
            case "plasma_deck":
                None
            case "erratic_deck":
                None # NEED TO ADD DECK CHECK HERE
            case _:
                print("Unknown Deck")
                exit()

        # Handles the changes from the stake
        if stake_list.index(stake) >= 5:
            self.discards -= 1

    def identify_card(self, id):
        card = {}
        match id[0]:
            case "C":
                card["suit"] = 1
            case "D":
                card["suit"] = 2
            case "H":
                card["suit"] = 3
            case "S":
                card["suit"] = 4
            case "R":
                card["suit"] = 0
            case "W":
                card["suit"] = 5
        match id[1]:
            case "R":
                card["value"] = 0
            case "A":
                card["value"] = 1
            case "J":
                card["value"] = 11
            case "Q":
                card["value"] = 12
            case "K":
                card["value"] = 13
            case _:
                card["value"] = int(id[1])
        return card
    
    def find_best_hand(self, hand, goal=None, consumables=None):
        goal_hands = []
        best_hand = {
            "value": 0,
            "hand": [],
            "money": 0
        }
        print(hand)

        # Setup Joker Logic, mainly for copyers
        jokers = self.jokers
        joker_names = []
        sorted_jokers = jokers.sort()

        for joker in jokers:
            joker_names.append(joker['name'])

        self.joker_counter = Counter(jokers)

        def check_hand(hand_indexes):
            global best_hand
            hand = []
            for hand_index in hand_indexes:
                hand.append(hand[hand_index])
            hand_result = self.find_hand_value(hand)
            if hand_result["value"] >= goal:
                goal_hands.append(hand_result)
                return
            if hand_result["value"] > best_hand["value"]:
                best_hand = hand_result
                return

        # Calculate the value of every hand
        for index1 in range(len(hand)):
            for index2 in range(index1 + 1, len(hand)):
                for index3 in range(index2 + 1, len(hand)):
                    for index4 in range(index3 + 1, len(hand)):
                        for index5 in range(index4 + 1, len(hand)):
                            check_hand([index1, index2, index3, index4, index5])
                        check_hand([index1, index2, index3, index4])
                    check_hand([index1, index2, index3])
                check_hand([index1, index2])
            check_hand([index1])


        # for r in range(1, 6):
        #     for hand in combinations(hand, r):
        #         print(hand)
        #         hand_value = self.find_hand_value(hand)
        #         if hand_value > best_hand["value"]:
        #             best_hand["value"] = hand_value
        #             best_hand["hand"] = hand
                

        if len(goal_hands) > 0:
            goal_hands.sort(key=lambda x: x["money"])
            best_hand = goal_hands[0]

        print(best_hand)
        hand_numbers = []
        for card in best_hand["hand"]:
            for index, hand_card in enumerate(hand):
                if card == hand_card:
                    hand_numbers.append(index)
                    break
                
        
        return {
            "hand": hand_numbers,
            "value": best_hand["value"]
        }

    def find_best_hand_with_consumable(self, hand, goal=None): #Need to finish

        consumables = []

        # Adds jokers that are related
        for joker in self.jokers:
            if joker["name"] in ["luchador"]:
                consumables.append(joker)

        # Adds consumables that are related
        for consumable in self.consumables:
            if not consumable in [""]:
                consumables.append(consumable)

        best_hand = []
        for i in range(consumables):
            for combo in combinations(hand, i):
                hand_result = self.find_hand_value(hand)
                if hand_result["value"] >= goal:
                    best_hand.append(hand_result)

        if len(best_hand) == 0:
            return False
        
        return best_hand.sort(key=lambda x: x["value"])[0]

    def find_best_discard(self, hand, goal=None):
        
        best_discard = {
            "value": 0,
            "hand": []
        }

        for i in len(hand):
            combos = combinations(hand, i)
            for combo in combos:
                hand = list(set(hand) - set(combo))
                new_cards = combinations(self.current_deck, len(combo))
                possablities = 0
                accumulative_value = 0
                for new_card in new_cards:
                    best_hand = self.find_best_hand(hand + new_card)
                    possablities += 1
                    accumulative_value += best_hand["value"]

                if accumulative_value / possablities >= best_discard["value"]:
                    best_discard = {
                        "value": accumulative_value / possablities,
                        "hand": combo
                    }
        
        return best_discard

    def find_hand_value(self, hand):
        print(hand)
        money = 0
        # Figures out hand type and active cards
        values = [0] * 15
        suits = [0] * 5
        for card in hand:
            card = self.identify_card(card)
            # print(card)
            values[card["value"]] += 1
            suits[card["suit"]] += 1
        
        # print(values)
        # print(suits)

        jokers = self.jokers
        for index, joker in enumerate(jokers):
            match joker["name"]:
                case "blueprint":
                    if index == len(jokers) - 1:
                        continue
                    joker = jokers[index + 1]
                    joker[index]["value"] = self.sheet.loc[self.sheet["name"] == joker["value"]]["value"]
                case "brainstorm":
                    if index == 0:
                        continue
                    joker = jokers[0]
                    joker[index]["value"] = self.sheet.loc[self.sheet["name"] == joker["value"]]["value"]
                case _:
                    pass

        disable_boss = False
        fingers = 5
        shortcut = False
        for joker in jokers:
            match joker["name"]:
                case "shortcut":
                    shortcut = True
                case "four_fingers":
                    fingers = 4
                case "smeared_joker":
                    for i in range(4):
                        suits[i + 1] += suits[4 - i]
                case "chicot":
                    disable_boss = True
                case _:
                    pass

        # Check if it's a flush at all
        straight = False
        for i in range(1, 11):
            if values[i] == 1 and values[i + 1] == 1 and values[i + 2] == 1 and values[i + 3] == 1 and (values[i + 4] == 1 or fingers == 4):
                straight = True
        if shortcut: # CHECK IF CURRENTLY HAVE SHORTCUT
            offset = 0
            for i in range(1, 11):
                offset = 0
                if not check:
                    for j in range(0, fingers):
                        check = True
                        if values[i + j + offset] == 1:
                            pass
                        elif values[i + j + offset + 1] == 1:
                            pass
                            offset += 1
                        else:
                            check = False

        flush = False
        if fingers in suits:
            flush = True

        # Check for flush five
        if flush and 5 in values:
            active_cards = hand
            hand_type = "flush_five"
            if fingers == 4:
                hand_type = value
        # Check for flush house
        elif flush and 3 in values and 2 in values:
            active_cards = hand
            hand_type = "flush_house"
            if fingers == 4:
                pass
        # Check for five of a kind
        elif 5 in values:
            active_cards = hand
            hand_type = "five_of_a_kind"
        # Check for straight flush
        elif flush:
            if straight:
                active_cards = hand
                hand_type = "straight_flush"
            if fingers == 4:
                pass
        # Check for four of a kind
            elif 4 in values:
                cards = []
                value = values.index(4)
                for card in hand:
                    if self.identify_card(card)["value"] == value:
                        cards.append(card)
                active_cards = cards
                hand_type = "four_of_a_kind"
        # Check for full house and flush
            else:
                active_cards = hand
                hand_type = "flush"
        elif 3 in values and 2 in values:
            active_cards = hand
            hand_type = "full_house"
        # Check for straight
        elif straight:
            active_cards = hand
            hand_type = "straight"
            if fingers == 4:
                pass
        # Check for three of a kind
        elif 3 in values:
            cards = []
            value = values.index(3)
            for card in hand:
                if self.identify_card(card)["value"] == value:
                    cards.append(card)
            active_cards = cards
            hand_type = "three_of_a_kind"
        # Check for two pair
        elif values.count(2) == 2:
            active_cards = hand
            for card in hand:
                if values[self.identify_card(card)["value"]] != 2:
                    active_cards.remove(card)
            hand_type = "two_pair"
        # Check for pair
        elif 2 in values:
            cards = []
            value = values.index(2)
            for card in hand:
                if self.identify_card(card)["value"] == value:
                    cards.append(card)
            active_cards = cards
            hand_type = "pair"
        # Check for high card
        else:
            high_card = hand[0]
            for card in hand:
                if self.identify_card(card)["value"] > self.identify_card(high_card)["value"]:
                    high_card = card
            active_cards = [high_card]
            hand_type = "high_card"

        for card in hand:
            if card[0] == "R":
                active_cards.append(card)

        # Calculates the value of the hand
        for type in self.hand_values:
            if type["name"] == hand_type:
                value = type["value"]
                multiplier = type["multiplier"]
        
        # print(hand)
        # print(active_cards)
        
        # Non-active cards in hand for joker purposes. TO-DO: Add the checks here
        non_active_cards = []
        non_active_hand = []

        # Joker logic here that are for pre scoring
        for joker in jokers:
            match joker["name"]:
                case "ride_the_bus":
                    joker["value"] += 1
                case "splash":
                    active_cards = hand
                    non_active_hand = []
                case "sixth_sense":
                    if len(hand) == 1:
                        if hand[0][1] == 6:
                            return 0 # Maybe want to change to just remove it from active
                case "seltzer" | "hanging_chad" | "hack" | "sock_and_buskin" | "mime" | "dusk":
                    joker["active"] = True
                case _:
                    pass
        
        if not disable_boss:
            match self.boss:
                case "the_psychic":
                    return 0
                case "the_mouth":
                    if self.played_hands == [] or not hand_type in self.played_hands:
                        return 0
                case "the_eye":
                    if hand_type in self.played_hands:
                        return 0
                case _:
                    pass

        # Scores the hand
        for index in range(len(active_cards)):

            face_card = False

            if card[1] == "J" or card[1] == "Q" or card[1] == "K":
                face_card = True
            for jokers in jokers:
                if joker["name"] == "pareidolia":
                    face_card = True

            # Debuff logic here (Bosses)
            if not disable_boss:
                match self.boss:
                    case "the_club":
                        if active_cards[index][0] == "C":
                            continue
                    case "the_goad":
                        if active_cards[index][0] == "S":
                            continue
                    case "the_window":
                        if active_cards[index][0] == "D":
                            continue
                    case "the_head":
                        if active_cards[index][0] == "H":
                            continue
                    case "the_plant":
                        if face_card:
                            continue
                    case _:
                        pass

            if card[2] == "D":
                continue

            card = active_cards[index]
            triggers = 1
            while triggers > 0:

                value += self.identify_card(card)["value"]
                if card[0] == "R": #Stone Card
                    value += 50

                try:
                    match card[2]: # Card Enchantments
                        case "B": #Bonus Card
                            value += 30
                        case "M": #Mult Card
                            multiplier += 4
                        case "G": #Glass Card
                            multiplier *= 2
                        case "F": #Steel Card (F for Fe)
                            multiplier *= 1.5
                except IndexError:
                    pass

                try:
                    match card[3]: # Card Editions
                        case "F": #Foil Card
                            value += 50
                        case "H": #Holographic Card
                            multiplier += 10
                        case "P": #Polychrome Card
                            multiplier *= 1.5
                except IndexError:
                    pass

                try:
                    match card[4]: # Card Seals
                        case "R":
                            triggers += 1
                except IndexError:
                    pass
                triggers -= 1

            # Joker logic here that are for "on played" jokers
            on_played_triggers = 1
            while on_played_triggers > 0:
                for joker in jokers:
                    match joker["name"]:
                        case "greedy_joker":
                            if card[0] == "D":
                                multiplier += 3
                        case "lustful_joker":
                            if card[0] == "H":
                                multiplier += 3
                        case "wrathful_joker":
                            if card[0] == "S":
                                multiplier += 3
                        case "gluttonous_joker":
                            if card[0] == "C":
                                multiplier += 3
                        case "mime":
                            if joker["active"]:
                                on_played_triggers += 1
                        case "dusk":
                            if joker["active"] and self.current_hands == 1:
                                on_played_triggers += 1
                        case "fibonacci":
                            if card[1] == "A" or card[1] == "2" or card[1] == "3" or card[1] == "5" or card[1] == "8":
                                multiplier += 8
                        case "scary_face":
                            if face_card:
                                value += 30
                        case "hack":
                            if card[1] == "2" or card[1] == "3" or card[1] == "4" or card[1] == "5":
                                if joker["active"]:
                                    on_played_triggers += 1
                        case "even_steven":
                            if self.identify_card(card)["value"] % 2 == 0:
                                multiplier += 4
                        case "odd_todd":
                            if self.identify_card(card)["value"] % 2 != 0:
                                value += 31
                        case "scholar":
                            if card[1] == "A":
                                value += 20
                                multiplier += 4
                        case "ride_the_bus":
                            if face_card:
                                joker["value"] == 0
                        case "photograph":
                            if not joker["value"]:
                                joker["value"] = True
                                multiplier *= 2
                        case "ancient_joker":
                            if card[0] == joker["suit"]:
                                multiplier *= 1.5
                        case "walkie_talkie":
                            if card[1] == 10 or card[1] == 4:
                                value += 10
                                multiplier += 4
                        case "seltzer":
                            if joker["active"]:
                                on_played_triggers += 1
                                joker["active"] = False
                        case "smiley_face":
                            if face_card:
                                multiplier += 5
                        case "sock_and_buskin":
                            if face_card and joker["active"]:
                                on_played_triggers += 1
                        case "hanging_chad":
                            if joker["active"]:
                                joker["active"] = False
                                on_played_triggers += 2 
                        case "bloodstone":
                            if card[0] == "H":
                                multiplier *= 1.25
                        case "arrowhead":
                            if card[0] == "S":
                                value += 50
                        case "onyx_agate":
                            if card[0] == "C":
                                multiplier += 7
                        case "wee_joker":
                            if card[1] == "2":
                                joker["value"] += 8
                        case "triboulet":
                            if card[1] == "K" or card[1] == "Q":
                                multiplier *= 2
                        case "buisness_card":
                            if face_card:
                                money += 1
                        case "reserved_parking":
                            if face_card:
                                money += 0.5
                        case "golden_ticket":
                            if card[2] == "G":
                                money += 4
                        case "rough_gem":
                            if card[0] == "D":
                                money += 1
                        case _:
                            pass

                on_played_triggers -= 1

        # Joker logic here that are for "on held" jokers
        for card in active_cards:
            for joker in jokers:
                match joker["name"]:
                    case "raised_fist":
                        lowest = 14
                        if len(non_active_cards) == 0:
                            continue
                        for card in non_active_cards:
                            if self.identify_card(card)["value"] < lowest:
                                lowest = self.identify_card(card)["value"]
                    case "baron":
                        for card in non_active_hand:
                            if card[0] == "H":
                                multiplier *= 1.5
                    case "shoot_the_moon":
                        for card in active_cards:
                            if card[1] == "Q":
                                multiplier += 13
                        for card in non_active_hand:
                            if card[1] == "Q":
                                multiplier += 13
                    case _:
                        pass

        # Joker logic here that are for "independent" jokers
        for joker in jokers:
            match joker["name"]:
                case "joker":
                    multiplier += 4
                case "jolly_joker":
                    if hand_type == "pair":
                        multiplier += 8
                case "zany_joker":
                    if hand_type == "three_of_a_kind":
                        multiplier += 12
                case "mad_joker":
                    if hand_type == "two_pair":
                        multiplier += 10
                case "crazy_joker":
                    if hand_type == "straight":
                        multiplier += 12
                case "droll_joker":
                    if hand_type == "flush":
                        multiplier += 10
                case "sly_joker":
                    if hand_type == "pair":
                        value += 50
                case "wily_joker":
                    if hand_type == "three_of_a_kind":
                        value += 100
                case "clever_joker":
                    if hand_type == "two_pair":
                        value += 80
                case "devious_joker":
                    if hand_type == "straight":
                        value += 100
                case "crafty_joker":
                    if hand_type == "flush":
                        value += 80
                case "half_joker":
                    if len(active_cards) >= 3:
                        multiplier += 20
                case "joker_stencil":
                    total = 1 # 1 is for the joker itself
                    for joker in jokers:
                        if joker["name"] == "joker_stencil":
                            total += 1
                    multiplier *= self.max_jokers - len(jokers) + total
                case "banner":
                    value += self.current_discards * 30
                case "mystic_summit":
                    if self.current_discards == 0:
                        multiplier += 15
                case "misprint":
                    multiplier += 11.5
                case "steel_joker":
                    mult = 0
                    for card in self.deck:
                        try:
                            if card[2] == "F":
                                mult += 1
                        except IndexError:
                            pass
                    multiplier *= mult + 1
                case "abstract_joker":
                    multiplier += 3 * len(jokers)
                case "gros_miichel":
                    multiplier += 15
                case "supernova":
                    multiplier += self.hand_values[self.hand_values.index(hand_type) + 1]["multiplier"]
                case "ceremonial_dagger" | "ride_the_bus" | "red_card" | "fortune_teller" | "flash_card" | "popcorn":
                    multiplier += joker["value"]
                case "runner":
                    if hand_type == "straight":
                        joker["value"] += 15
                    value += joker["value"]
                case "ice_cream":
                    joker["value"] -= 5
                    value += joker["value"]
                case "blue_joker":
                    value += 2 * len(self.current_deck)
                case "constellation":
                    multiplier *= 1 + joker["value"]
                case "green_joker":
                    multiplier += (self.hands - self.current_hands) - (self.discards - self.current_discards)
                case "cavendish":
                    multiplier *= 3
                case "square_joker":
                    if len(active_cards) + len(non_active_cards) == 4:
                        joker["value"] += 4
                    value += joker["value"]
                case "obelisk":
                    top_hand = {}
                    for hand_type in self.hand_values:
                        if hand_type["played"] > top_hand["played"]:
                            top_hand = hand_type
                    if top_hand["name"] == hand_type:
                        joker["value"] = 1
                    else:
                        joker["value"] += 0.2
                    multiplier *= joker["value"]
                case "erosion":
                    match self.deck:
                        case "abondoned_deck":
                            deck_difference = (40 - len(self.deck))
                        case "checkered_deck":
                            deck_difference = (26 - len(self.deck))
                        case _:
                            deck_difference = (52 - len(self.deck))
                    if deck_difference > 0:
                        multiplier += deck_difference * 4
                case "stone_joker":
                    for card in self.deck:
                        if card[0] == "R":
                            value += 25
                case "baseball_card":
                    for joker in jokers:
                        if joker["rarirty"] == "U":
                            multiplier *= 1.5
                case "bull":
                    value += 2 * self.money
                case "spare_trousers":
                    if hand_type == "pair":
                        joker["value"] += 2
                    multiplier += joker["value"]
                case "madness" | "ramen" | "campfire" | "throwback" | "glass_joker" | "lucky_cat" | "hologram" | "canio" | "yorick":
                    multiplier *= joker["value"]
                case "castle" | "wee_joker":
                    value += joker["value"]
                case "acrobat":
                    if self.current_hands == 1:
                        multiplier *= 3
                case "swashbuckler":
                    amount = 0
                    for joker in jokers:
                        amount += joker["sell_value"]
                    multiplier += amount
                case "flower_pot":
                    if joker["active"]:
                        multiplier *= 3
                case "hit_the_road":
                    amount = 1
                    for card in self.discarded:
                        if card[1] == "J":
                            amount += 1
                    multiplier *= amount
                case "the_duo":
                    if hand_type == "pair":
                        multiplier *= 2
                case "the_trio":
                    if hand_type == "three_of_a_kind":
                        multiplier *= 3
                case "the_family":
                    if hand_type == "four_of_a_kind":
                        multiplier *= 4
                case "the_order":
                    if hand_type == "straight":
                        multiplier *= 3
                case "the_tribe":
                    if hand_type == "flush":
                        multiplier *= 2
                case "stuntman":
                    value += 250
                case "driver's_license":
                    amount = 0
                    for card in self.deck:
                        try:
                            if card[2]:
                                amount += 1
                        except IndexError:
                            pass
                    if amount >= 16:
                        multiplier *= 3
                case "bootstraps":
                    multiplier += 2 * (self.money / 5)
                case "loyalty_card":
                    if joker["value"] == 0:
                        multiplier *= 4
                case "blackboard":
                    check = True
                    for card in active_cards["hand"] + non_active_cards["hand"]:
                        if card[0] != "C" and card[0] != "S" and card[0] != "M":
                            check = False
                    if check:
                        multiplier *= 3
                case "to_do_list":
                    if hand_type == joker["value"]:
                        money += 4
                case "vagabond":
                    if self.money <= 4:
                        money += 4
                case _:
                    pass

        # Applies bonuses from joker editions and types
        for joker in jokers:
            match joker['edition']:
                case "F":
                    value += 50
                case "H":
                    multiplier += 10
                case "P":
                    multiplier *= 1.5
        return {
            "value": value * multiplier,
            "hand": hand,
            "type": hand_type,
            "money": money
        }

    def pre_bind_logic(self, bind_data):
        
        self.current_discards = self.discards
        self.current_hands = self.discards
        self.played_hands = []

        match self.current_bind_type:
            case "small":
                self.current_bind_amount = bind_base_amount[self.current_bind]
            case "big":
                self.current_bind_amount = bind_base_amount[self.current_bind] * 1.5
            case "boss":
                match self.boss:
                    case "the_wall":
                        self.current_bind_amount = bind_base_amount[self.current_bind] * 4
                    case "the_needle":
                        self.current_bind_amount = bind_base_amount[self.current_bind]
                    case "violet_vessel":
                        self.current_bind_amount = bind_base_amount[self.current_bind] * 6
                    case _:
                        self.current_bind_amount = bind_base_amount[self.current_bind] * 2

        offset = 0
        for index, joker in enumerate(self.jokers):
            match joker["name"]:
                case "ceremonial_dagger":
                    if len(self.jokers > index - offset):
                        self.jokers[index - offset]["value"] += self.jokers[index + 1 - offset]["sell_value"]
                        self.jokers.pop(index + 1 - offset)
                        offset += 1
                case "marble_joker":
                    self.deck.append("RR")
                case "burglar":
                    self.current_discards = 0
                    self.current_hands += 3
                case "card_sharp":
                    self.jokers[index - offset]["value"] = 0
                case "madness":
                    if self.current_bind_type == "small" or self.current_bind_type == "big":
                        self.jokers[index - offset]["value"] += 0.5
                case "turtle_bean":
                    self.jokers[index - offset]["value"] -= 1
                    if self.jokers[index - offset]["value"] <= 0:
                        self.jokers.pop(index - offset)
                        offset += 1
                case _:
                    pass

        for index, voucher in enumerate(self.vouchers):
            match voucher:
                case "grabber" | "nacho_tong":
                    selfcurrent_hands += 1
                case "wasteful" | "recyclomancy":
                    self.current_discards += 1

        match self.boss:
            case "the_water":
                self.current_discards = 0
            case "the_needle":
                self.current_hands = 1
            case "the_manacle":
                self.current_hands -= 1
            case _:
                pass
            
    def pre_hand_logic(self, hand):
        
        for joker in self.jokers:
            match joker["name"]:
                case "juggler":
                    pass
                case _:
                    pass

    def post_hand_logic(self, hand, hand_type):
            
        for index, type in enumerate(self.hand_values):
            if type["name"] == hand_type:
                self.hand_values[index]["played"] += 1

        for joker in self.jokers:
            if joker["name"] == "pareidolia":
                face_card = True

        offset = 0
        for index, joker in enumerate(self.jokers):
            match joker["name"]:
                case "loyalty_card":
                    self.jokers[index- offset]["value"] -= 1
                    if self.jokers[index- offset]["value"] < 0:
                        self.jokers[index- offset]["value"] = 5
                case "ice_cream":
                    self.jokers[index]["value"] -= 5
                    if self.jokers[index - offset]["value"] <= 0:
                        self.jokers.pop(index- offset)
                        offset += 1
                case "vampire":
                    new_hand = []
                    for card in hand:
                        new_card = card
                        if card != new_card:
                            self.jokers[index]["value"] += 0.01
                        new_hand.append(new_card)
                    hand = new_hand
                case "midas_mask":
                    for card in hand:
                        if card[1] in ["J", "Q", "K"] or face_card:
                            hand.remove(card)
                            hand.append(card[:2] + "F" + card[3:])
                case "seltzer":
                    self.jokers[index]["value"] -= 1
                    if self.jokers[index]["value"] <= 0:
                        self.jokers.pop(index)
                        offset += 1
                case "spare_trousers":
                    if hand_type == "pair":
                        self.jokers[index]["value"] += 2
                case "golden_ticket":
                    for card in hand:
                        if card[2] == "G":
                            self.money += 4
                case _:
                    pass

        if self.boss == "the_arm":
            for hand_value in self.hand_values:
                if hand_value["name"] == hand_type and hand_value["level"] > 1:
                    hand_level -= 1
        elif self.boss == "the_tooth":
            self.money -= len(hand)

        self.discarded += hand      

    def post_bind_logic(self, bind_data):
        
        self.current_deck += self.discarded
    
        offset = 0
        for index, joker in enumerate(self.jokers):
            index -= offset
            match joker["name"]:
                case "delayed_gratification":
                    if self.current_discards == self.discards:
                        self.money += 2 * self.current_discards
                case "egg":
                    self.jokers[index]["sell_value"] += 3
                case "rocket":
                    self.money += self.jokers[index]["value"]
                    if bind_data["bind_type"] == "boss":
                        self.jokers[index]["value"] += 2
                case "cloud_9":
                    for card in self.current_deck:
                        if card[1] == "9":
                            self.money += 1
                case "popcorn":
                    self.jokers[index]["value"] -= 4
                    if self.jokers[index]["value"] <= 0:
                        self.jokers.pop(index)
                        offset += 1
                case "campfire":
                    if self.current_bind_type == "boss":
                        self.jokers[index]["value"] = 1
                case "satalite":
                    self.money += self.jokers[index]["value"]
                case _:
                    pass

        match self.current_bind_type:
            case "small":
                self.current_bind_type = "big"
            case "big":
                self.current_bind_type = "boss"
            case "boss":
                self.current_bind_type = "small"
                self.current_bind += 1

        self.discarded = []

    def handle_discard(self, discard_values, hand):

        self.discarded += discard_values

        for index, joker in enumerate(self.jokers):
            match joker["name"]:
                case "faceless_joker":
                    face_card = 0
                    for card in discard_values:
                        
                            
                        if card[1] == "J" or card[1] == "Q" or card[1] == "K":
                            face_card += 1
                case "main-in_rebate":
                    pass
                case "trading_card":
                    if len(discard_values) == 1 and self.discard_times == 0:
                        self.discarded.remove(discard_values[0])
                        self.money += 3
                case "ramen":
                    self.jokers[index]["value"] -= 0.01
                case "castle":
                    pass
                case "hit_the_road":
                    self.jokers[index]["value"] += 0.5
                case "burnt_joker":
                    if self.dicard_times == 0:
                        self.hand_type_upgrade(self.find_best_hand(hand)["type"])
                case "yorick":
                    self.jokers[index]["discards"] -= 1
                    if self.jokers[index]["discards"] <= 0:
                        self.jokers[index]["value"] += 1
                        self.jokers[index]["discards"] = 23
                case _:
                    pass

    def get_hands(self):
        self.current_hands = self.hands

        for joker in self.jokers:
            match joker["name"]:
                case "juggler":
                    self.current_hands += 1
                case "turtle_bean":
                    self.current_hands += joker["value"]
                case _:
                    pass
        
        return self.current_hands

    def get_discards(self):
        self.current_discards = self.discards

        for joker in self.jokers:
            match joker["name"]:
                case "drunkard":
                    self.current_discards += 1
                case _:
                    pass

    def aquire_joker(self, joker):
        self.jokers.append( {
            "name": joker,
            "value": self.sheet.loc[joker, "start_value"],
            "sell_value": self.sheet.loc[joker, "sell_value"]
        } )

    def get_shop_bonuses(self):
        bonuses = {
            "consumables": 2,
            "vouchers": 1,
        }

        for index, tag in self.tags:
            if tag["name"] == "voucher":
               if tag["active"] == True:
                    bonuses["vouchers"] += 1
                    self.tags[index]["active"] = False 
        
        if "overstock" in self.vouchers:
            bonuses["consumables"] += 1
            if "overstock_plus" in self.vouchers:
                bonuses["consumables"] += 1
    
        return bonuses

    def handle_bind(self, bind_data):
        hand = bind_data["hand"]
        current_score = bind_data["current_score"]
        bind_amount = self.current_bind_amount

        goal = bind_amount - current_score

        for joker in self.jokers:
            match joker["name"]:
                case "dna":
                    if self.played_hands == ["high_card"]:
                        hand.append(self.discarded[0])

        best_hand = self.find_best_hand(hand, goal)
        print(best_hand)
        if best_hand["value"] >= goal:
            return {
                "action": "play",
                "hand": best_hand["hand"],
                "consume": []
            }

        best_consumable_hand = self.find_best_hand_conusmable(hand, goal)
        if best_consumable_hand != False:
            if best_consumable_hand["value"] >= goal:
                for consumable in best_consumable_hand["consume"]:
                    if consumable in self.consumables:
                        self.consumables.remove(consumable)
                    if consumable in self.jokers:
                        self.sell_joker(consumable)
                return {
                    "action": "play",
                    "hand": best_consumable_hand["hand"],
                    "consume": best_consumable_hand["consume"]
                }

        if self.current_discards > 0:
            best_discard = self.find_best_discard(hand, goal)
            if best_discard["value"] > best_hand["value"]:
                return {
                    "action": "discard",
                    "hand": best_discard["hand"]
                }
            return {
                "action": "play",
                "hand": best_hand["hand"]
            }

        # If everything fails, then this means we lose or screwed up. This is the losing hand
        return {
            "action": "play",
            "hand": best_hand["hand"]
        }
        # Now check if the hand is a better option then the potential discards

    def find_value(self, item, type):
        try:
            value = self.sheet.loc[item, type]
        except KeyError:
            return 0

        if type == "cost" or type =="sell_value": # For voucher logic
            if "clearacne_sale" in self.vouchers:
                value *= 0.75
            if "liquidation" in self.vouchers:
                value *= 0.5
        
        return int(value)

    def handle_preference(self, select_item):
        
        self.favorite_hand = self.hand_values[11]
        for type in self.hand_values:
            if type["played"] > self.favorite_hand["played"]:
                self.favorite_hand = type

        check_items = ["base_worth", self.favorite_hand["name"], self.deck_type, self.stake]
        check_items += self.jokers + self.consumables + self.vouchers
        
        # Add most played card if certain hand types is most played
        if self.favorite_hand["name"] in ["flush_five", "five_of_a_kind", "four_of_a_kind", "three_of_a_kind", "pair"]:
            card_value = [] * 14
            for card in self.current_deck:
                card_value[self.identify_card(card)["value"]] += 1
            check_items.append(reversed(card_value).index(max(card_value)))
        
        # Add most played suit if certain hand types is most played
        if self.favorite_hand["name"] in ["flush_five", "flush_house", "flush"]:
            suit_value = [] * 5
            for card in self.current_deck:
                if "W" in card: # wild cards count for everything
                    continue
                suit_value[self.identify_card(card)["suit"]] += 1
            check_items.append(reversed(suit_value).index(max(suit_value)))

        select_item_worth = 0

        chip_worth = self.sheet.loc[select_item, "chip_worth"]
        mult_worth = self.sheet.loc[select_item, "mult_worth"]

        type = self.sheet.loc[select_item, "type"]

        # Find the value of all the items
        for item in check_items:
            value = self.sheet.loc[select_item, item]
            match value:
                case "Auto No":
                    return -99
                case "Auto Yes":
                    select_item_worth == 99
                    return select_item_worth
                case _:
                    select_item_worth += value

        # Change the weight of the item based on the type
        weight = 2
        if type.find("Muti*") != -1: # Checks if the item is a multiplier multiplier
            if 'muli_multiplier' in self.buying_preference:
                select_item_worth += weight
        if type.find("Mult+") != -1: # Checks if the item is a multiplier increaser
            if 'mult_increase' in self.buying_preference:
                select_item_worth += weight
        if type.find("Chip") != -1: # Checks if the item is a chip increaser
            if 'chip_increase' in self.buying_preference:
                select_item_worth += weight
        if type.find("Money") != -1: # Checks if the item is a money increaser
            if 'money_increase' in self.buying_preference:
                select_item_worth += weight


        return [select_item, select_item_worth]

    def handle_buy(self, options):
        # Sort the options into their respective categories
        jokers = []
        cards = []
        packs = []
        planets = []
        tarots = []
        vouchers = []
        preferences = []

        self.reroll_cost = 5

        for index, joker in enumerate(self.jokers):
            match joker["name"]:
                case "chaos_the_clown":
                    self.jokers[index]["active"] = True
                case _:
                    pass

        for option in options:
            preferences.append(self.handle_preference(option))
            match options[type]:
                case "joker":
                    jokers.append(option)
                case "card":
                    cards.append(option)
                case "pack":
                    packs.append(option)
                case "planet":
                    planets.append(option)
                case "tarot":
                    tarots.append(option)
                case "voucher":
                    vouchers.append(option)
                case _:
                    print("Unknown Option")
                    exit()
        
        for preference in preferences:
            if preference[1] > self.money:
                preferences.remove(preference)
            
        buying = []
        for preference in preferences:
            if preference[1] <= self.money:
                buying.append(preference[0])
                self.money -= preference[1]

        if buying == []:
            chaos_clown = False
            cost = self.reroll_cost
            for index, joker in enumerate(self.jokers):
                match joker["name"]:
                    case "chaos_the_clown":
                        chaos_clown = True
                        self.jokers[index]["active"] = False
                    case "flash_card":
                        self.jokers[index]["value"] += 2
                    case _:
                        pass

            if chaos_clown:
                return ["reroll"]
            if self.money / 2 >= cost:
                return ["reroll"]
        else:
            for item in buying:
                if item in jokers:
                    self.aquire_joker(item)
                if item in cards:
                    self.deck.append(item)
                    for index, joker in enumerate(self.jokers):
                        match joker["name"]:
                            case "hologram":
                                self.jokers[index]["value"] += 0.25
                            case _:
                                pass
                if item in packs:
                    self.current_deck += self.sheet.loc[item, "pack"]
                if item in planets:
                    self.current_deck += self.sheet.loc[item, "planet"]
                    for index, joker in enumerate(self.jokers):
                        match joker["name"]:
                            case "constellation":
                                self.jokers[index]["value"] += 0.1
                            case _:
                                pass
                if item in tarots:
                    self.current_deck += self.sheet.loc[item, "tarot"]
                if item in vouchers:
                    self.vouchers.append(item)
        return buying

    def handle_pack(self, pack_info):
        options = pack_info["options"]
        type = pack_info["type"]
        card_choices = pack_info["cards"]
        valued_options = []
        for option in options:
            valued_options.append(self.handle_preference(option))

        match type:
            case "spectral":
                valued_options, card_choices = self.select_spectral(valued_options, card_choices)
            case "tarot":
                valued_options, card_choices = self.select_tarot(valued_options, card_choices)
            case _:
                pass

        valued_options = valued_options.sort(key=lambda x: x[1], reverse=True)

        for option in valued_options:
            if option[1] <= 1:
                valued_options.remove(option)

        if valued_options == []:    # If no options worth choseing/we are skipping
            for index, joker in enumerate(self.jokers):
                match joker["name"]:
                    case "red_card":
                        self.jokers[index]["value"] += 3

        return valued_options

    def select_spectral(self, options, card_choices):
        card_choices = []
        card_select_options = []

        values = [] * 14
        suits = [] * 5
        for card in self.current_deck:
            values[self.identify_card(card)["value"]] += 1
            suits[self.identify_card(card)["suit"]] += 1

        open_seal_cards = 0
        for card in card_choices:
            try:
                if card[3] == "N":
                    open_seal_cards += 1
            except IndexError:
                open_seal_cards += 1

        open_edition_cards = 0
        for card in card_choices:
            try:
                if card[4] == "N":
                    open_edition_cards += 1
            except IndexError:
                open_edition_cards +=

        def get_pack_options(index_check, amount):
            options = []
            for card in card_choices:
                try:
                    card[index_check] == "N"
                    continue
                except IndexError:
                    pass
                if values.index(values.max()) > 6:
                    options.append(card)
                elif suits.index(suits.max()) > 15:
                    options.append(card)
                else:
                    card_target = "C2"
                    for card in card_choices:
                        if self.identify_card(card)["value"] > self.identify_card(card_target)["value"]:
                            card_target = card
                    options.append(card_target)
            options.sort(key=lambda x: self.identify_card(x)["value"], reverse=True)
            return options[:amount]

        for option in options:
            match option:
                case "familiar": # Removes if too many in non-royal cards
                    if values.max() > 10 and (not values[13] > 10 or not values[12] > 10 or not values[11] > 10):
                        options.remove(option)
                case "grim": # Removes if too many that aren't aces
                    if values.max() > 6 and not values[0] > 6:
                        options.remove(option)
                case "incantation": # Removes if too many cards in a single rank
                    if values.max() > 10:
                        options.remove(option)
                case "talisman":
                    if open_seal_cards == 0:
                        options.remove(option)
                        continue

                    card_select_options.append(["talisman", get_pack_options(3, 1)])
                case "aura":
                    if open_edition_cards == 0:
                        options.remove(option)
                        continue
                    
                    card_select_options.append(["aura", get_pack_options(4, 1)])
                case "wraith":
                    if self.money > 7 or len(self.jokers) >= self.max_jokers:
                        options.remove(option)
                case "sigil":
                    if suits.max() > 15:
                        options.remove(option)
                case "ouija":
                    if values.max() > 6:
                        options.remove(option)
                case "ectoplasm":
                    if self.jokers == [] or self.get_hands() <= 2:
                        options.remove(option)
                case "immolate":
                    pass
                case "ankh":
                    if self.max_jokers - len(self.jokers) <= 2:
                        options.remove(option)
                case "deja_vu":
                    if open_seal_cards == 0:
                        options.remove(option)
                        continue

                    card_select_options.append(["deja_vu", get_pack_options(3, 1)])
                case "hex":
                    if len(self.jokers) <= 2:
                        options.remove(option)
                case "trance":
                    if open_seal_cards == 0:
                        options.remove(option)
                        continue

                    card_select_options.append(["trance", get_pack_options(3, 1)])
                case "medium":
                    if open_seal_cards == 0:
                        options.remove(option)
                        continue

                    card_select_options.append(["medium", get_pack_options(3, 1)])
                case "cryptid":
                    pass
                case "soul":
                    pass
                case "black_hole":
                    pass

        return options, card_select_options

    def select_tarot(self, options, card_choices):
        card_choices = []

        suits = [] * 5
        values = [] * 14
        for card in self.current_deck:
            suits[self.identify_card(card)["suit"]] += 1
            values[self.identify_card(card)["value"]] += 1

        open_enhanched_cards = 0
        for card in card_choices:
            try:
                if card[2] == "N":
                    open_enhanched_cards += 1
            except IndexError:
                open_enhanched_cards += 1

        def get_pack_options(index_check, amount):
            options = []
            for card in card_choices:
                try:
                    card[index_check] == "N"
                    continue
                except IndexError:
                    pass
                if values.index(values.max()) > 6:
                    options.append(card)
                elif suits.index(suits.max()) > 15:
                    options.append(card)
                else:
                    card_target = "C2"
                    for card in card_choices:
                        if self.identify_card(card)["value"] > self.identify_card(card_target)["value"]:
                            card_target = card
                    options.append(card_target)
            options.sort(key=lambda x: self.identify_card(x)["value"], reverse=True)
            return options[:amount]

        for option in options:
            match option:
                case "the_fool":
                    pass
                case "the_magician" | "the_empress" | "the_hierophant" | "the_lovers" | "the_chariot" | "justice":
                    if open_enhanched_cards <= 2:
                        options.remove(option)
                case "the_high_priestess" | "the_emperor":
                    if len(self.consumables) >= self.max_consumables - 1:
                        options.remove(option)
                case "the_hermit":
                    if self.money <= 5:
                        options.remove(option)
                case "wheel_of_fortune":
                    if len(self.jokers) < 0:
                        options.remove(option)
                case "strength":
                    best_rank = suits.index(suits.max())
                    strength_options = []
                    for card in card_choices:
                        if self.identify_card(card)["suit"] == best_rank - 1:
                            strength_options.append(card)
                    if strength_options == []:
                        options.remove(option)
                case "the_hanged_man":
                    pass
                case "death":
                    pass
                case "temperance":
                    sell_value = 0
                    for joker in self.jokers:
                        sell_value += joker["sell_value"]
                    if sell_value <= 10:
                        options.remove(option)
                case "the_devil":
                    if open_enhanched_cards < 1:
                        options.remove(option)
                case "the_tower":
                    pass
                case "the_star": # Diamonds
                    if not suits.max() > 13 or suits[2] < 13:
                        options.remove(option)
                case "the_moon": # Clubs
                    if not suits.max() > 13 or suits[1] < 13:
                        options.remove(option)
                case "the_sun": # Hearts
                    if not suits.max() > 13 or suits[3] < 13:
                        options.remove(option)
                case "judgement":
                    if len(self.jokers) >= self.max_jokers:
                        options.remove(option)
                case "the_world": # Spades
                    if not suits.max() > 13 or suits[4] < 13:
                        options.remove(option)

        return options, card_choices

    def skip_blind(self, tag):
        match tag:
            case "uncommon":
                return False
            case "rare":
                return False
            case "negative":
                return True
            case "foil":
                return False
            case "holographic":
                return False
            case "polychrome":
                return False
            case "investment":
                return False
            case "voucher":
                return False
            case "boss":
                return False
            case "standard":
                return False
            case "charm":
                return False
            case "meteor":
                return False
            case "buffoon":
                return False
            case "handy":
                return False
            case "garbage":
                return True
            case "ethereal":
                return False
            case "coupon":
                return False
            case "double":
                return False
            case "jungle":
                return False
            case "d6":
                return False
            case "top-up":
                return False
            case "speed":
                return False
            case "oribital":
                return False
            case "economy":
                return False


if __name__ == "__main__":
    algo = Algorithm("red_deck", "red_stake", None)
    print(algo.find_best_hand(["CA", "C5", "D3", "D3", "H3", "H3", "S3", "S3"]))