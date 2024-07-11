

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
        if stake >= 5:
            self.discards -= 1

    def identify_card(self, id):
        card = {}
        match id[0]:
            case "C":
                card["suit"] = "clubs"
            case "D":
                card["suit"] = "diamonds"
            case "H":
                card["suit"] = "hearts"
            case "S":
                card["suit"] = "spades"
            case "R":
                card["suit"] = "rock"
            case "W":
                card["suit"] = "wild"
        
        match id[1]:
            case "R":
                card["value"] = None
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
    
    def find_best_hand(self, hand):
        value = 0
        multiplier = 1
        best_hand = {}

        # Calculate the value of every hand
        for card1 in hand:
            for card2 in hand.splice(hand.index(card1), 1):
                for card3 in hand.splice(hand.index(card2), 1):
                    for card4 in hand.splice(hand.index(card3), 1):
                        for card5 in hand.splice(hand.index(card4), 1):
                            hand_value = self.hand_value([card1, card2, card3, card4, card5])
                            if hand_value["value"] > value:
                                value = hand_value["value"]
                                best_hand = hand_value

def find_hand_value(self, hand):
    pass