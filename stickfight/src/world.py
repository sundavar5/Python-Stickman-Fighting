
import pygame
from stickfight.src.constants import *

class Platform:
    def __init__(self, x, y, width, height, color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class MovingPlatform(Platform):
    def __init__(self, x, y, width, height, end_x, end_y, speed):
        super().__init__(x, y, width, height, BLUE)
        self.start_pos = pygame.Vector2(x, y)
        self.end_pos = pygame.Vector2(end_x, end_y)
        self.speed = speed
        self.direction = 1
        self.position = pygame.Vector2(x, y)

    def update(self, dt):
        move = self.end_pos - self.start_pos
        length = move.length()
        if length == 0: return

        move.normalize_ip()
        self.position += move * self.direction * self.speed * (dt / 16.0)

        # Check bounds (simple toggle)
        dist_start = self.position.distance_to(self.start_pos)
        dist_end = self.position.distance_to(self.end_pos)

        if self.direction == 1 and dist_start >= length:
            self.direction = -1
        elif self.direction == -1 and dist_end >= length:
            self.direction = 1

        self.rect.x = int(self.position.x)
        self.rect.y = int(self.position.y)

class Level:
    def __init__(self):
        self.platforms = []

    def add_platform(self, p):
        self.platforms.append(p)

    def draw(self, surface):
        for p in self.platforms:
            p.draw(surface)

    def update(self, dt):
        for p in self.platforms:
            if hasattr(p, 'update'):
                p.update(dt)

def load_test_level():
    lvl = Level()
    # Main ground (split to allow falling off edges?)
    # For now, just platforms above the ground constant

    lvl.add_platform(Platform(300, 450, 200, 20))
    lvl.add_platform(Platform(700, 350, 200, 20))
    lvl.add_platform(Platform(100, 250, 150, 20))

    lvl.add_platform(MovingPlatform(500, 200, 100, 20, 500, 500, 2))

    return lvl
