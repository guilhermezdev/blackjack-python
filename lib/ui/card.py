import pygame
from utils.assets import *

CARD_WIDTH = 100
CARD_HEIGHT = 140

class CardUI:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def image_size(self):
        return (CARD_WIDTH, CARD_HEIGHT)
    
    def draw_image(self, position, screen, showBack=False):
        x, y = position
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)

        if showBack:
            pygame.draw.rect(screen, RED, rect, border_radius=8)
            pygame.draw.rect(screen, BLACK, rect, width=2, border_radius=8)
            return
        
        # Draw card front
        pygame.draw.rect(screen, WHITE, rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, rect, width=2, border_radius=8)

        # Draw rank and suit text
        rank_text = regular_font.render(self.rank, True, (0, 0, 0))
        suit_text = regular_font.render(self.suit_symbol(), True, (0, 0, 0))

        # Top left rank
        screen.blit(rank_text, (x + 5, y + 5))
        screen.blit(suit_text, (x + 5, y + 25))

        # Bottom right rank (mirrored)
        rank_rect = rank_text.get_rect()
        suit_rect = suit_text.get_rect()

        screen.blit(rank_text, (x + CARD_WIDTH - rank_rect.width - 5, y + CARD_HEIGHT - rank_rect.height - 25))
        screen.blit(suit_text, (x + CARD_WIDTH - suit_rect.width - 5, y + CARD_HEIGHT - suit_rect.height - 5))

    def suit_symbol(self):
        symbols = {
            "hearts": "♥",
            "diamonds": "♦",
            "spades": "♠",
            "clubs": "♣"
        }
        return symbols.get(self.suit, "?")
