import pygame, os, sys

pygame.font.init()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
LIGHT_GREEN = (144, 238, 144)
RED = (200, 0, 0)

big_font = pygame.font.Font(resource_path('assets/fonts/SawarabiMincho-Regular.ttf'), 32)
regular_font = pygame.font.Font(resource_path('assets/fonts/SawarabiMincho-Regular.ttf'), 24)
small_font = pygame.font.Font(resource_path('assets/fonts/SawarabiMincho-Regular.ttf'), 16)