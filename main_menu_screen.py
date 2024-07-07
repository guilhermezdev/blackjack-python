import pygame, sys

from assets import *

from pygame.surface import Surface

from game_state_manager import *

from button import *

from assets import *
from text import *

class MainMenu:
    def __init__(self, screen: Surface, game_state_manager: GameStateManager):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.game_state_manger = game_state_manager
        
        self.play_button =  Button(self.width / 2, 160, 100, 50, 'PLAY')
        
    def run(self):
        self.screen.fill(LIGHT_GREEN)
        self.handle_events()
        
        self.play_button.draw(self.screen)
        Text('MAIN MENU').draw(self.screen, (self.width / 2, 80), pixel_font)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.play_button.check_collision(event.pos):
                    self.game_state_manger.set_state('blackjack')
        