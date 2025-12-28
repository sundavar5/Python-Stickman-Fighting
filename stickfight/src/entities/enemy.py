import pygame
import random
import math
from entities.entity import Entity
from engine.settings import *

class Enemy(Entity):
    """
    Base class for enemies with State Machine AI.
    States: IDLE, PATROL, CHASE, ATTACK, FLEE
    """
    def __init__(self, x, y, width, height, physics_engine, tilemap):
        super().__init__(x, y, width, height)
        self.physics = physics_engine
        self.tilemap = tilemap
        self.color = RED
        self.tags.append('enemy')

        self.speed = 2
        self.direction = 1
        self.state = "PATROL"
        self.timer = 0
        self.target = None # Reference to player

    def update(self, dt):
        self.ai_behavior(dt)
        self.physics.apply_gravity(self)
        self.physics.check_collisions(self, self.tilemap)

        if self.rect.y > 2000:
            self.kill()

    def ai_behavior(self, dt):
        """State Machine Logic"""
        if self.state == "PATROL":
            self.timer += 1
            self.vel[0] = self.speed * self.direction

            if self.timer > 100:
                self.timer = 0
                self.direction *= -1
                self.state = "IDLE"

        elif self.state == "IDLE":
            self.vel[0] = 0
            self.timer += 1
            if self.timer > 60:
                self.timer = 0
                self.state = "PATROL"

        elif self.state == "CHASE":
            if self.target:
                dist = self.target.rect.centerx - self.rect.centerx
                if abs(dist) > 5:
                    self.direction = 1 if dist > 0 else -1
                    self.vel[0] = self.speed * 1.5 * self.direction
                else:
                    self.vel[0] = 0

class FlyingEnemy(Enemy):
    """
    Bat-like enemy that ignores gravity.
    """
    def __init__(self, x, y, physics_engine, tilemap):
        super().__init__(x, y, 30, 30, physics_engine, tilemap)
        self.color = (100, 0, 255)
        self.start_y = y
        self.offset = 0

    def update(self, dt):
        # Sine wave movement
        self.offset += 0.1
        self.vel[1] = math.sin(self.offset) * 2
        self.vel[0] = self.speed * self.direction

        # Simple bounce back and forth
        self.timer += 1
        if self.timer > 100:
            self.direction *= -1
            self.timer = 0

        # No gravity for flying units, just update pos
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]

class StickmanEnemy(Enemy):
    def __init__(self, x, y, physics_engine, tilemap):
        super().__init__(x, y, 30, 50, physics_engine, tilemap)

    def draw(self, surface, camera_offset):
        screen_x = self.rect.centerx - camera_offset[0]
        screen_y = self.rect.centery - camera_offset[1]
        pygame.draw.circle(surface, self.color, (screen_x, screen_y - 15), 10)
        pygame.draw.line(surface, self.color, (screen_x, screen_y - 5), (screen_x, screen_y + 15), 2)
        pygame.draw.line(surface, self.color, (screen_x - 10, screen_y), (screen_x + 10, screen_y), 2)
        pygame.draw.line(surface, self.color, (screen_x, screen_y + 15), (screen_x - 10, screen_y + 30), 2)
        pygame.draw.line(surface, self.color, (screen_x, screen_y + 15), (screen_x + 10, screen_y + 30), 2)

class SlimeEnemy(Enemy):
    def __init__(self, x, y, physics_engine, tilemap):
        super().__init__(x, y, 40, 30, physics_engine, tilemap)
        self.color = GREEN
        self.speed = 1
