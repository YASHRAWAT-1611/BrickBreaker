# objects/brick.py
import pygame
from settings import *

class Brick:
    def __init__(self, x, y, brick_type):
        self.rect = pygame.Rect(x, y, 70, 25)
        self.type = brick_type
        self.alive = True

        if brick_type == "strong":
            self.hits = 2
            self.color = NEON_ORANGE
        else:
            self.hits = 1
            self.color = NEON_GREEN

    def hit(self):
        self.hits -= 1
        if self.hits <= 0:
            self.alive = False

    def draw(self, screen):
        if not self.alive:
            return

        pygame.draw.rect(screen, self.color, self.rect, border_radius=6)

        # 🔥 CRACK EFFECT FOR DAMAGED STRONG BRICK
        if self.type == "strong" and self.hits == 1:
            pygame.draw.line(
                screen, WHITE,
                (self.rect.left + 5, self.rect.top + 5),
                (self.rect.right - 5, self.rect.bottom - 5), 2
            )
            pygame.draw.line(
                screen, WHITE,
                (self.rect.left + 5, self.rect.bottom - 5),
                (self.rect.right - 5, self.rect.top + 5), 2
            )
