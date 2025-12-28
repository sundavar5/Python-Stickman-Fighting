import pygame
from engine.settings import GRAVITY, FRICTION

class PhysicsEngine:
    """
    Handles physics calculations, collision detection, and resolution.
    """
    def __init__(self):
        pass

    def apply_gravity(self, entity):
        """Applies gravity to an entity's vertical velocity."""
        entity.vel[1] += GRAVITY

    def apply_friction(self, entity):
        """Applies horizontal friction."""
        entity.vel[0] *= (1 + FRICTION) # Simple damping
        if abs(entity.vel[0]) < 0.1:
            entity.vel[0] = 0

    def check_collisions(self, entity, tilemap):
        """
        Checks and resolves collisions for an entity against the tilemap.
        Updates entity position and velocity directly.
        """
        # Horizontal movement
        entity.rect.x += entity.vel[0]
        hits = tilemap.get_tiles_around(entity.rect.center)

        for tile_rect in hits:
            if entity.rect.colliderect(tile_rect):
                if entity.vel[0] > 0: # Moving right
                    entity.rect.right = tile_rect.left
                elif entity.vel[0] < 0: # Moving left
                    entity.rect.left = tile_rect.right
                entity.vel[0] = 0

        # Vertical movement
        entity.rect.y += entity.vel[1]
        hits = tilemap.get_tiles_around(entity.rect.center)

        entity.on_ground = False
        for tile_rect in hits:
            if entity.rect.colliderect(tile_rect):
                if entity.vel[1] > 0: # Falling down
                    entity.rect.bottom = tile_rect.top
                    entity.on_ground = True
                    entity.vel[1] = 0
                elif entity.vel[1] < 0: # Jumping up
                    entity.rect.top = tile_rect.bottom
                    entity.vel[1] = 0
