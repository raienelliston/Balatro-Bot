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

bind_base_amount = [300]

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
        self.deck = deck
        self.current_bind = 1
        self.current_bind_type = "small"
        self.current_bind_amount = 300
        self.stake = stake_list.index(stake)
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
    
    def find_best_hand(self, hand, goal=None):
        value = 0
        multiplier = 1
        best_hand = {
            "value": 0,
            "hand": []
        }
        print(hand)

        # Setup Joker Logic, mainly for copyers
        jokers = self.jokers
        joker_names = []
        sorted_jokers = jokers.sort()

        for joker in jokers:
            joker_names.append(joker['name'])

        self.joker_counter = Counter(jokers)

        # Calculate the value of every hand
        for index1 in range(len(hand)):
            card1 = hand[index1]
            for index2 in range(index1 + 1, len(hand)):
                card2 = hand[index2]
                for index3 in range(index2 + 1, len(hand)):
                    card3 = hand[index3]
                    for index4 in range(index3 + 1, len(hand)):
                        card4 = hand[index4]
                        for index5 in range(index4 + 1, len(hand)):
                            card5 = hand[index5]
                            hand_check = [card1, card2, card3, card4, card5]
                            hand_value = self.find_hand_value(hand_check)
                            if hand_value > best_hand["value"]:
                                best_hand["value"] = hand_value
                                best_hand["hand"] = hand_check
                        hand_check = [card1, card2, card3, card4]
                        hand_value = self.find_hand_value(hand_check)
                        if hand_value > best_hand["value"]:
                            best_hand["value"] = hand_value
                            best_hand["hand"] = hand_check
                    hand_check = [card1, card2, card3]
                    hand_value = self.find_hand_value(hand_check)
                    if hand_value > best_hand["value"]:
                        best_hand["value"] = hand_value
                        best_hand["hand"] = hand_check
                hand_check = [card1, card2]
                hand_value = self.find_hand_value(hand_check)
                if hand_value > best_hand["value"]:
                    best_hand["value"] = hand_value
                    best_hand["hand"] = hand_check
            hand_check = [card1]
            hand_value = self.find_hand_value(hand_check)
            if hand_value > best_hand["value"]:
                best_hand["value"] = hand_value
                best_hand["hand"] = hand_check


        for r in range(1, 6):
            for hand in combinations(hand, r):
                print(hand)
                hand_value = self.find_hand_value(hand)
                if hand_value > best_hand["value"]:
                    best_hand["value"] = hand_value
                    best_hand["hand"] = hand
                
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

    def find_best_discard(self, hand, goal=None):
        discard = []
        for index, card in enumerate(hand):
            pass

    def find_hand_value(self, hand):
        print(hand)
        money = 0
        # Figures out hand type and active cards
        values = [0] * 14
        suits = [0] * 5
        for card in hand:
            card = self.identify_card(card)
            # print(card)
            values[card["value"]] += 1
            suits[card["suit"]] += 1
        
        # print(values)
        # print(suits)

        shortcut = False
        for joker in self.jokers:
            if joker["name"] == "shortcut":
                shortcut = True

        # Check if it's a flush at all
        straight = False
        for i in range(1, 10):
            if values[i] == 1 and values[i + 1] == 1 and values[i + 2] == 1 and values[i + 3] == 1 and values[i + 4] == 1:
                straight = True
        if shortcut: # CHECK IF CURRENTLY HAVE SHORTCUT
            offset = 0
            for i in range(1, 10):
                offset = 0
                if not check:
                    for j in range(0, 5):
                        check = True
                        if values[i + j + offset] == 1:
                            pass
                        elif values[i + j + offset + 1] == 1:
                            pass
                            offset += 1
                        else:
                            check = False

        flush = False
        if 5 in suits:
            flush = True

        # Check for flush five
        if flush and 5 in values:
            active_cards = hand
            hand_type = "flush_five"
        # Check for flush house
        elif flush and 3 in values and 2 in values:
            active_cards = hand
            hand_type = "flush_house"
        # Check for five of a kind
        elif 5 in values:
            active_cards = hand
            hand_type = "five_of_a_kind"
        # Check for straight flush
        elif flush:
            if straight:
                active_cards = hand
                hand_type = "straight_flush"
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
        for joker in self.jokers:
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
            for jokers in self.jokers:
                if joker["name"] == "pareidolia":
                    face_card = True

            # Debuff logic here (Bosses)
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
                for joker in self.jokers:
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
                        case _:
                            pass

                on_played_triggers -= 1

        # Joker logic here that are for "on held" jokers
        for card in active_cards:
            for joker in self.jokers:
                match joker["name"]:
                    case "raised_fist":
                        pass
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
        for joker in self.jokers:
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
                    multiplier *= (self.max_jokers - len(self.jokers) + 1)
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
                    multiplier += 3 * len(self.jokers)
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
                    for joker in self.jokers:
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
                    for joker in self.jokers:
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
                case _:
                    pass
            
            
                    
            
            

        # # Applies bonuses from joker editions and types
        # for joker in self.jokers:
        #     match joker['edition']:
        #         case "F":
        #             value += 50
        #         case "H":
        #             multiplier += 10
        #         case "P":
        #             multiplier *= 1.5
                

        return value * multiplier

    def pre_bind_logic(self, bind_data):
        
        self.current_discards = bind_data["current_discards"]
        self.current_hands = bind_data["current_hands"]
        self.boss = bind_data["boss"]
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
                    self.jokers[index - offset]["value"] += 0.5
                case "turtle_bean":
                    self.jokers[index - offset]["value"] -= 1
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
            
        self.played_hands.append(hand_type)

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
                case _:
                    pass

        if self.boss == "the_arm":
            for hand_value in self.hand_values:
                if hand_value["name"] == hand_type and hand_value["level"] > 1:
                    hand_level -= 1
        elif self.boss == "the_tooth":
            self.money -= len(hand)

    def post_bind_logic(self, bind_data):
        
        for index, joker in enumerate(self.jokers):
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

    def handle_discard(self, discard_values, hand):

        for joker in self.jokers:
            match joker["name"]:
                case "faceless_joker":
                    pass
                case _:
                    pass

    def get_hands(self):
        self.current_hands = self.hands

        for joker in self.jokers:
            match joker["name"]:
                case "juggler":
                    self.current_hands += 1
                case _:
                    pass

    def get_discards(self):
        self.current_discards = self.discards

        for joker in self.jokers:
            match joker["name"]:
                case "drunkard":
                    self.current_discards += 1
                case _:
                    pass

    def aquire_joker(self, joker):
        match joker:
            case "turtle_bean":
                self.jokers.append({"name": joker, "value": 5, "sell_value": 3})

    def handle_bind(self, bind_data):
        current_score = bind_data["current_score"]
        bind_amount = self.current_bind_amount

        goal = bind_amount - current_score

        best_hand = self.find_best_hand(bind_data["hand"], goal)
        print(best_hand)
        if best_hand["value"] >= goal:
            return {
                "action": "play",
                "hand": best_hand["hand"]
            }
        
        return {
            "action": "play",
            "hand": best_hand["hand"]
        }
        # Now check if the hand is a better option then the potential discards

    def handle_buy(self, options):
        jokers = []
        cards = []
        packs = []
        planets = []
        tarots = []
        for option in options:
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
                case _:
                    print("Unknown Option")
                    exit()
        
        

if __name__ == "__main__":
    algo = Algorithm("red_deck", "red_stake", None)
    print(algo.find_best_hand(["CA", "C5", "D3", "D3", "H3", "H3", "S3", "S3"]))