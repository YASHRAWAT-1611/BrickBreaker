# objects/ball.py
import pygame
import random
from settings import *

class Ball:
    def __init__(self):
        self.trail = []      # ✅ define first
        self.reset()

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.dx = random.choice([-BALL_SPEED, BALL_SPEED])
        self.dy = -BALL_SPEED
        self.trail.clear()

    def move(self):
        self.trail.append((self.x, self.y))
        if len(self.trail) > 12:
            self.trail.pop(0)

        self.x += self.dx
        self.y += self.dy

        if self.x <= BALL_RADIUS or self.x >= WIDTH - BALL_RADIUS:
            self.dx *= -1
        if self.y <= BALL_RADIUS:
            self.dy *= -1

    def draw(self, screen):
        # Trail glow
        for i, pos in enumerate(self.trail):
            alpha = i * 15
            glow = pygame.Surface((BALL_RADIUS*4, BALL_RADIUS*4), pygame.SRCALPHA)
            pygame.draw.circle(
                glow,
                (*NEON_MAGENTA, alpha),
                (BALL_RADIUS*2, BALL_RADIUS*2),
                BALL_RADIUS
            )
            screen.blit(glow, (pos[0]-BALL_RADIUS*2, pos[1]-BALL_RADIUS*2))

        pygame.draw.circle(
            screen,
            NEON_MAGENTA,
            (int(self.x), int(self.y)),
            BALL_RADIUS
        )
