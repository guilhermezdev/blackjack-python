from pygame.surface import Surface
from pygame.font import Font

from utils.assets import *

class TextUI:
    def __init__(self, text):
        self.text = text
    
    def draw(self, screen: Surface, center : tuple[float, float], font: Font = small_font, color = BLACK):
        text_surf = font.render(self.text, True, color)
        text_rect = text_surf.get_rect(center=center)
        screen.blit(text_surf, text_rect)
        