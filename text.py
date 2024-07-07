from pygame.surface import Surface
from pygame.font import Font
from pygame.rect import Rect

from assets import *

class Text():
    def __init__(self, text):
        self.text = text
    
    def draw(self, screen: Surface, center : tuple[float, float], font: Font = small_pixel_font):
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=center)
        screen.blit(text_surf, text_rect)
        