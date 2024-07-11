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
        self.discarded = []
        self.money = 4
        self.hands = 4
        self.hand_size = 8
        self.discards = 4
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
    def find_best_hand(self, hand):
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

        return best_hand

    def find_hand_value(self, hand):
        print(hand)
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

            # Joker value logic here
            for i in self.joker_counter['joker']:
                value += 10
                multiplier += 1

        # Applies bonuses from joker editions and types
        for joker in self.jokers:
            match joker['edition']:
                case "F":
                    value += 50
                case "H":
                    multiplier += 10
                case "P":
                    multiplier *= 1.5
                

        return value * multiplier



if __name__ == "__main__":
    algo = Algorithm("red_deck", "red_stake", None)
    print(algo.find_best_hand(["CA", "C5", "D3", "D3", "H3", "H3", "S3", "S3"]))