# objects/paddle.py
import pygame
import math, time
from settings import *

class Paddle:
    def __init__(self):
        self.base_width = PADDLE_WIDTH
        self.rect = pygame.Rect(
            WIDTH//2 - PADDLE_WIDTH//2,
            HEIGHT - 40,
            PADDLE_WIDTH,
            PADDLE_HEIGHT
        )

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += PADDLE_SPEED

    def expand(self):
        self.rect.width = min(self.rect.width + 40, 200)

    def reset(self):
        self.rect.width = self.base_width

    def draw(self, screen):
        pygame.draw.rect(screen, NEON_CYAN, self.rect, border_radius=8)
        
        pulse = int(40 + 20 * math.sin(time.time() * 6))
        glow = pygame.Surface(
            (self.rect.width + pulse, self.rect.height + pulse),
            pygame.SRCALPHA
        )
        pygame.draw.rect(
            glow,
            (*NEON_CYAN, 60),
            glow.get_rect(),
            border_radius=20
        )
        screen.blit(
            glow,
            (self.rect.x - pulse//2, self.rect.y - pulse//2)
        )
