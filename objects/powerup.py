# objects/powerup.py
import pygame
import random
from settings import *

POWER_COLORS = {
    "expand": NEON_CYAN,
    "multiball": NEON_MAGENTA,
    "life": NEON_GREEN
}

class PowerUp:
    def __init__(self, x, y):
        self.type = random.choice(list(POWER_COLORS.keys()))
        self.rect = pygame.Rect(x, y, 25, 25)
        self.speed = 3

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            POWER_COLORS[self.type],
            self.rect,
            border_radius=6
        )
