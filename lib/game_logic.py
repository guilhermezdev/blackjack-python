import random
from enum import Enum

class BlackJackGameResult(Enum):
    PLAYER_WON_BLACKJACK = 0
    DEALER_WON_BLACKJACK = 1
    PLAYER_WON = 2
    DEALER_WON = 3
    PLAYER_BUSTED = 4
    DEALER_BUSTED = 5
    TIE = 6

class Card():
    def __init__(self, rank: str, suit: str, value: int):
        self.rank = rank
        self.suit = suit
        self.value = value

    def is_ace(self):
        return self.rank == 'A'
    
    def __str__(self):
        return f'{self.rank} {self.suit}'

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
        suits = ['hearts', 'diamonds', 'spades', 'clubs']
        return [Card(rank[0], suit, rank[1]) for rank in ranks for suit in suits]
    
class Hand():
    def __init__(self, cards: list[Card]):
        self.cards = cards

    def add_card(self, card: Card):
        self.cards.append(card)

    def has_ace(self):
        return any(card.is_ace() for card in self.cards)

    def value(self):
        total_value = sum(card.value for card in self.cards)

        if total_value <= 11 and self.has_ace():
            total_value += 10

        return total_value
    
    def is_blackjack(self):
        return len(self.cards) == 2 and self.value() == 21
    
    def busted(self):
        return self.value() > 21
    

class BlackJackGame():
    def __init__(self, initial_money: int):
        self.money = initial_money
        self.bet = 0
        self.deck = Deck(shuffled= True)

    def start_round(self, bet: int):
        self.bet = bet

        self.player_hand = Hand([self.deck.get_card(), self.deck.get_card()])
        self.dealer_hand = Hand([self.deck.get_card(), self.deck.get_card()])

    def player_hit(self):
        next_card = self.deck.get_card()
        self.player_hand.add_card(next_card)

        return next_card
    
    def dealer_play(self):
        while self.dealer_hand.value() < 17:
            self.dealer_hand.add_card(self.deck.get_card())

    def can_double_down(self):
        return len(self.player_hand.cards) == 2 and self.money >= self.bet
    
    def double_down(self):
        if self.can_double_down():
            self.bet *= 2
    
    def stop_round(self):
        player = self.player_hand
        dealer = self.dealer_hand

        if player.is_blackjack() and not dealer.is_blackjack():
            win = int(self.bet * 1.5)
            self.money += win
            return BlackJackGameResult.PLAYER_WON_BLACKJACK
        if dealer.is_blackjack() and not player.is_blackjack():
            self.money -= self.bet
            return BlackJackGameResult.DEALER_WON_BLACKJACK
        if player.busted():
            self.money -= self.bet
            return BlackJackGameResult.PLAYER_BUSTED
        if dealer.busted():
            self.money += self.bet
            return BlackJackGameResult.DEALER_BUSTED
        if player.value() > dealer.value():
            self.money += self.bet
            return BlackJackGameResult.PLAYER_WON
        if player.value() < dealer.value():
            self.money -= self.bet
            return BlackJackGameResult.DEALER_WON

        return BlackJackGameResult.TIE
