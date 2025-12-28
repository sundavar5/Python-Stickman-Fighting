import pygame

class Entity:
    """
    Base class for all interactive objects in the game world.
    """
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.vel = [0, 0] # [x, y]
        self.on_ground = False
        self.is_active = True
        self.color = (255, 255, 255) # Default white

        # Tags for identification
        self.tags = []

    def update(self, dt):
        """Update logic for the entity."""
        pass

    def draw(self, surface, camera_offset):
        """Draws the entity rectangle."""
        screen_x = self.rect.x - camera_offset[0]
        screen_y = self.rect.y - camera_offset[1]

        # Draw placeholder rect
        pygame.draw.rect(surface, self.color, (screen_x, screen_y, self.rect.width, self.rect.height))

    def kill(self):
        """Marks the entity for removal."""
        self.is_active = False
