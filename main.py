# main.py
import pygame
from settings import *
from game import Game
from menu import Menu

pygame.init()

# OS window (can resize / fullscreen)
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Neon Brick Breaker")

# Virtual game surface (FIXED resolution)
screen = pygame.Surface((WIDTH, HEIGHT))

# Music
pygame.mixer.music.load("assets/sounds/music.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)
music_on = True

clock = pygame.time.Clock()

menu = Menu(screen)
game = None
game_active = False
fullscreen = False

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.KEYDOWN:
        
            # Fullscreen toggle
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    
            # Music mute toggle
            if event.key == pygame.K_m:
                music_on = not music_on
                pygame.mixer.music.set_volume(0.4 if music_on else 0)
    
            # Menu → Game
            if not game_active and event.key == pygame.K_RETURN:
                game = Game(screen)
                game_active = True
    
            # Game controls
            if game_active:
                if event.key == pygame.K_p:
                    game.paused = not game.paused
                if event.key == pygame.K_ESCAPE:
                    game_active = False
    
            # Game Over controls
            if game_active and game.state == "gameover":
                if event.key == pygame.K_r:
                    game = Game(screen)
                if event.key == pygame.K_m:
                    game_active = False


    # ----- DRAW ON VIRTUAL SCREEN -----
    if not game_active:
        if menu.draw():
            game = Game(screen)
            game_active = True
    else:
        game.update()
        game.draw()

    # ----- SCALE TO WINDOW (THIS FIXES EVERYTHING) -----
    win_w, win_h = window.get_size()
    scaled_surface = pygame.transform.smoothscale(screen, (win_w, win_h))
    window.blit(scaled_surface, (0, 0))

    pygame.display.flip()

pygame.quit()
