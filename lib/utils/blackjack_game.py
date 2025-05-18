import random, functools
import  pygame

from typing import List

from ui.card import *

from enum import Enum

from utils.events import *

class GameStep(Enum):
    BETTING = 1
    PLAYING = 2
    RESULT = 3
    GAME_OVER = 4

class BlackjackGame:
    def __init__(self):
        self.dealer_hand = []
        self.player_hand = []
        
        self.player_won = False
        self.dealer_won = False
        
        self.new_shoe_deck()

        self.player_chips = 1000
        self.bet = 0

        self.game_step = GameStep.BETTING

    def new_shoe_deck(self):
        self.shoe_deck = [Card(x, y) for x in ranks for y in suits] * 6
        random.shuffle(self.shoe_deck)

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
    
    def stand(self):
        self.game_step = GameStep.RESULT
        self.check_game_status()

    def show_result(self):
        self.game_step = GameStep.RESULT

        player_hand_value = self.value_of_hand(self.player_hand)

        if not self.player_won and not self.dealer_won:
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

        pygame.time.set_timer(go_to_betting_step, 5000, 1)
           
    def check_game_status(self):
        player_hand_value = self.value_of_hand(self.player_hand)

        if player_hand_value > 21:
            self.show_result()
            self.dealer_won = True
        elif player_hand_value == 21:
            self.show_result()
            if len(self.player_hand) == 2:
                self.player_won = True
    
    def start_betting(self):
        self.game_step = GameStep.BETTING
        self.bet = 0

    def start_hand(self, bet):
        self.bet = bet
        self.player_won = False
        self.dealer_won = False
        
        self.player_hand = []
        self.dealer_hand = []
        
        self.deal_card(self.player_hand)
        self.deal_card(self.dealer_hand)
        self.deal_card(self.player_hand)
        self.deal_card(self.dealer_hand)

        self.game_step = GameStep.PLAYING

        self.check_game_status()

    