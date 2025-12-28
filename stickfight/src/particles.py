
import pygame
import random
import math
from stickfight.src.constants import *

class Particle:
    def __init__(self, x, y, dx, dy, life, color, size, gravity=0):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.life = life
        self.max_life = life
        self.color = color
        self.size = size
        self.gravity = gravity

    def update(self, dt):
        # Apply gravity
        self.dy += self.gravity * (dt / 16.0)

        # Move
        self.x += self.dx * (dt / 16.0)
        self.y += self.dy * (dt / 16.0)

        # Age
        self.life -= dt

    def draw(self, surface):
        if self.life <= 0:
            return

        # Fade out alpha
        alpha = int(255 * (self.life / self.max_life))

        # Since pygame drawing doesn't support alpha directly on primitives easily without surface,
        # we will simulate fading by shrinking or just disappearing.
        # For better performance, we'll just shrink.
        current_size = max(0, self.size * (self.life / self.max_life))

        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(current_size))

class ParticleManager:
    def __init__(self):
        self.particles = []

    def add_particle(self, p):
        self.particles.append(p)

    def create_blood(self, x, y, count=10):
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(1, 5)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            life = random.uniform(200, 500)
            size = random.uniform(2, 4)
            self.add_particle(Particle(x, y, dx, dy, life, RED, size, gravity=0.2))

    def create_dust(self, x, y, count=5):
        for _ in range(count):
            angle = random.uniform(math.pi, math.pi * 2) # Upwards
            speed = random.uniform(0.5, 2)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            life = random.uniform(100, 300)
            size = random.uniform(3, 6)
            self.add_particle(Particle(x, y, dx, dy, life, GRAY, size, gravity=-0.05))

    def create_spark(self, x, y, count=5):
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(3, 8)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            life = random.uniform(50, 150)
            size = random.uniform(1, 3)
            self.add_particle(Particle(x, y, dx, dy, life, (255, 255, 0), size, gravity=0))

    def update(self, dt):
        # Update all particles
        for p in self.particles:
            p.update(dt)

        # Remove dead particles
        self.particles = [p for p in self.particles if p.life > 0]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)
