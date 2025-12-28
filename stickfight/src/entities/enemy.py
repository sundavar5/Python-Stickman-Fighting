import pygame
import random
from entities.entity import Entity
from engine.settings import *

class Enemy(Entity):
    """
    Base class for enemies.
    """
    def __init__(self, x, y, width, height, physics_engine, tilemap):
        super().__init__(x, y, width, height)
        self.physics = physics_engine
        self.tilemap = tilemap
        self.color = RED
        self.tags.append('enemy')

        self.speed = 2
        self.direction = 1 # 1 or -1
        self.timer = 0
        self.move_duration = 100

    def update(self, dt):
        """Basic AI: Patrol back and forth."""
        self.timer += 1
        if self.timer > self.move_duration:
            self.direction *= -1
            self.timer = 0
            # Small chance to jump
            if random.random() < 0.3 and self.on_ground:
                self.vel[1] = -10

        self.vel[0] = self.speed * self.direction

        self.physics.apply_gravity(self)
        self.physics.check_collisions(self, self.tilemap)

        if self.rect.y > 2000:
            self.kill()

class StickmanEnemy(Enemy):
    """
    A standard stickman enemy.
    """
    def __init__(self, x, y, physics_engine, tilemap):
        super().__init__(x, y, 30, 50, physics_engine, tilemap)

    def draw(self, surface, camera_offset):
        # Draw "Stickman" details
        screen_x = self.rect.centerx - camera_offset[0]
        screen_y = self.rect.centery - camera_offset[1]

        # Head
        pygame.draw.circle(surface, self.color, (screen_x, screen_y - 15), 10)
        # Body
        pygame.draw.line(surface, self.color, (screen_x, screen_y - 5), (screen_x, screen_y + 15), 2)
        # Arms
        pygame.draw.line(surface, self.color, (screen_x - 10, screen_y), (screen_x + 10, screen_y), 2)
        # Legs
        pygame.draw.line(surface, self.color, (screen_x, screen_y + 15), (screen_x - 10, screen_y + 30), 2)
        pygame.draw.line(surface, self.color, (screen_x, screen_y + 15), (screen_x + 10, screen_y + 30), 2)

class SlimeEnemy(Enemy):
    """
    A slime enemy.
    """
    def __init__(self, x, y, physics_engine, tilemap):
        super().__init__(x, y, 40, 30, physics_engine, tilemap)
        self.color = GREEN
        self.speed = 1

    def draw(self, surface, camera_offset):
         super().draw(surface, camera_offset)
         # Just a box for now, maybe add eyes later
