import random
import sys
from functools import reduce

playing = True

money = 1000

shoe_deck = []

hearts   = chr(9829) # Character 9829 is '♥'.
diamonds = chr(9830) # Character 9830 is '♦'.
spades   = chr(9824) # Character 9824 is '♠'.
clubs    = chr(9827) # Character 9827 is '♣'.

ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
suits = [hearts, diamonds, spades, clubs]

def generate_deck():
    return [(x, y) for x in ranks for y in suits]

shoe_deck = generate_deck() * 6
random.shuffle(shoe_deck)


# Print a blackjack hand in the format:
#  ___   ___
# |A  | |J  |
# | ♥ | | ♠ |
# |__A| |__J|
#
def draw_hand(hand):
    first_line = ' ___  ' * len(hand)
    second_line = ' '.join([f'|{rank}  |' for rank, _ in hand])
    third_line = ' '.join([f'| {suit} |' for _, suit in hand])
    forth_line = ' '.join([f'|__{rank}|' for rank, _ in hand])
    
    print(first_line)
    print(second_line)
    print(third_line)
    print(forth_line)

def draw_back():
    print(' ___ ')
    print('|*  |')
    print('| * |')
    print('|__*|')


def hand_value(hand):
    ranks = [rank for rank, suit in hand]

    def add_card(acc, rank):
        value = 0
        if rank == 'A':
            value = 1
        elif rank == 'J' or rank == 'Q' or rank == 'K':
            value = 10
        else:
            value = int(rank)
        return acc + value

    total_value = reduce(add_card, ranks, 0)

    if total_value <= 10 and 'A' in ranks:
        total_value += 10
    
    return total_value

def print_player_hand():
    print('Player:')
    draw_hand(player_hand)
    print(f'\nTotal: {hand_value(player_hand)}')


while True:
    bet = 0
    while bet == 0:
        print(f'How much do you wanna bet? (available money: {money})')
        bet = int(input('> '))
        if bet < 0 or bet > money:
            print('Invalid bet, try again')
            bet = 0
    print(f'Betting: {bet}\n')

    dealer_hand = [shoe_deck.pop(), shoe_deck.pop()]
    player_hand = [shoe_deck.pop(), shoe_deck.pop()]

    print('Dealer:')
    draw_hand(dealer_hand)
    print()

    print_player_hand()
   
    print('\n(H)it, (S)tand, (Q)uit')
    option = input('> ').upper()
    print('')

    if option == 'H':
        player_hand.append(shoe_deck.pop())
    elif option == 'Q':
        sys.exit()

    print_player_hand()

