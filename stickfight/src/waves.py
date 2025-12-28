
import pygame
import random
from stickfight.src.entities import Stickman
from stickfight.src.ai import AIController
from stickfight.src.weapons import Sword, Spear, Axe, Fists
from stickfight.src.constants import *

class WaveManager:
    def __init__(self, game):
        self.game = game
        self.wave_number = 0
        self.enemies = []
        self.wave_timer = 0
        self.in_wave = False

    def start_next_wave(self):
        self.wave_number += 1
        self.in_wave = True
        self.spawn_wave()

    def spawn_wave(self):
        count = 1 + (self.wave_number // 2)
        print(f"Spawning Wave {self.wave_number} with {count} enemies")

        for i in range(count):
            # Random position (spawn from right side mostly)
            spawn_x = random.randint(800, 1200)
            spawn_y = GROUND_Y

            # 20% chance to spawn on a platform if level exists
            if self.game.level and random.random() < 0.2:
                if self.game.level.platforms:
                    plat = random.choice(self.game.level.platforms)
                    spawn_x = plat.rect.centerx
                    spawn_y = plat.rect.top

            enemy = Stickman(spawn_x, spawn_y, color=RED)
            enemy.level = self.game.level
            enemy.particles = self.game.particles

            # Random Weapon
            w_choice = random.choice([Sword, Spear, Axe, Fists])
            enemy.equip_weapon(w_choice())

            # Slightly random stats based on weapon?
            if isinstance(enemy.weapon, Axe):
                enemy.max_health = 150
                enemy.health = 150
            elif isinstance(enemy.weapon, Spear):
                pass

            self.enemies.append({
                'entity': enemy,
                'ai': AIController(enemy, self.game.player)
            })

    def update(self, dt):
        if not self.in_wave:
            # Check if we should start
            # For now, auto start next wave immediately if no enemies
            if len(self.enemies) == 0:
                self.start_next_wave()

        # Update enemies
        dead_indices = []
        for i, data in enumerate(self.enemies):
            entity = data['entity']
            ai = data['ai']

            entity.update(dt)
            ai.update()

            # Check death
            if entity.health <= 0:
                dead_indices.append(i)
                # Particles?

        # Remove dead
        for i in sorted(dead_indices, reverse=True):
            self.enemies.pop(i)

        if self.in_wave and len(self.enemies) == 0:
            self.in_wave = False

    def draw(self, surface):
        for data in self.enemies:
            data['entity'].draw(surface)
