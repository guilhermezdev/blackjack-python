import  pygame
from utils.assets import *

from ui.text import *
 
class Button():
    def __init__(self, x, y, width, height, title, callback = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x,y)
        self.callback = callback
        
    def draw(self, screen):
        color = WHITE
        
        pos = pygame.mouse.get_pos()
        
        if self.check_collision(pos):
            color = GRAY
        
        # draw button fill
        pygame.draw.rect(screen, color, self.rect, border_radius= 8)
        # draw button border
        pygame.draw.rect(screen, GRAY, self.rect, 2, border_radius= 8)
        
        text = Text(self.title)
        text.draw(screen, self.rect.center)
        
    def check_collision(self, pos):
        return self.rect.collidepoint(pos)
    
    def check_and_perform_click(self, pos):
        if self.check_collision(pos) and callable(self.callback):
            self.callback()

        