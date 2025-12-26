# menu.py
import pygame
import os
from settings import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Menu:
    def __init__(self, screen):
        self.screen = screen

        image_path = os.path.join(
            BASE_DIR, "assets", "images", "home.png"
        )

        self.bg = pygame.image.load(image_path).convert()
        # 🔑 SCALE TO VIRTUAL RESOLUTION
        self.bg = pygame.transform.smoothscale(self.bg, (WIDTH, HEIGHT))

        self.font = pygame.font.SysFont("consolas", 32)

    def draw(self):
        # Draw background on virtual screen
        self.screen.blit(self.bg, (0, 0))

        text = self.font.render("PRESS ENTER TO START", True, WHITE)
        self.screen.blit(
            text,
            (WIDTH // 2 - text.get_width() // 2, HEIGHT - 80)
        )
