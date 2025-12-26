# game.py
import pygame
import random
from settings import *
from objects.paddle import Paddle
from objects.ball import Ball
from effects.particles import Particle
from objects.powerup import PowerUp
from sound_manager import SoundManager
from save_manager import load_highscore, save_highscore
from level_manager import LevelManager


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("consolas", 24)
        self.big_font = pygame.font.SysFont("consolas", 48)

        self.sound = SoundManager()

        self.state = "playing"
        self.highscore = load_highscore()

        self.fade_alpha = 0
        self.shake_time = 0
        self.shake_intensity = 6

        # 🔹 LEVEL SYSTEM
        self.level_manager = LevelManager()
        self.current_level = 0

        self.paused = False
        self.reset_game()

    # ---------------- RESET GAME ----------------
    def reset_game(self):
        self.paddle = Paddle()
        self.balls = [Ball()]
        self.powerups = []
        self.particles = []

        self.score = 0
        self.lives = 3
        self.state = "playing"
        self.fade_alpha = 0

        self.ball_launched = False

        self.bricks = self.level_manager.load_level(self.current_level)

    # ---------------- LOAD NEXT LEVEL ----------------
    def load_next_level(self):
        self.current_level += 1

        if self.current_level >= self.level_manager.total_levels():
            self.state = "gameover"
            if self.score > self.highscore:
                self.highscore = self.score
                save_highscore(self.highscore)
            return

        self.bricks = self.level_manager.load_level(self.current_level)
        self.balls = [Ball()]
        self.ball_launched = False
        self.powerups.clear()
        self.particles.clear()

    # ---------------- UPDATE ----------------
    def update(self):
        if self.paused or self.state == "gameover":
            return

        keys = pygame.key.get_pressed()
        self.paddle.move(keys)

        # -------- BALL NOT LAUNCHED --------
        if not self.ball_launched:
            for ball in self.balls:
                ball.x = self.paddle.rect.centerx
                ball.y = self.paddle.rect.top - BALL_RADIUS - 2

            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                self.ball_launched = True

            return

        # ---------------- BALL UPDATE ----------------
        for ball in self.balls[:]:
            ball.move()

            # Paddle collision
            if self.paddle.rect.collidepoint(ball.x, ball.y):
                offset = (ball.x - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
                ball.dx = BALL_SPEED * offset
                ball.dy *= -1
                self.sound.play("paddle")

            # Brick collision
            for brick in self.bricks:
                if brick.alive and brick.rect.collidepoint(ball.x, ball.y):

                    brick.hit()        # 🔥 HIT LOGIC (STRONG / NORMAL)
                    ball.dy *= -1
                    self.shake_time = 10

                    if not brick.alive:
                        # Brick destroyed
                        self.score += 100
                        self.sound.play("brick")

                        for _ in range(10):
                            self.particles.append(
                                Particle(ball.x, ball.y, brick.color)
                            )

                        if random.random() < 0.3:
                            self.powerups.append(
                                PowerUp(brick.rect.centerx, brick.rect.centery)
                            )
                    else:
                        # Strong brick damaged (first hit)
                        self.sound.play("paddle")

                    break

            if ball.y > HEIGHT:
                self.balls.remove(ball)

        # -------- LIFE LOST --------
        if not self.balls:
            self.lives -= 1
            if self.lives <= 0:
                self.state = "gameover"
                self.sound.play("lose")
                if self.score > self.highscore:
                    self.highscore = self.score
                    save_highscore(self.highscore)
            else:
                self.balls.append(Ball())
                self.ball_launched = False

        # -------- LEVEL COMPLETE --------
        if all(not brick.alive for brick in self.bricks):
            self.load_next_level()

        # ---------------- POWER-UPS ----------------
        for power in self.powerups[:]:
            power.update()
            if power.rect.colliderect(self.paddle.rect):
                if power.type == "expand":
                    self.paddle.expand()
                elif power.type == "life":
                    self.lives += 1
                elif power.type == "multiball":
                    self.balls.append(Ball())

                self.sound.play("power")
                self.powerups.remove(power)

            elif power.rect.top > HEIGHT:
                self.powerups.remove(power)

        # ---------------- PARTICLES ----------------
        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)

    # ---------------- DRAW GAME OVER ----------------
    def draw_gameover(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, self.fade_alpha))
        self.screen.blit(overlay, (0, 0))
        self.fade_alpha = min(self.fade_alpha + 6, 200)

        cx, cy = WIDTH // 2, HEIGHT // 2

        title = self.big_font.render("GAME OVER", True, NEON_MAGENTA)
        score = self.font.render(f"Score: {self.score}", True, WHITE)
        high = self.font.render(f"High Score: {self.highscore}", True, NEON_CYAN)
        restart = self.font.render("Press R to Restart", True, WHITE)
        menu = self.font.render("Press M for Menu", True, WHITE)

        self.screen.blit(title, (cx - title.get_width() // 2, cy - 120))
        self.screen.blit(score, (cx - score.get_width() // 2, cy - 40))
        self.screen.blit(high, (cx - high.get_width() // 2, cy))
        self.screen.blit(restart, (cx - restart.get_width() // 2, cy + 60))
        self.screen.blit(menu, (cx - menu.get_width() // 2, cy + 100))

    # ---------------- DRAW UI ----------------
    def draw_ui(self):
        self.screen.blit(
            self.font.render(f"SCORE: {self.score}", True, WHITE), (20, 10)
        )
        self.screen.blit(
            self.font.render(f"LIVES: {self.lives}", True, WHITE), (WIDTH - 130, 10)
        )
        self.screen.blit(
            self.font.render(f"LEVEL: {self.current_level + 1}", True, NEON_CYAN),
            (WIDTH // 2 - 40, 10)
        )

        if not self.ball_launched:
            hint = self.font.render("Press SPACE or ↑ to Launch", True, NEON_CYAN)
            self.screen.blit(
                hint,
                (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 60)
            )

        if self.paused:
            pause = self.big_font.render("PAUSED", True, NEON_MAGENTA)
            self.screen.blit(
                pause,
                (WIDTH // 2 - pause.get_width() // 2,
                 HEIGHT // 2 - pause.get_height() // 2)
            )

    # ---------------- DRAW ----------------
    def draw(self):
        offset_x = offset_y = 0
        if self.shake_time > 0:
            offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_time -= 1

        self.screen.fill(BLACK)

        if self.state == "playing":
            self.paddle.draw(self.screen)
            for ball in self.balls:
                ball.draw(self.screen)
            for brick in self.bricks:
                brick.draw(self.screen)
            for power in self.powerups:
                power.draw(self.screen)
            for p in self.particles:
                p.draw(self.screen)
            self.draw_ui()

        elif self.state == "gameover":
            self.draw_gameover()

        if offset_x or offset_y:
            shaken = self.screen.copy()
            self.screen.fill(BLACK)
            self.screen.blit(shaken, (offset_x, offset_y))
