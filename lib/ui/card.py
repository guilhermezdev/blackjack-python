import pygame
from utils.assets import *

class CardUI:
    def __init__(self, rank, suit):
        image = pygame.image.load(f'assets/images/cards/{suit}/{rank}.png')
        original_size = image.get_size()
        new_size = (original_size[0] * 5 , original_size[1] * 5)
        self.image = pygame.transform.scale(image, new_size)
        
        image_back = pygame.image.load(f'assets/images/cards/backs/back_0.png')
        original_size = image_back.get_size()
        new_size = (original_size[0] * 5, original_size[1] * 5)
        self.image_back = pygame.transform.scale(image_back, new_size)
    
    def image_size(self):
        return self.image.get_size()
    
    def draw_image(self, position, screen, showBack=False):
        image = self.image if not showBack else self.image_back
        image_rect = image.get_rect(bottomleft=position)
        
        screen.blit(image, image_rect)