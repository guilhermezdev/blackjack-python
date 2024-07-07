import pygame, sys

from pygame.surface import Surface
from pygame.locals import *

from assets import *

from blackjack_game import *
from game_state_manager import *

class BlackjackScreen:
    def __init__(self, screen: Surface, game_state_manager: GameStateManager ):
        self.screen = screen
       
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.game_state_manager = game_state_manager
        
        self.game_state = BlackjackGame()
        self.game_state.new_game()
        
    def run(self):
        self.screen.fill(LIGHT_GREEN)
        
        hit_button_rect = pygame.Rect(self.width - 120, self.height - 70, 100, 50)
        stop_button_rect = pygame.Rect(self.width - 240, self.height - 70, 100, 50)
        restart_button_rect = pygame.Rect(self.width - 140, self.height - 70, 120, 50)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.game_state_manager.set_state('main_menu')
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if hit_button_rect.collidepoint(event.pos) and self.game_state.playing:
                        print("HIT button clicked!")
                        self.game_state.deal_card(self.game_state.player_hand)
                        self.game_state.check_game_status()
                        
                    elif stop_button_rect.collidepoint(event.pos) and self.game_state.playing:
                        print("STOP button clicked!")
                        self.game_state.playing = False
                        self.game_state.check_game_status()
                        
                    elif restart_button_rect.collidepoint(event.pos) and not self.game_state.playing:
                        print("RESTART button clicked!")
                        self.game_state.new_game()
    
        mouse_pos = pygame.mouse.get_pos()
        if hit_button_rect.collidepoint(mouse_pos):
            hit_button_color = hover_color
        else:
            hit_button_color = button_color

        if stop_button_rect.collidepoint(mouse_pos):
            stop_button_color = hover_color
        else:
            stop_button_color = button_color       

        if restart_button_rect.collidepoint(mouse_pos):
            restart_button_color = hover_color
        else:
            restart_button_color = button_color             

        # draw title
        text_surf = pixel_font.render('BLACKJACK PYTHON CASINO', True, BLACK)
        text_rect = text_surf.get_rect(center=(self.width / 2, 80))
        self.screen.blit(text_surf, text_rect)

        if self.game_state.playing:
            # Draw the HIT button
            pygame.draw.rect(self.screen, hit_button_color, hit_button_rect)

            # Draw text on the HIT button
            text_surf = small_pixel_font.render('HIT', True, BLACK)
            text_rect = text_surf.get_rect(center=hit_button_rect.center)
            self.screen.blit(text_surf, text_rect)

            # Draw the STOP button
            pygame.draw.rect(self.screen, stop_button_color, stop_button_rect)

            # Draw text on the STOP button
            text_surf = small_pixel_font.render('STOP', True, BLACK)
            text_rect = text_surf.get_rect(center=stop_button_rect.center)
            self.screen.blit(text_surf, text_rect)
        else:
            # Draw the RESTART button
            pygame.draw.rect(self.screen, restart_button_color, restart_button_rect)

            # Draw text on the RESTART button
            text_surf = small_pixel_font.render('RESTART', True, BLACK)
            text_rect = text_surf.get_rect(center=restart_button_rect.center)
            self.screen.blit(text_surf, text_rect)

            # draw result
            result = 'PLAYER WON' if self.game_state.player_won else 'DEALER WON' if self.game_state.dealer_won else 'TIE'
            text_surf = pixel_font.render(result, True, BLACK)
            text_rect = text_surf.get_rect(center=(self.width / 2, 160))
            self.screen.blit(text_surf, text_rect)


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
