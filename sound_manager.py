# sound_manager.py
import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        self.sounds = {
            "paddle": pygame.mixer.Sound("assets/sounds/hit.wav"),
            "brick": pygame.mixer.Sound("assets/sounds/brick.wav"),
            "power": pygame.mixer.Sound("assets/sounds/powerup.wav"),
            "lose": pygame.mixer.Sound("assets/sounds/lose.wav"),
        }

        # Volume control
        for sound in self.sounds.values():
            sound.set_volume(0.4)

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()
