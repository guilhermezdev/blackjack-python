import random, functools
from typing import List

from card import *

class BlackjackGame:
    def __init__(self):
        self.playing = True
        self.dealer_hand = []
        self.player_hand = []
        
        self.player_won = False
        self.dealer_won = False
        
        deck = [Card(x, y) for x in ranks for y in suits] * 6
        random.shuffle(deck)
        
        self.shoe_deck = deck * 6

    def deal_card(self, hand: List[Card]):
        hand.append(self.shoe_deck.pop())     

    def value_of_hand(self, hand: List[Card]):
        value = functools.reduce(lambda acc, card: acc + card.value(), hand, 0)
        aces_count = sum(1 for card in hand if card.is_ace())
        if aces_count > 0 and value < 12:
            while value <= 21 and aces_count > 0:
                value = value + 10
                aces_count = aces_count - 1
        return value
           
    def check_game_status(self):
        player_hand_value = self.value_of_hand(self.player_hand)

        if player_hand_value > 21:
            self.playing = False
            self.dealer_won = True
        elif player_hand_value == 21:
            self.playing = False
            if len(self.player_hand) == 2:
                self.player_won = True

        if not self.playing and not self.player_won and not self.dealer_won:
            while self.value_of_hand(self.dealer_hand) < 17:
                self.deal_card(self.dealer_hand)

            dealer_hand_value = self.value_of_hand(self.dealer_hand)

            if dealer_hand_value > 21:
                self.player_won = True
            elif dealer_hand_value == 21 and len(self.dealer_hand) == 2:
                self.dealer_won = True
            elif dealer_hand_value == player_hand_value:
                self.dealer_won = False
                self.player_won = False
            elif player_hand_value > dealer_hand_value:
                self.player_won = True
            else:
                self.dealer_won = True
                
    def new_game(self):
        self.playing = True
        self.player_won = False
        self.dealer_won = False
        
        self.player_hand = []
        self.dealer_hand = []
        
        self.deal_card(self.player_hand)
        self.deal_card(self.dealer_hand)
        self.deal_card(self.player_hand)
        self.deal_card(self.dealer_hand)
        
        self.check_game_status()
    