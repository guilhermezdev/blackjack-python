import  pygame

from assets import *

from main_menu_screen import *
from blackjack_screen import *
from game_state_manager import *

w = 960
h = 540

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((w, h))
        self.clock = pygame.time.Clock()
        
        self.game_state_manager = GameStateManager('main_menu')
        
        self.main_menu_screen = MainMenu(self.screen, self.game_state_manager)
        self.blackjack_screen = BlackjackScreen(self.screen, self.game_state_manager)
        
        self.game_states = {'main_menu': self.main_menu_screen, 'blackjack': self.blackjack_screen}
        
    def run(self):
        while True:
            pygame.display.update()
            self.clock.tick(60)
        
            self.game_states[self.game_state_manager.get_state()].run()

game = Game()
game.run()
