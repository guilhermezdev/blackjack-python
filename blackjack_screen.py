import pygame, sys

from pygame.surface import Surface
from pygame.locals import *

from assets import *

from blackjack_game import *
from game_state_manager import *

from button import *
from text import *

class BlackjackScreen:
    def __init__(self, screen: Surface, game_state_manager: GameStateManager ):
        self.screen = screen
       
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.game_state_manager = game_state_manager
        
        self.game_state = BlackjackGame()
        self.game_state.new_game()
        
        self.hit_button = Button(self.width - 120, self.height - 70, 100, 50, 'HIT')
        self.stop_button = Button(self.width - 240, self.height - 70, 100, 50, 'STOP')
        self.restart_button = Button(self.width - 140, self.height - 70, 120, 50, 'RESTART')
        
    def run(self):
        self.screen.fill(LIGHT_GREEN)
        self.handle_events()
        self.draw()
  
        # draw dealer hand
        dealer_hand_text =  'Dealer: ' + (str(self.game_state.value_of_hand(self.game_state.dealer_hand)) if not self.game_state.playing else str(self.game_state.dealer_hand[0].value()))
        text_surf = pixel_font.render(dealer_hand_text, True, BLACK)
        text_rect = text_surf.get_rect(bottomleft=(20, self.height - 250))
        self.screen.blit(text_surf, text_rect)

        for index, card in enumerate(self.game_state.dealer_hand):
            position_x = 20 + index * card.image_size()[0] * 1.1
            position_y = self.height - 170
            card.draw_image((position_x, position_y), self.screen, self.game_state.playing and index > 0)

        # draw player hand
        player_hand_text =  'Player: ' + str(self.game_state.value_of_hand(self.game_state.player_hand))
        text_surf = pixel_font.render(player_hand_text, True, BLACK)
        text_rect = text_surf.get_rect(bottomleft=(20, self.height - 100))
        self.screen.blit(text_surf, text_rect)

        for index, card in enumerate(self.game_state.player_hand):
            position_x = 20 + index * card.image_size()[0] * 1.1
            position_y = self.height - 20
            card.draw_image((position_x, position_y), self.screen)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.game_state_manager.set_state('main_menu')
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.hit_button.check_collision(event.pos) and self.game_state.playing:
                        self.game_state.deal_card(self.game_state.player_hand)
                        self.game_state.check_game_status()
                        
                    elif self.stop_button.check_collision(event.pos) and self.game_state.playing:
                        self.game_state.playing = False
                        self.game_state.check_game_status()
                        
                    elif self.restart_button.check_collision(event.pos) and not self.game_state.playing:
                        self.game_state.new_game()
                        
    def draw(self):
        Text('BLACKJACK PYTHON CASINO').draw(self.screen, (self.width / 2, 80), pixel_font)
        
        if self.game_state.playing:
            self.hit_button.draw(self.screen)
            self.stop_button.draw(self.screen)
        else:
            self.restart_button.draw(self.screen)
            
            result = 'PLAYER WON' if self.game_state.player_won else 'DEALER WON' if self.game_state.dealer_won else 'TIE'
            Text(result).draw(self.screen, (self.width / 2, 160), pixel_font)
        