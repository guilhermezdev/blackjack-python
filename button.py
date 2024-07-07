import  pygame
from assets import *

from text import *
 
class Button():
    def __init__(self, x, y, width, height, title):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x,y)
        
    def draw(self, screen):
        color = button_color
        
        pos = pygame.mouse.get_pos()
        
        if self.check_collision(pos):
            color = hover_color
        
        pygame.draw.rect(screen, color, self.rect)
        
        text = Text(self.title)
        text.draw(screen, self.rect.center)
        
    def check_collision(self, pos):
        return self.rect.collidepoint(pos)
        