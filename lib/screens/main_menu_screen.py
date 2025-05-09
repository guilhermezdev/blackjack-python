import pygame, sys

from utils.assets import *

from pygame.surface import Surface

from utils.game_state_manager import *

from ui.button import *

from ui.text import *

class MainMenu:
    def __init__(self, screen: Surface, game_state_manager: GameStateManager):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.game_state_manger = game_state_manager
        
        self.play_button =  Button(self.width / 2, 200, 130, 50, 'PLAY')
        self.options_button = Button(self.width / 2, 260, 130, 50, 'OPTIONS')
        self.exit_button = Button(self.width / 2, 320, 130, 50, 'EXIT')
        
    def run(self):
        self.screen.fill(LIGHT_GREEN)
        self.handle_events()
        
        Text('MAIN MENU').draw(self.screen, (self.width / 2, 80), pixel_font)
        
        self.play_button.draw(self.screen)
        self.options_button.draw(self.screen)
        self.exit_button.draw(self.screen)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.play_button.check_collision(event.pos):
                    self.game_state_manger.set_state('blackjack')
                if self.options_button.check_collision(event.pos):
                    self.game_state_manger.set_state('options')
                elif self.exit_button.check_collision(event.pos):
                    pygame.quit()
                    sys.exit()
        