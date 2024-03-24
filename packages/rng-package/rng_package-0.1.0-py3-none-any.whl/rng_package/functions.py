import random

def coin_flip(num_coins=1):
    result = ['heads', 'tails']
    return [random.choice(result) for _ in range(num_coins)]

def dice_roll(num_dice=1, sides=6):
    return [random.randint(1, sides) for _ in range(num_dice)]

def draw_cards(num_hands=1, num_cards=1):
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    face_cards = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
    jokers = ['Big Joker', 'Small Joker']

    deck = [(suit, value) for suit in suits for value in range(1, 14)]

    for joker in jokers:
        deck.append(('Joker', joker))

    random.shuffle(deck)
    
    hands = []
    for _ in range(num_hands):
        hand = []
        for _ in range(num_cards):
            suit, value = deck.pop()
            if suit == 'Joker':
                hand.append(value)
            else:
                if value in face_cards:
                    value = face_cards[value]
                else:
                    value = str(value)
                hand.append(f"{value} of {suit}")
        hands.append(hand)
    return hands

def generate_powerball():
    main_numbers = random.sample(range(1, 70), 5)
    powerball_number = random.randint(1, 26)
    powerball_combination = main_numbers + [powerball_number]
    return powerball_combination
