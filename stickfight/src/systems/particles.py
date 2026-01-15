import pygame
import random
import math

class Particle:
    def __init__(self, x, y, velocity, color, life, size, gravity=0, friction=0.95):
        self.x = x
        self.y = y
        self.vel = list(velocity)
        self.color = color
        self.life = life
        self.max_life = life
        self.size = size
        self.gravity = gravity
        self.friction = friction

    def update(self):
        self.vel[0] *= self.friction
        self.vel[1] *= self.friction
        self.vel[1] += self.gravity

        self.x += self.vel[0]
        self.y += self.vel[1]
        self.life -= 1
        self.size *= 0.95 # Shrink over time

    def draw(self, surface, camera_offset):
        if self.life > 0:
            screen_x = self.x - camera_offset[0]
            screen_y = self.y - camera_offset[1]
            if self.size > 1:
                pygame.draw.circle(surface, self.color, (int(screen_x), int(screen_y)), int(self.size))
            else:
                surface.set_at((int(screen_x), int(screen_y)), self.color)

class TextParticle(Particle):
    def __init__(self, x, y, text, color, font):
        super().__init__(x, y, (0, -2), color, 60, 10, gravity=0.1)
        self.text = text
        self.font = font

    def update(self):
        super().update()
        # Text doesn't shrink, maybe fade out?

    def draw(self, surface, camera_offset):
        if self.life > 0 and self.font:
            screen_x = self.x - camera_offset[0]
            screen_y = self.y - camera_offset[1]
            # Fade alpha
            alpha = min(255, int(255 * (self.life / self.max_life)))
            text_surf = self.font.render(str(self.text), True, self.color)
            text_surf.set_alpha(alpha)
            surface.blit(text_surf, (screen_x, screen_y))

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_particle(self, particle):
        self.particles.append(particle)

    def create_blood(self, x, y, amount=10):
        for _ in range(amount):
            angle = random.uniform(0, 6.28)
            speed = random.uniform(2, 6)
            vel = [math.cos(angle) * speed, math.sin(angle) * speed]
            self.particles.append(Particle(x, y, vel, (200, 0, 0), random.randint(20, 40), random.randint(2, 4), gravity=0.5))

    def create_dust(self, x, y, amount=5):
        for _ in range(amount):
            vel = [random.uniform(-1, 1), random.uniform(-2, 0)]
            self.particles.append(Particle(x, y, vel, (200, 200, 200), random.randint(20, 50), random.randint(3, 6), gravity=-0.05))

    def create_hit_spark(self, x, y):
         for _ in range(5):
            vel = [random.uniform(-5, 5), random.uniform(-5, 5)]
            self.particles.append(Particle(x, y, vel, (255, 255, 0), random.randint(5, 15), 2))

    def create_text(self, x, y, text, color, font):
        self.particles.append(TextParticle(x, y, text, color, font))

    def update(self):
        self.particles = [p for p in self.particles if p.life > 0]
        for p in self.particles:
            p.update()

    def draw(self, surface, camera_offset):
        for p in self.particles:
            p.draw(surface, camera_offset)
