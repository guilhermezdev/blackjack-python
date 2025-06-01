import pygame, sys

from pygame.surface import Surface

from utils.game_state_manager import *

from ui.button import *

from utils.assets import *
from ui.text import *

from utils.config import *

class Options:
    def __init__(self, screen: Surface, game_state_manager: GameStateManager):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.game_state_manger = game_state_manager
        
        self.muted = game_config.get_muted()
        
        self.back_button = ButtonUI(self.width / 2, 320, 130, 50, 'BACK')
        self.mute_button = ButtonUI(self.width / 2, 200, 130, 50,  'UNMUTE' if self.muted else 'MUTE')
        
    def run(self):
        self.screen.fill(LIGHT_GREEN)
        self.handle_events()
        
        TextUI('OPTIONS').draw(self.screen, (self.width / 2, 80), regular_font)

        self.back_button.draw(self.screen)
        self.mute_button.draw(self.screen)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.back_button.check_collision(event.pos):
                    self.game_state_manger.set_state('main_menu')
                elif self.mute_button.check_collision(event.pos):
                    self.muted = not self.muted
                    game_config.set_muted(self.muted)
                    pygame.mixer.music.set_volume(0 if self.muted else 1)
