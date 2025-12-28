import sys
import pygame
from stickfight.src.constants import *
from stickfight.src.entities import Stickman
from stickfight.src.ai import AIController
from stickfight.src.particles import ParticleManager
from stickfight.src.weapons import Sword, Spear, Axe
from stickfight.src.world import load_test_level
from stickfight.src.waves import WaveManager
from stickfight.src.ui import UIManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Stickman Fighting")
        self.clock = pygame.time.Clock()
        self.running = True

        # Systems
        self.particles = ParticleManager()
        self.level = load_test_level()

        # Entities
        self.player = Stickman(200, GROUND_Y, color=BLACK)
        self.player.equip_weapon(Sword())
        self.player.level = self.level

        # Inject Particle Manager into Player
        self.player.particles = self.particles

        # Waves
        self.wave_manager = WaveManager(self)

        # UI
        self.ui = UIManager(self)

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

        if keys[pygame.K_x]:
            self.player.block(True)
        else:
            self.player.block(False)

    def update(self):
        dt = self.clock.get_time() # Time since last tick in ms

        self.particles.update(dt)
        self.level.update(dt)
        self.player.update(dt)

        self.wave_manager.update(dt)

        # Combat Checks against Wave Enemies
        for data in self.wave_manager.enemies:
            enemy = data['entity']

            # Player hits Enemy
            if self.player.check_hit(enemy):
                enemy.take_damage(self.player.weapon.damage)
                self.particles.create_blood(enemy.position.x, enemy.position.y - 40)
                self.particles.create_spark(enemy.position.x, enemy.position.y - 40)

            # Enemy hits Player
            if enemy.check_hit(self.player):
                self.player.take_damage(enemy.weapon.damage)
                self.particles.create_blood(self.player.position.x, self.player.position.y - 40)
                self.particles.create_spark(self.player.position.x, self.player.position.y - 40)

        # Game Over Check
        if self.player.health <= 0:
            self._reset_game()

    def _reset_game(self):
        self.player = Stickman(200, GROUND_Y, color=BLACK)
        self.player.equip_weapon(Sword())
        self.player.level = self.level
        self.player.particles = self.particles

        self.wave_manager = WaveManager(self)
        self.particles.particles.clear()

    def draw(self):
        self.screen.fill(WHITE)
        # Draw ground
        pygame.draw.line(self.screen, BLACK, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)

        # Draw Level
        self.level.draw(self.screen)

        # Draw Particles (Behind entities?) or In front
        self.particles.draw(self.screen)

        # Draw Entities
        self.player.draw(self.screen)
        self.wave_manager.draw(self.screen)

        # UI
        self.ui.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()
