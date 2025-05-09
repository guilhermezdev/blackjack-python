import pygame

suits = ['spades', 'clubs', 'diamonds', 'hearts']
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        
        image = pygame.image.load(f'assets/images/cards/{self.suit}/{self.rank}.png')
        original_size = image.get_size()
        new_size = (original_size[0] * 2, original_size[1] * 2)
        self.image = pygame.transform.scale(image, new_size)
        
        image_back = pygame.image.load(f'assets/images/cards/backs/back_0.png')
        original_size = image_back.get_size()
        new_size = (original_size[0] * 2, original_size[1] * 2)
        self.image_back = pygame.transform.scale(image_back, new_size)
    
    def value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        if self.is_ace():
            return 1
        return int(self.rank)
        
    def is_ace(self):
        return self.rank == 'A'
    
    def image_size(self):
        return self.image.get_size()
    
    def draw_image(self, position, screen, showBack=False):
        image = self.image if not showBack else self.image_back
        image_rect = image.get_rect(bottomleft=position)
        screen.blit(image, image_rect)
    
    def __repr__(self):
        return f'{self.rank} of {self.suit}'
    
    def __str__(self):
        return f'{self.rank} of {self.suit}'
    