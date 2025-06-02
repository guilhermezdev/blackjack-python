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

        self.buttons = [
            ButtonUI(self.width / 2, 200, 130, 50, 'BLACKJACK', lambda: self.game_state_manger.set_state('blackjack')),
            ButtonUI(self.width / 2, 260, 130, 50, '2048', lambda: self.game_state_manger.set_state('2048')),
            ButtonUI(self.width / 2, 320, 130, 50, 'OPTIONS', lambda: self.game_state_manger.set_state('options')),
            ButtonUI(self.width / 2, 380, 130, 50, 'EXIT', lambda: self.exit())
        ]

    def exit(self):
        pygame.quit()
        sys.exit()
        
    def run(self):
        self.screen.fill(LIGHT_GREEN)
        self.handle_events()
        
        TextUI('MAIN MENU').draw(self.screen, (self.width / 2, 80), regular_font)

        for button in self.buttons:
            button.draw(self.screen)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    button.check_and_perform_click(event.pos)
        