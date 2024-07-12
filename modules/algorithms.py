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

class Algorithm:
    def __init__(self, deck, stake, controller):
        self.controller = controller
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
    
    # Iterates through
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


        # for r in range(1, 6):
        #     for hand in combinations(hand, r):
        #         print(hand)
        #         # hand_value = self.find_hand_value(hand)
        #         # if hand_value > best_hand["value"]:
        #         #     best_hand["value"] = hand_value
                #     best_hand["hand"] = hand

        hand_numbers = []
        for card in hand:
            if card in best_hand["hand"]:
                index = best_hand["hand"].index(card)
                hand_numbers.append(hand.index(card))
                best_hand["hand"].pop(index)
        
        return {
            "hand": hand_numbers,
            "value": best_hand["value"]
        }

    def find_hand_value(self, hand):
        # print(hand)
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

        # Check if it's a flush at all
        straight = False
        for i in range(1, 10):
            if values[i] == 1 and values[i + 1] == 1 and values[i + 2] == 1 and values[i + 3] == 1 and values[i + 4] == 1:
                straight = True
        if False: # CHECK IF CURRENTLY HAVE SHORTCUT
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
                active_cards = hand
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
            active_cards = hand
            hand_type = "three_of_a_kind"
        # Check for two pair
        elif values.count(2) == 2:
            active_cards = hand
            hand_type = "two_pair"
        # Check for pair
        elif 2 in values:
            for card in hand:
                hand.remove(hand[0])
                # print(str(hand) + " " + str(card))
                for card2 in hand:
                    if self.identify_card(card)["value"] == self.identify_card(card2)["value"]:
                        active_cards = [card, card2]
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
            if joker["name"] == "ride_the_bus":
                joker["value"] += 1
            elif joker["name"] == "splash":
                active_cards = hand
                non_active_hand = []
            elif joker["name"] == "sixth_sense":
                if len(hand) == 1:
                    if hand[0][1] == 6:
                        return 0 # Maybe want to change to just remove it from active
            elif joker["name"] == "seltzer" or joker["name"] == "hack" or joker["sock_and_buskin"] or joker["name"] == "mime" or joker["name"] == "dusk" or joker["name"] == "hanging_chad":
                joker["active"] = True

        # Scores the hand
        for index in range(len(active_cards)):
            card = active_cards[index]
            triggers = 1
            while triggers > 0:
                # Initial value added
                # print("card = " + str(card))
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

            face_card = False

            if card[1] == "J" or card[1] == "Q" or card[1] == "K":
                face_card = True
            # Add if pareidolia joker, face value == true

            # Joker logic here that are for "on played" jokers
            on_played_triggers = 1
            while on_played_triggers > 0:
                for joker in self.jokers:
                    if joker["name"] == "greedy_joker":
                        if card[0] == "D":
                            multiplier += 3
                    elif joker["name"] == "lustful_joker":
                        if card[0] == "H":
                            multiplier += 3
                    elif joker["name"] == "wrathful_joker":
                        if card[0] == "S":
                            multiplier += 3
                    elif joker["name"] == "gluttonous_joker":
                        if card[0] == "C":
                            multiplier += 3
                    elif joker["name"] == "mime":
                        if joker["active"]:
                            on_played_triggers += 1
                    elif joker["name"] == "dusk":
                        if joker["active"]:
                            on_played_triggers += 1
                    elif joker["name"] == "fibonacci":
                        if card[1] == "A" or card[1] == "2" or card[1] == "3" or card[1] == "5" or card[1] == "8":
                            multiplier += 8
                    elif joker["name"] == "scary_face":
                        if face_card:
                            value += 30
                    elif joker["name"] == "hack":
                        if card[1] == "2" or card[1] == "3" or card[1] == "4" or card[1] == "5":
                            if joker["active"]:
                                on_played_triggers += 1
                    elif joker["name"] == "even_steven":
                        if self.identify_card(card)["value"] % 2 == 0:
                            multiplier += 4
                    elif joker["name"] == "odd_todd":
                        if self.identify_card(card)["value"] % 2 != 0:
                            value += 31
                    elif joker["name"] == "scholar":
                        if card[1] == "A":
                            value += 20
                            multiplier += 4
                    elif joker["name"] == "ride_the_bus":
                        if face_card:
                            joker["value"] == 0
                    elif joker["name"] == "photograph":
                        if not joker["value"]:
                            joker["value"] = True
                            multiplier *= 2
                    elif joker["name"] == "ancient_joker":
                        if card[0] == joker["suit"]:
                            multiplier *= 1.5
                    elif joker["name"] == "walkie_talkie":
                        if card[1] == 10 or card[1] == 4:
                            value += 10
                            multiplier += 4
                    elif joker["name"] == "seltzer":
                        if joker["active"]:
                            on_played_triggers += 1
                            joker["active"] = False
                    elif joker["name"] == "smiley_face":
                        if face_card:
                            multiplier += 5
                    elif joker["name"] == "sock_and_buskin":
                        if face_card and joker["active"]:
                            on_played_triggers += 1
                    elif joker["name"] == "hanging_chad":
                        if joker["active"]:
                            joker["active"] = False
                            on_played_triggers += 2 
                    elif joker["name"] == "bloodstone":
                        if card[0] == "H":
                            multiplier *= 1.25
                    elif joker["name"] == "arrowhead":
                        if card[0] == "S":
                            value += 50
                    elif joker["name"] == "onyx_agate":
                        if card[0] == "C":
                            multiplier += 7
                    elif joker["name"] == "wee_joker":
                        if card[1] == "2":
                            joker["value"] += 8
                    elif joker["name"] == "triboulet":
                        if card[1] == "K" or card[1] == "Q":
                            multiplier *= 2

                on_played_triggers -= 1

        # Joker logic here that are for "on held" jokers
        for card in active_cards:
            for joker in self.jokers:
                if joker["name"] == "raised_fist":
                    pass
                elif joker["name"] == "baron":
                    for card in non_active_hand:
                        if card[0] == "H":
                            multiplier *= 1.5
                elif joker["name"] == "shoot_the_moon":
                    for card in active_cards:
                        if card[1] == "Q":
                            multiplier += 13
                    for card in non_active_hand:
                        if card[1] == "Q":
                            multiplier += 13

        # Joker logic here that are for "independent" jokers
        for joker in self.jokers:
            if joker["name"] == "joker":
                multiplier += 4
            elif joker["name"] == "jolly_joker":
                if hand_type == "pair":
                    multiplier += 8
            elif joker["name"] == "zany_joker":
                if hand_type == "three_of_a_kind":
                    multiplier += 12
            elif joker["name"] == "mad_joker":
                if hand_type == "two_pair":
                    multiplier += 10
            elif joker["name"] == "crazy_joker":
                if hand_type == "straight":
                    multiplier += 12
            elif joker["name"] == "droll_joker":
                if hand_type == "flush":
                    multiplier += 10
            elif joker["name"] == "sly_joker":
                if hand_type == "pair":
                    value += 50
            elif joker["name"] == "wily_joker":
                if hand_type == "three_of_a_kind":
                    value += 100
            elif joker["name"] == "clever_joker":
                if hand_type == "two_pair":
                    value += 80
            elif joker["name"] == "devious_joker":
                if hand_type == "straight":
                    value += 100
            elif joker["name"] == "crafty_joker":
                if hand_type == "flush":
                    value += 80
            elif joker["name"] == "half_joker":
                if len(active_cards) >= 3:
                    multiplier += 20
            elif joker["name"] == "joker_stencil":
                multiplier *= (self.max_jokers - len(self.jokers) + 1)
            elif joker["name"] == "ceremonial_dagger":
                multiplier += joker["value"]
            elif joker["name"] == "banner":
                value += self.current_discards * 30
            elif joker["name"] == "mystic_summit":
                if self.current_discards == 0:
                    multiplier += 15
            elif joker["name"] == "misprint":
                multiplier += 11.5
            elif joker["name"] == "steel_joker":
                mult = 0
                for card in self.deck:
                    try:
                        if card[2] == "F":
                            mult += 1
                    except IndexError:
                        pass
                multiplier *= mult + 1
            elif joker["name"] == "abstract_joker":
                multiplier += 3 * len(self.jokers)
            elif joker["name"] == "gros_miichel":
                multiplier += 15
            elif joker["name"] == "supernova":
                multiplier += self.hand_values[self.hand_values.index(hand_type) + 1]["multiplier"]
            elif joker["name"] == "ride_the_bus":
                multiplier += joker["value"]
            elif joker["name"] == "runner":
                if hand_type == "straight":
                    joker["value"] += 15
                value += joker["value"]
            elif joker["name"] == "ice_cream":
                joker["value"] -= 5
                value += joker["value"]
            elif joker["name"] == "blue_joker":
                value += 2 * len(self.current_deck)
            elif joker["name"] == "constellation":
                multiplier *= 1 + joker["value"]
            elif joker["name"] == "green_joker":
                multiplier += (self.hands - self.current_hands) - (self.discards - self.current_discards)
            elif joker["name"] == "cavendish":
                multiplier *= 3
            elif joker["name"] == "red_card":
                multiplier += joker["value"]
            elif joker["name"] == "madness":
                multiplier *= joker["value"]
            elif joker["name"] == "square_joker":
                if len(active_cards) + len(non_active_cards) == 4:
                    joker["value"] += 4
                value += joker["value"]
            elif joker["name"] == "hologram":
                multiplier *= joker["value"]
            elif joker["name"] == "obelisk":
                top_hand = {}
                for hand_type in self.hand_values:
                    if hand_type["played"] > top_hand["played"]:
                        top_hand = hand_type
                if top_hand["name"] == hand_type:
                    joker["value"] = 1
                else:
                    joker["value"] += 0.2
                multiplier *= joker["value"]
            elif joker["name"] == "erosion":
                match self.deck:
                    case "abondoned_deck":
                        deck_difference = (40 - len(self.deck))
                    case "checkered_deck":
                        deck_difference = (26 - len(self.deck))
                    case _:
                        deck_difference = (52 - len(self.deck))
                if deck_difference > 0:
                    multiplier += deck_difference * 4
            elif joker["name"] == "fortune_teller":
                multiplier += joker["value"]
            elif joker["name"] == "stone_joker":
                for card in self.deck:
                    if card[0] == "R":
                        value += 25
            elif joker["name"] == "lucky_cat":
                multiplier *= joker["value"]
            elif joker["name"] == "baseball_card":
                for joker in self.jokers:
                    if joker["rarirty"] == "U":
                        multiplier *= 1.5
            elif joker["name"] == "bull":
                value += 2 * self.money
            elif joker["name"] == "flash_card":
                multiplier += joker["value"]
            elif joker["name"] == "popcorn":
                multiplier += joker["value"]
            elif joker["name"] == "spare_trousers":
                if hand_type == "pair":
                    joker["value"] += 2
                multiplier += joker["value"]
            elif joker["name"] == "ramen":
                multiplier *= joker["value"]
            elif joker["name"] == "castle":
                value += joker["value"]
            elif joker["name"] == "campfire":
                multiplier *= joker["value"]
            elif joker["name"] == "acrobat":
                if self.current_hands == 1:
                    multiplier *= 3
            elif joker["name"] == "swashbuckler":
                amount = 0
                for joker in self.jokers:
                    amount += joker["sell_value"]
                multiplier += amount
            elif joker["name"] == "throwback":
                multiplier *= joker["value"]
            elif joker["name"] == "glass_joker":
                multiplier *= joker["value"] 
            elif joker["name"] == "flower_pot":
                if joker["active"]:
                    multiplier *= 3
            elif joker["name"] == "wee_joker":
                value += joker["value"]
            elif joker["name"] == "hit_the_road":
                amount = 1
                for card in self.discarded:
                    if card[1] == "J":
                        amount += 1
                multiplier *= amount
            elif joker["name"] == "the_duo":
                if hand_type == "pair":
                    multiplier *= 2
            elif joker["name"] == "the_trio":
                if hand_type == "three_of_a_kind":
                    multiplier *= 3
            elif joker["name"] == "the_family":
                if hand_type == "four_of_a_kind":
                    multiplier *= 4
            elif joker["name"] == "the_order":
                if hand_type == "straight":
                    multiplier *= 3
            elif joker["name"] == "the_tribe":
                if hand_type == "flush":
                    multiplier *= 2
            elif joker["name"] == "stuntman":
                value += 250
            elif joker["name"] == "driver's_license":
                amount = 0
                for card in self.deck:
                    try:
                        if card[2]:
                            amount += 1
                    except IndexError:
                        pass
                if amount >= 16:
                    multiplier *= 3
            elif joker["name"] == "bootstraps":
                multiplier += 2 * (self.money / 5)
            elif joker["name"] == "canio":
                multiplier *= joker["value"]
            elif joker["name"] == "yorick":
                multiplier *= joker["value"]
            
            
                    
            
            

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

    def handle_bind(self, bind_data):
        current_score = bind_data["current_score"]
        bind_amount = bind_data["bind_amount"]

        goal = bind_amount - current_score

        best_hand = self.find_best_hand(self.current_deck, goal)

        if best_hand["value"] >= goal:
            return {
                "action": "play",
                "hand": best_hand["hand"]
            }
        
        # Now check if the hand is a better option then the potential discards






if __name__ == "__main__":
    algo = Algorithm("red_deck", "red_stake", None)
    print(algo.find_best_hand(["CA", "C5", "D3", "D3", "H3", "H3", "S3", "S3"]))