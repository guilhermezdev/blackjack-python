import pygame, sys

from assets import *

from pygame.surface import Surface

from game_state_manager import *

from button import *

class MainMenu:
    def __init__(self, screen: Surface, game_state_manager: GameStateManager):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.game_state_manger = game_state_manager
        
    def run(self):
        self.screen.fill(LIGHT_GREEN)
        
        play_button = Button(self.width / 2, 160, 100, 50, 'PLAY')
        play_button.draw(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.check_collision(event.pos):
                    self.game_state_manger.set_state('blackjack')
        
        # draw title
        text_surf = pixel_font.render('MAIN MENU', True, BLACK)
        text_rect = text_surf.get_rect(center=(self.width / 2, 80))
        self.screen.blit(text_surf, text_rect)
