import sys
import pygame
from stickfight.src.constants import *
from stickfight.src.entities import Stickman
from stickfight.src.ai import AIController

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Stickman Fighting")
        self.clock = pygame.time.Clock()
        self.running = True

        # Entities
        self.player = Stickman(200, GROUND_Y, color=BLACK)
        self.enemy = Stickman(800, GROUND_Y, color=RED)

        # AI
        self.enemy_ai = AIController(self.enemy, self.player)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_z:
                    self.player.attack()

        # Continuous input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move(-1)
        if keys[pygame.K_RIGHT]:
            self.player.move(1)

    def update(self):
        dt = self.clock.get_time() # Time since last tick in ms
        self.player.update(dt)
        self.enemy.update(dt)
        self.enemy_ai.update()

        # Combat Checks
        if self.player.check_hit(self.enemy):
            self.enemy.take_damage(5)
            # print("Enemy Hit!")

        if self.enemy.check_hit(self.player):
            self.player.take_damage(5)
            # print("Player Hit!")

        # Game Over Check
        if self.player.health <= 0 or self.enemy.health <= 0:
            self._reset_game()

    def _reset_game(self):
        self.player = Stickman(200, GROUND_Y, color=BLACK)
        self.enemy = Stickman(800, GROUND_Y, color=RED)
        self.enemy_ai = AIController(self.enemy, self.player)

    def draw(self):
        self.screen.fill(WHITE)
        # Draw ground
        pygame.draw.line(self.screen, BLACK, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)

        # Draw Entities
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)

        # UI
        self._draw_ui()

        pygame.display.flip()

    def _draw_ui(self):
        # Player Health
        pygame.draw.rect(self.screen, RED, (50, 50, 200, 20))
        pygame.draw.rect(self.screen, GREEN, (50, 50, 2 * self.player.health, 20))

        # Enemy Health
        pygame.draw.rect(self.screen, RED, (SCREEN_WIDTH - 250, 50, 200, 20))
        pygame.draw.rect(self.screen, GREEN, (SCREEN_WIDTH - 250, 50, 2 * self.enemy.health, 20))

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()
