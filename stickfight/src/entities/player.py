import pygame
from entities.entity import Entity
from engine.settings import *

class Player(Entity):
    """
    The main player class controlled by the user.
    """
    def __init__(self, x, y, input_manager, physics_engine, tilemap):
        super().__init__(x, y, 30, 50)
        self.input = input_manager
        self.physics = physics_engine
        self.tilemap = tilemap
        self.color = BLUE
        self.tags.append('player')

        # Stats
        self.speed = PLAYER_SPEED
        self.jump_force = PLAYER_JUMP_FORCE

        # Skills
        self.max_jumps = 1
        self.jumps_remaining = 0

        # Combat State
        self.attacking = False
        self.attack_cooldown = 0
        self.facing_right = True
        self.is_blocking = False

    def update(self, dt):
        """Processes input and physics for the player."""

        # Blocking
        self.is_blocking = self.input.is_key_down(pygame.K_LSHIFT) or self.input.is_key_down(pygame.K_s)
        if self.is_blocking:
            self.vel[0] *= 0.5 # Move slower while blocking

        # Horizontal Movement
        if self.input.is_key_down(pygame.K_LEFT) or self.input.is_key_down(pygame.K_a):
            self.vel[0] = -self.speed
            self.facing_right = False
        elif self.input.is_key_down(pygame.K_RIGHT) or self.input.is_key_down(pygame.K_d):
            self.vel[0] = self.speed
            self.facing_right = True
        else:
            self.physics.apply_friction(self)

        # Jumping
        if self.on_ground:
            self.jumps_remaining = self.max_jumps

        if (self.input.is_key_just_pressed(pygame.K_SPACE) or self.input.is_key_just_pressed(pygame.K_w) or self.input.is_key_just_pressed(pygame.K_UP)):
            if self.jumps_remaining > 0:
                self.vel[1] = -self.jump_force
                self.jumps_remaining -= 1
                self.on_ground = False

        # Apply Physics
        self.physics.apply_gravity(self)
        self.physics.check_collisions(self, self.tilemap)

        # Bounds checking (prevent falling indefinitely)
        if self.rect.y > 2000:
            self.rect.y = 0
            self.vel = [0, 0]

    def draw(self, surface, camera_offset):
        super().draw(surface, camera_offset)

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
