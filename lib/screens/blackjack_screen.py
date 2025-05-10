import pygame, sys

from pygame.surface import Surface
from pygame.locals import *

from utils.assets import *

from utils.blackjack_game import *
from utils.game_state_manager import *

from ui.button import *
from ui.text import *

class BlackjackScreen:
    def __init__(self, screen: Surface, game_state_manager: GameStateManager ):
        self.screen = screen
       
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.game_state_manager = game_state_manager
        
        self.blackjack_game = BlackjackGame()
        self.blackjack_game.new_game()
        
        self.hit_button = Button(self.width - 120, self.height - 70, 100, 50, 'HIT')
        self.stop_button = Button(self.width - 240, self.height - 70, 100, 50, 'STOP')
        self.restart_button = Button(self.width - 140, self.height - 70, 120, 50, 'RESTART')
        
    def run(self):
        self.handle_basic_events()

        self.draw()

    def handle_basic_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
            elif event.type == pygame.KEYDOWN:
               if event.key == K_ESCAPE:
                   self.game_state_manager.set_state('main_menu')      
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.blackjack_game.game_step is GameStep.PLAYING:
                        if self.hit_button.check_collision(event.pos):
                            self.blackjack_game.deal_card(self.blackjack_game.player_hand)
                            self.blackjack_game.check_game_status()
                            
                        elif self.stop_button.check_collision(event.pos):
                            self.blackjack_game.game_step = GameStep.GAME_OVER
                            self.blackjack_game.check_game_status()

                    elif self.blackjack_game.game_step is GameStep.GAME_OVER:
                        if self.restart_button.check_collision(event.pos):
                            self.blackjack_game.new_game()   
                    
    def draw(self):
        self.screen.fill(LIGHT_GREEN)

        Text('BLACKJACK PYTHON CASINO').draw(self.screen, (self.width / 2, 80), pixel_font)

        if self.blackjack_game.game_step is GameStep.PLAYING:
            # draw dealer hand
            self.draw_hand('Dealer', self.blackjack_game.dealer_hand, self.height - 250, True)

            # draw player hand
            self.draw_hand('Player', self.blackjack_game.player_hand, self.height - 100)
        
            self.hit_button.draw(self.screen)
            self.stop_button.draw(self.screen)

        elif self.blackjack_game.game_step is GameStep.GAME_OVER:
            self.restart_button.draw(self.screen)
            
            result = 'PLAYER WON' if self.blackjack_game.player_won else 'DEALER WON' if self.blackjack_game.dealer_won else 'TIE'
            Text(result).draw(self.screen, (self.width / 2, 160), pixel_font)

    def draw_hand(self, name, hand, pos_y, hide = False):
        hand_value =  self.blackjack_game.value_of_hand(hand) if not hide else self.blackjack_game.dealer_hand[0].value()
        player_hand_text =  f'{name}: ' + str(hand_value)
        text_surf = pixel_font.render(player_hand_text, True, BLACK)
        text_rect = text_surf.get_rect(bottomleft=(20, pos_y))
        self.screen.blit(text_surf, text_rect)

        for index, card in enumerate(hand):
            position_x = 20 + index * card.image_size()[0] * 1.1
            position_y = pos_y + 80
            card.draw_image((position_x, position_y), self.screen, hide and index > 0)
        