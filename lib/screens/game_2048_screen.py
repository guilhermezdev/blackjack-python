import pygame, sys
from pygame.locals import *

from pygame.surface import Surface
from utils.game_state_manager import GameStateManager
from utils.assets import *

from ui.text import TextUI

from game_logic.game_logic_2048 import GameLogic2048

class Game2048Screen:
    def __init__(self, screen: Surface, game_state_manager: GameStateManager):
        self.screen = screen

        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.game_state_manager = game_state_manager

        self.game_logic = GameLogic2048(4)

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
               if event.key == K_LEFT:
                   self.game_logic.move_left()

    def draw(self):
        self.screen.fill(WHITE)

        board_rect = pygame.Rect(0, 0, 400, 400)
        board_rect.center = (self.width // 2, self.height // 2)

        pygame.draw.rect(self.screen, (156, 137, 120), board_rect, border_radius= 12)

        padding = 8
        grid_size = self.game_logic.grid_size
        cell_size = (board_rect.size[0] - (padding * 2) - (padding * (grid_size - 1))) / grid_size

        for row in range(grid_size):
            for column in range(grid_size):
                x = board_rect.x + padding + column * (cell_size + padding)
                y = board_rect.y + padding + row * (cell_size + padding)
                new_rect = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(self.screen, WHITE, new_rect, border_radius= 12)

                value = self.game_logic.grid[row][column]
                if value > 0:
                    TextUI(str(value)).draw(self.screen, new_rect.center)
