# Balatro-Bot
A bot/script that's designed to beat the card gambling roguelike game by Playstick Games, Balatro. The purpose of creating this is to have a main project for me to learn more algorithms, have something to attempt to make more efficient, and be a specific project that showcases my programming skills. Written all in Python and gaining information on the game using OpenGL and Tesseract, it requires no connection to the game itself for it to know what's on the screen.

## Features
- Able to identify the Balatro window by itself and set it up, along with starting a new run and essentially starting playing the game.
- Can identify all cards, jokers, booster packs, and other things in the game without needing to access the program memory.
- Plays the game, using almost all aspects of the game, including using items, buying stuff from the shop, and using discards.
- Takes preferences with specific cards and other things using weighted relations taken from a CSV file.

## How to install/use

1. Install Balatro from anywhere and Tesseract.
2. Clone the repo ```git clone https://www.github.com/raienelliston/Balatro-Bot.git```
3. Add your settings in the config.txt
4. Run the commands below

```
pip install -r requirements.txt
python main.py
```

## Seeds
You can find seeds for Balatro from [here](https://balatroseeds.com/).

### Notable Seeds
None at the moment

## List of things to implement
- [] Handle keeping track of SPECIFIC cards in the deck.


### Core
- [] Handle upside

### Card Types
- [] Wild Card
- [x] Glass Card (Kinda)
- [] Gold Card
- [] Lucky Card
- [] Negative
- [] Gold Seal
- [] Red Seal
- [] Blue Seal
- [] Purple Seal

### Decks
- [] Green Deck
- [] Anaglyph Deck
- [] Plasma Deck
- [] Erratic Deck

### Stakes
- [] Red Stake
- [] Green Stake
- [] Black Stake
- [] Blue Stake
- [] Orange Stake
- [] Gold Stake

### Jokers
- [] Credit Card (Just no?)
- [] Space Joker
- [] Hiker
- [] Faceless Joker
- [] Superposition
- [] To Do List
- [] Cavendish
- [] Card Sharp
- [] Séance
- [] Riff-Raff
- [x] Shortcut (Need to add check for if joker)
- [] Vagabond
- [] Cloud 9
- [] Rocket
- [] Midas Mask
- [] Luchador
- [x] Photograph (Need to add set_false at begining of bind)
- [] Gift Card
- [x] Reserved Parking (Chance based)
- [] Mail-In Rebate
- [] To the Moon
- [] Hallucination
- [] Golden Joker
- [] Diet Cola
- [] Trading Card
- [] Golden Ticket
- [] Mr. Bones
- [] Troubadour
- [] Certificate
- [] Smeared Joker
- [x] Throwback (Needs update check)
- [] Rough Gem
- [] Showman
- [x] Flower Pot (Needs active check)
- [] Blueprint
- [] Merry Andy
- [] Oops! All 6s
- [] The Idol
- [] Seeing Double
- [] Matador
- [] Invisible Joker
- [] Brainstorm
- [] Satellite
- [] Cartomancer
- [] Astronomer
- [] Burnt Joker
- [] Chicot
- [] Perkeo

### Boss Blinds
- [x] Amber Acorn (Nothing Needed)
- [] Verdant Leaf 
- [] Crimson Heart
- [] Cerulean Bell
- [] The Hook
- [] The Ox
- [] The House
- [x] The Wall (Nothing Needed)
- [] The Wheel
- [] The Arm
- [] The Fish
- [x] The Manacle (Nothing Needed)
- [x] The Serpent (Nothing Needed)
- [] The Pillar
- [] The Flint
- [] The Mark
