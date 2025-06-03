import pygame, sys
from pygame.locals import *

from pygame.surface import Surface
from utils.game_state_manager import GameStateManager
from utils.assets import *

from ui.text import TextUI
from ui.button import ButtonUI

from game_logic.game_logic_2048 import GameLogic2048

class Game2048Screen:
    def __init__(self, screen: Surface, game_state_manager: GameStateManager):
        self.screen = screen

        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.game_state_manager = game_state_manager

        self.game_logic = GameLogic2048(4)

        self.restart_button = ButtonUI(100, 40, 140, 50, 'Restart')

        self.animation = None

        self.playing = True

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
                elif self.playing and event.key == K_LEFT:
                    self.game_logic.move_left()
                    new_position = self.game_logic.insert_at_random_empty_space()
                    self.animation = (new_position, 200, pygame.time.get_ticks())
                    self.playing = not self.game_logic.no_moves_left

                elif self.playing and event.key == K_RIGHT:
                    self.game_logic.move_right()
                    new_position = self.game_logic.insert_at_random_empty_space()
                    self.animation = (new_position, 200, pygame.time.get_ticks())
                    self.playing = not self.game_logic.no_moves_left

                elif self.playing and event.key == K_UP:
                    self.game_logic.move_up()
                    new_position = self.game_logic.insert_at_random_empty_space()
                    self.animation = (new_position, 200, pygame.time.get_ticks())
                    self.playing = not self.game_logic.no_moves_left

                elif self.playing and event.key == K_DOWN:
                    self.game_logic.move_down()
                    new_position = self.game_logic.insert_at_random_empty_space()
                    self.animation = (new_position, 200, pygame.time.get_ticks())
                    self.playing = not self.game_logic.no_moves_left
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.restart_button.check_collision(event.pos):
                        self.game_logic.start_fresh()
                        self.playing = True

    def get_cell_color(self, cell_value: int):
        if cell_value == 0:
            return (189, 172, 151)
        if cell_value == 2:
            return (238, 228, 218)
        if cell_value == 4:
            return (235, 216, 182)
        if cell_value == 8:
            return (243, 178, 120)
        if cell_value == 16:
            return (246, 148, 97)
        # if cell_value == 32:
        return (247, 128, 100)
        
    def get_cell_value_color(self, cell_value: int):
        if cell_value == 2 or cell_value == 4:
            return (117, 100, 82)
        return WHITE

    def draw(self):
        self.screen.fill(WHITE)

        self.restart_button.draw(self.screen)

        TextUI(f'Points: {self.game_logic.points}').draw(self.screen, (self.width - 150, 50), big_font)
        TextUI(f'Moves: {self.game_logic.moves}').draw(self.screen, (self.width - 150, 80), big_font)

        if not self.playing:
            TextUI('No moves left!').draw(self.screen, (self.width / 2, 20), big_font)


        board_rect = pygame.Rect(0, 0, 400, 400)
        board_rect.center = (self.width // 2, self.height // 2)

        pygame.draw.rect(self.screen, (156, 137, 120), board_rect, border_radius= 12)

        padding = 8
        grid_size = self.game_logic.grid_size
        cell_size = (board_rect.size[0] - (padding * 2) - (padding * (grid_size - 1))) / grid_size

        for row in range(grid_size):
            for column in range(grid_size):
                scale = 1.0

                if self.animation:
                    position, duration, start_time = self.animation
                    if (row, column) == position:
                        elapsed_time = pygame.time.get_ticks() - start_time
        
                        if elapsed_time < duration:
                            progress = elapsed_time / duration
                            scale = 0.5 + 0.5 * progress
                        else:
                            self.animation = None

                scaled_size = cell_size * scale
                offset = (cell_size - scaled_size) / 2

                value = self.game_logic.grid[row][column]

                x = board_rect.x + padding + column * (cell_size + padding) 
                y = board_rect.y + padding + row * (cell_size + padding)
                new_rect = pygame.Rect(x + offset, y + offset, scaled_size, scaled_size)
                pygame.draw.rect(self.screen, self.get_cell_color(value), new_rect, border_radius= 12)

                if value > 0 and scale == 1.0:
                    TextUI(str(value)).draw(self.screen, new_rect.center, big_font, self.get_cell_value_color(value))
