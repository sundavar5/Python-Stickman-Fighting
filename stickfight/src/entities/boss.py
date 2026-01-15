import pygame
import random
from entities.entity import Entity
from engine.settings import *

class Boss(Entity):
    """
    Boss entity with multiple phases and higher stats.
    """
    def __init__(self, x, y, name, physics_engine, tilemap, particle_system):
        super().__init__(x, y, 60, 100) # Larger size
        self.physics = physics_engine
        self.tilemap = tilemap
        self.particles = particle_system
        self.name = name
        self.color = (139, 0, 0) # Dark Red
        self.tags.append('enemy')
        self.tags.append('boss')

        # Logic
        self.speed = 3
        self.direction = 1
        self.state = "IDLE"
        self.timer = 0
        self.target = None
        self.phase = 1

    def update(self, dt):
        if self.state == "IDLE":
            self.timer += 1
            if self.timer > 60:
                self.state = "PATROL"
                self.timer = 0

        elif self.state == "PATROL":
            self.vel[0] = self.speed * self.direction
            self.timer += 1
            if self.timer > 120:
                self.direction *= -1
                self.timer = 0
                self.state = "IDLE"

            # Simple aggro check (mock)
            # if distance to player < 300: self.state = "CHASE"

        elif self.state == "CHASE":
            # Logic to follow player would go here
            pass

        elif self.state == "ATTACK":
            pass

        self.physics.apply_gravity(self)
        self.physics.check_collisions(self, self.tilemap)

        # Boss ability: Stomp
        if self.on_ground and random.random() < 0.01:
            self.vel[1] = -15 # Big jump
            self.particles.create_dust(self.rect.centerx, self.rect.bottom, 20)

    def draw(self, surface, camera_offset):
        super().draw(surface, camera_offset)
        # Draw Name
        # (Simplified)
