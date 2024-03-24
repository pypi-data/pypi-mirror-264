from rng_package.functions import *

def test_coin_flip_defaults():
    # Test default behavior with one coin flip
    result = coin_flip()
    assert len(result) == 1
    assert result[0] in ['heads', 'tails']

def test_coin_flip_multiple_coins():
    # Test flipping multiple coins
    num_coins = 5
    result = coin_flip(num_coins)
    assert len(result) == num_coins
    assert all(coin in ['heads', 'tails'] for coin in result)

def test_coin_flip_invalid_input():
    # Test with invalid input (negative number of coins)
    num_coins = -1
    result = coin_flip(num_coins)
    assert len(result) == 0  # Expect an empty list for negative input

def test_dice_roll_defaults():
    # Test default behavior with one die and six sides
    result = dice_roll()
    assert len(result) == 1
    assert 1 <= result[0] <= 6

def test_dice_roll_multiple_dice():
    # Test rolling multiple dice
    num_dice = 3
    result = dice_roll(num_dice)
    assert len(result) == num_dice
    assert all(1 <= die <= 6 for die in result)

def test_dice_roll_custom_sides():
    # Test rolling dice with custom number of sides
    num_dice = 5
    sides = 10
    result = dice_roll(num_dice, sides)
    assert len(result) == num_dice
    assert all(1 <= die <= sides for die in result)

def test_dice_roll_invalid_input():
    # Test with invalid input (negative number of dice)
    num_dice = -1
    sides = 6
    result = dice_roll(num_dice, sides)
    assert len(result) == 0  # Expect an empty list for negative input

def test_draw_cards_defaults():
    # Test default behavior with one hand and one card
    result = draw_cards()
    assert len(result) == 1
    assert len(result[0]) == 1

def test_draw_cards_multiple_hands():
    # Test drawing multiple hands
    num_hands = 3
    result = draw_cards(num_hands)
    assert len(result) == num_hands
    assert all(len(hand) == 1 for hand in result)

def test_draw_cards_multiple_cards():
    # Test drawing multiple cards in each hand
    num_cards = 5
    result = draw_cards(num_cards=num_cards)
    assert len(result) == 1
    assert len(result[0]) == num_cards

def test_draw_cards_invalid_input():
    # Test with invalid input (negative number of hands)
    num_hands = -1
    num_cards = 5
    result = draw_cards(num_hands, num_cards)
    assert len(result) == 0  # Expect an empty list for negative input

def test_generate_powerball_defaults():
    # Test default behavior
    result = generate_powerball()
    assert len(result) == 6
    assert all(1 <= num <= 69 for num in result[:5])
    assert 1 <= result[5] <= 26

def test_generate_powerball_multiple_times():
    # Test generating multiple powerball combinations
    num_times = 10
    results = [generate_powerball() for _ in range(num_times)]
    assert all(len(result) == 6 for result in results)
    assert all(1 <= num <= 69 for result in results for num in result[:5])
    assert all(1 <= result[5] <= 26 for result in results)

def test_generate_powerball_unique_combinations():
    # Test generating multiple powerball combinations and ensure uniqueness
    num_times = 1000
    results = [generate_powerball() for _ in range(num_times)]
    unique_results = set(tuple(result) for result in results)
    assert len(results) == len(unique_results)