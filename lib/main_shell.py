import random
import sys
import os

hearts   = chr(9829) # Character 9829 is '♥'.
diamonds = chr(9830) # Character 9830 is '♦'.
spades   = chr(9824) # Character 9824 is '♠'.
clubs    = chr(9827) # Character 9827 is '♣'.

class Card():
    def __init__(self, rank: str, suit: str, value: int):
        self.rank = rank
        self.suit = suit
        self.value = value

    def is_ace(self):
        return self.rank == 'A'

class Deck():
    def __init__(self, shuffled = False):
        self.cards = self.generate_basic_deck()
        if shuffled:
            self.shuffle()

    def get_card(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        return None

    def shuffle(self):
        random.shuffle(self.cards)

    def generate_basic_deck(self):
        ranks = [('A', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10), ('J', 10), ('Q', 10), ('K', 10)]
        suits = [hearts, diamonds, spades, clubs]
        return [ Card(rank[0], suit, rank[1]) for rank in ranks for suit in suits ]
    
class Hand():
    def __init__(self, cards: list[Card]):
        self.cards = cards

    def add_card(self, card: Card):
        self.cards.append(card)

    def has_ace(self):
        return any(card.is_ace() for card in self.cards)

    def hand_value(self):
        total_value = sum(card.value for card in self.cards)

        if total_value <= 11 and self.has_ace():
            total_value += 10

        return total_value
    
    def is_blackjack(self):
        return len(self.cards) == 2 and self.hand_value() == 21

    # Print a blackjack hand in the format:
    #  ___   ___
    # |A  | |J  |
    # | ♥ | | ♠ |
    # |__A| |__J|
    #
    def draw_hand(self, hide = False):
        first_line = ' ___  ' * len(self.cards)
        second_line = ''
        third_line = ''
        forth_line = ''

        for i, card in enumerate(self.cards):
            is_hidden = hide and i == 1

            rank = card.rank if not is_hidden else '#'
            suit = card.suit if not is_hidden else ' '

            if len(rank) > 1:
                suit += ' '

            second_line += f"|{rank}  | "
            third_line += f"| {suit} | "
            forth_line += f"|__{rank}| "
        
        print(first_line)
        print(second_line)
        print(third_line)
        print(forth_line)
        print()

class BlackJackGame():
    def __init__(self, initial_money):
        self.money = initial_money
        self.bet = 0

    def make_bet(self):
        self.bet = bet
    

money = 1000
bet = 0

deck = Deck(shuffled= True)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def get_bet():
    while True:
        try:
            print(f'Place your bet: (available money: {money})')
            raw_bet = int(input('> '))
            if raw_bet > money or raw_bet <= 0:
                print('Wrong value')
                continue
            return raw_bet
        except ValueError:
            continue

def get_action(player_hand: Hand):
    can_double_down = len(player_hand.cards) == 2 and money >= bet
    actions = ['S', 'H']
    if can_double_down:
        actions.append('D')

    while True:
        if can_double_down:
            print(f'(S)tand, (H)it or (D)ouble Down. Hand value: {player_hand.hand_value()}')
        else:
            print(f'(S)tand or (H)it. Hand value: {player_hand.hand_value()}')
        action = input('> ').upper()

        if action not in actions:
            print('Wrong action')
            continue
        print()
        return action
    
def result(player_hand: Hand, dealer_hand: Hand):
    global money, bet
    player_hand_value = player_hand.hand_value()
    dealer_hand_value = dealer_hand.hand_value()
    
    print(f'Player hand value: {player_hand.hand_value()}')
    player_hand.draw_hand()
    print(f'Dealer hand value: {dealer_hand.hand_value()}')
    dealer_hand.draw_hand()

    if player_hand.is_blackjack() or dealer_hand.is_blackjack():
        if player_hand.is_blackjack() and not dealer_hand.is_blackjack():
            print('Player won with a Blackjack!')
            money += bet * 1.5
        elif not player_hand.is_blackjack():
            print('Dealer won with a Blackjack!')
            money -= bet
        else:
            print('Tie! Player and Dealer had a Blackjack!')
    elif player_hand_value > 21:
        print(f'Player busted with {player_hand_value}!')
        money -= bet
    elif dealer_hand_value > 21:
        print(f'Dealer busted with {dealer_hand_value}')
        money += bet
    elif player_hand_value > dealer_hand_value:
        print('Player won!')
        money += bet
    elif dealer_hand_value > player_hand_value:
        print('Player lost!')
        money -= bet
    else:
        print('Tie!')
    print()

while True:
    if money <= 0:
        print('Player went bankrupt, better luck next time!')
        sys.exit(0)

    bet = get_bet()

    player_hand = Hand([deck.get_card(), deck.get_card()])
    dealer_hand = Hand([deck.get_card(), deck.get_card()])

    stop = player_hand.hand_value() == 21

    while player_hand.hand_value() < 21 and not stop:
        print(f'Player hand value: {player_hand.hand_value()}')
        player_hand.draw_hand()
        print('Dealer hand value: ??')
        dealer_hand.draw_hand(True)

        action = get_action(player_hand)

        if action == 'S':
            stop = True
        elif action == 'H':
            player_hand.add_card(deck.get_card())
        elif action == 'D':
            player_hand.add_card(deck.get_card())
            bet += bet
            stop = True
    
    while dealer_hand.hand_value() < 17:
        dealer_hand.add_card(deck.get_card())

    cls()
    result(player_hand, dealer_hand)