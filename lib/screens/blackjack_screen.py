import pygame, sys

from pygame.surface import Surface
from pygame.locals import *

from utils.assets import *

from game_logic import *
from utils.game_state_manager import GameStateManager

from ui.button import ButtonUI
from ui.text import TextUI
from ui.card import CardUI

from enum import Enum

class GameStep(Enum):
    BETTING = 0
    PLAYING = 1
    RESULT = 2

class BlackjackScreen:
    def __init__(self, screen: Surface, game_state_manager: GameStateManager):
        self.screen = screen
       
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.game_state_manager = game_state_manager
        
        self.blackjack_game = BlackJackGame(10000)

        self.cash_out_button = ButtonUI(100, 40, 140, 50, 'Cash Out')
        
        self.double_down_button = ButtonUI(self.width - 120, self.height - 170, 100, 50, 'Double Down', self.player_double_down)
        self.hit_button = ButtonUI(self.width - 120, self.height - 110, 100, 50, 'Hit', self.player_hit)
        self.stand_button = ButtonUI(self.width - 120, self.height - 50, 100, 50, 'Stand', self.player_stand)

        self.play_again_button = ButtonUI(self.width - 120, self.height - 110, 100, 50, 'Play Again', self.play_again)

        self.betting_buttons = [
            ButtonUI(self.width / 2 - 140, self.height - 150, 50, 50, '5', lambda : self.update_bet(5)),
            ButtonUI(self.width / 2 - 70, self.height - 150, 50, 50, '10', lambda : self.update_bet(10)),
            ButtonUI(self.width / 2 , self.height - 150, 50, 50, '25', lambda : self.update_bet(25)),
            ButtonUI(self.width / 2 + 70, self.height - 150, 50, 50, '100', lambda : self.update_bet(100)),
            ButtonUI(self.width / 2 + 140, self.height - 150, 50, 50, '500', lambda : self.update_bet(500)),
            ButtonUI(self.width / 2, self.height - 70, 100, 50, 'BET', self.start_round)
        ]

        self.game_step = GameStep.BETTING
        self.current_bet = 0
        self.result = None

    def update_bet(self, new_bet):
        self.current_bet += new_bet

    def run(self):
        self.handle_events()
        self.draw()

    def start_round(self):
        if self.current_bet > 0 and self.current_bet < self.blackjack_game.money:
            self.blackjack_game.start_round(self.current_bet)
            self.game_step = GameStep.PLAYING

    def player_hit(self):
        self.blackjack_game.player_hit()
        if self.blackjack_game.player_hand.busted() or self.blackjack_game.player_hand.value() == 21:
            self.blackjack_game.dealer_play()
            self.result = self.blackjack_game.stop_round()
            self.game_step = GameStep.RESULT
    
    def player_stand(self):
        self.blackjack_game.dealer_play()
        self.result = self.blackjack_game.stop_round()
        self.game_step = GameStep.RESULT
    
    def player_double_down(self):
        self.blackjack_game.double_down()
        self.blackjack_game.player_hit()
        self.blackjack_game.dealer_play()
        self.result = self.blackjack_game.stop_round()
        self.game_step = GameStep.RESULT

    def play_again(self):
        self.current_bet = 0
        self.result = None
        self.game_step = GameStep.BETTING

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
            elif event.type == pygame.KEYDOWN:
               if event.key == K_ESCAPE:
                   self.game_state_manager.set_state('main_menu')
            else:
                self.handle_game_events(event)

    def handle_game_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.cash_out_button.check_collision(event.pos):
                    self.game_state_manager.set_state('main_menu')
                if self.game_step == GameStep.PLAYING:
                    self.double_down_button.check_and_perform_click(event.pos)
                    self.hit_button.check_and_perform_click(event.pos)
                    self.stand_button.check_and_perform_click(event.pos)
                elif self.game_step == GameStep.BETTING:
                    for button in self.betting_buttons:
                        button.check_and_perform_click(event.pos)
                elif self.game_step == GameStep.RESULT:
                    self.play_again_button.check_and_perform_click(event.pos)

    def result_label(self, result: BlackJackGameResult):
        result_labels = {
            BlackJackGameResult.PLAYER_WON_BLACKJACK: "Blackjack! Player Win",
            BlackJackGameResult.DEALER_WON_BLACKJACK: "Dealer Blackjack! Player Lose",
            BlackJackGameResult.PLAYER_WON: "Player Win",
            BlackJackGameResult.DEALER_WON: "Dealer Wins",
            BlackJackGameResult.PLAYER_BUSTED: "Player Busted! Dealer Wins",
            BlackJackGameResult.DEALER_BUSTED: "Dealer Busted! Player Win",
            BlackJackGameResult.TIE: "Push — It's a Tie",
        }
        return result_labels[result]

    def draw(self):
        self.screen.fill(WHITE)

        TextUI('BLACKJACK').draw(self.screen, (self.width / 2, 40), regular_font)

        self.cash_out_button.draw(self.screen)

        TextUI(f'Money: {self.blackjack_game.money}').draw(self.screen, (self.width - 200, 80), regular_font)

        if self.game_step == GameStep.BETTING:
            TextUI(f'BET: {self.current_bet}').draw(self.screen, (self.width / 2, self.height / 2), regular_font)
            for button in self.betting_buttons:
                button.draw(self.screen)

        if self.game_step == GameStep.PLAYING:
            TextUI(f'Bet: {self.blackjack_game.bet}').draw(self.screen, (self.width - 200, 120), regular_font)

            self.draw_hand( self.blackjack_game.dealer_hand, 200, True)
            self.draw_hand( self.blackjack_game.player_hand, self.height - 160)
        
            if self.blackjack_game.can_double_down():
                self.double_down_button.draw(self.screen)

            self.hit_button.draw(self.screen)
            self.stand_button.draw(self.screen)

        elif self.game_step == GameStep.RESULT:
            TextUI(self.result_label(self.result)).draw(self.screen, (self.width / 2, 140), regular_font)

            self.play_again_button.draw(self.screen)

            self.draw_hand( self.blackjack_game.dealer_hand, 200, False)
            self.draw_hand( self.blackjack_game.player_hand, self.height - 160)

    def draw_hand(self,  hand: Hand, pos_y: int, hide = False):
        player_hand_text = str(hand.value()) if not hide else '??'
        text_surf = regular_font.render(player_hand_text, True, BLACK)
        text_rect = text_surf.get_rect(bottomleft=(20, pos_y + 80))
        self.screen.blit(text_surf, text_rect)

        for index, card in enumerate(hand.cards):
            card_ui = CardUI(card.rank, card.suit)
            card_width = card_ui.image_size()[0]
            position_x =  card_width / 2 + (index * card_width * 0.3)
            card_ui.draw_image((position_x, pos_y), self.screen, hide and index > 0)
        