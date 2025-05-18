import pygame, sys

from pygame.surface import Surface
from pygame.locals import *

from utils.assets import *

from utils.blackjack_game import *
from utils.game_state_manager import *
from utils.events import *

from ui.button import *
from ui.text import *

class BlackjackScreen:
    def __init__(self, screen: Surface, game_state_manager: GameStateManager ):
        self.screen = screen
       
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.game_state_manager = game_state_manager
        
        self.blackjack_game = BlackjackGame()

        self.cash_out_button = Button(100, 40, 140, 50, 'Cash Out')
        
        self.hit_button = Button(self.width - 120, self.height - 110, 100, 50, 'Hit')
        self.stand_button = Button(self.width - 120, self.height - 50, 100, 50, 'Stand')

        self.betting_buttons = [
            Button(self.width / 2 - 140, self.height - 150, 50, 50, '5', lambda : self.update_bet(5)),
            Button(self.width / 2 - 70, self.height - 150, 50, 50, '10', lambda : self.update_bet(10)),
            Button(self.width / 2 , self.height - 150, 50, 50, '25', lambda : self.update_bet(25)),
            Button(self.width / 2 + 70, self.height - 150, 50, 50, '100', lambda : self.update_bet(100)),
            Button(self.width / 2 + 140, self.height - 150, 50, 50, '500', lambda : self.update_bet(500)),
            Button(self.width / 2, self.height - 70, 100, 50, 'BET', lambda: self.blackjack_game.start_hand(self.current_bet))
        ]

        self.current_bet = 0

    def update_bet(self, new_bet):
        self.current_bet += new_bet

    def run(self):
        self.handle_events()
        self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
            elif event.type == pygame.KEYDOWN:
               if event.key == K_ESCAPE:
                   self.game_state_manager.set_state('main_menu')
            elif event.type == go_to_betting_step:
                self.blackjack_game.start_betting()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.cash_out_button.check_collision(event.pos):
                        self.game_state_manager.set_state('main_menu')

                    if self.blackjack_game.game_step is GameStep.PLAYING:
                        if self.hit_button.check_collision(event.pos):
                            self.blackjack_game.deal_card(self.blackjack_game.player_hand)
                            self.blackjack_game.check_game_status() 
                        elif self.stand_button.check_collision(event.pos):
                            self.blackjack_game.stand()

                    elif self.blackjack_game.game_step is GameStep.BETTING:
                        for button in self.betting_buttons:
                            button.check_and_perform_click(event.pos)
                    
    def draw(self):
        self.screen.fill(WHITE)

        Text('BLACKJACK').draw(self.screen, (self.width / 2, 40), pixel_font)

        self.cash_out_button.draw(self.screen)

        if self.blackjack_game.game_step is GameStep.BETTING:
            Text(f'BET:{self.current_bet}').draw(self.screen, (self.width / 2, self.height / 2), pixel_font)
            for button in self.betting_buttons:
                button.draw(self.screen)

        if self.blackjack_game.game_step is GameStep.PLAYING:
            # draw dealer hand
            self.draw_hand('Dealer', self.blackjack_game.dealer_hand, 150, True)

            # draw player hand
            self.draw_hand('Player', self.blackjack_game.player_hand, self.height - 100)
        
            self.hit_button.draw(self.screen)
            self.stand_button.draw(self.screen)

        elif self.blackjack_game.game_step is GameStep.RESULT:
            result = 'PLAYER WON' if self.blackjack_game.player_won else 'DEALER WON' if self.blackjack_game.dealer_won else 'TIE'
            Text(result).draw(self.screen, (self.width / 2, 160), pixel_font)

            # draw dealer hand
            self.draw_hand('Dealer', self.blackjack_game.dealer_hand, 150, False)

            # draw player hand
            self.draw_hand('Player', self.blackjack_game.player_hand, self.height - 100)

    def draw_hand(self, name, hand, pos_y, hide = False):
        hand_value =  self.blackjack_game.value_of_hand(hand) if not hide else self.blackjack_game.dealer_hand[0].value()
        player_hand_text =  f'{name}: ' + str(hand_value)
        text_surf = pixel_font.render(player_hand_text, True, BLACK)
        text_rect = text_surf.get_rect(bottomleft=(20, pos_y))
        self.screen.blit(text_surf, text_rect)

        for index, card in enumerate(hand):
            card_width = card.image_size()[0]
            position_x = (self.width / 2  - card_width / 2) + (index * card_width * 0.25)
            position_y = pos_y + 80
            card.draw_image((position_x, position_y), self.screen, hide and index > 0)
        