# effects/particles.py
import pygame
import random

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.dx = random.uniform(-3, 3)
        self.dy = random.uniform(-3, 3)
        self.life = 30
        self.color = color

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1

    def draw(self, screen):
        if self.life > 0:
            pygame.draw.circle(screen, self.color,
                                (int(self.x), int(self.y)), 3)
