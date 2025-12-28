import pygame
import random
from engine.settings import *

class TileMap:
    """
    Manages the game world map using a grid of tiles.
    Handles map generation, rendering, and collision data.
    """
    def __init__(self, width=100, height=50):
        self.width = width
        self.height = height
        self.tile_size = TILE_SIZE
        self.tiles = {}  # Dictionary to store tile data: (x, y) -> tile_type
        self.generate_map()

    def generate_map(self):
        """Generates a simple procedural map."""
        print("Generating map...")
        # Create a floor
        for x in range(self.width):
            self.tiles[(x, self.height - 1)] = 'grass'
            self.tiles[(x, self.height - 2)] = 'dirt'

        # Create some platforms
        for _ in range(20):
            w = random.randint(3, 8)
            x = random.randint(5, self.width - 5)
            y = random.randint(self.height - 15, self.height - 5)
            for i in range(w):
                self.tiles[(x + i, y)] = 'stone'

        # Create some walls
        for _ in range(5):
             h = random.randint(3, 10)
             x = random.randint(5, self.width - 5)
             y = self.height - 2
             for i in range(h):
                 self.tiles[(x, y - i)] = 'stone'

    def get_tile(self, x, y):
        """Gets the tile type at grid coordinates."""
        return self.tiles.get((x, y))

    def get_tiles_around(self, pos):
        """
        Returns a list of tiles surrounding a world position (pixel coords).
        Used for collision detection optimization.
        """
        rects = []
        grid_x = int(pos[0] // self.tile_size)
        grid_y = int(pos[1] // self.tile_size)

        for y in range(grid_y - 2, grid_y + 3):
            for x in range(grid_x - 2, grid_x + 3):
                tile = self.tiles.get((x, y))
                if tile:
                    rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                    rects.append(rect)
        return rects

    def draw(self, surface, camera_offset):
        """Draws visible tiles to the surface."""
        # Simple culling could be added here
        for (x, y), tile_type in self.tiles.items():
            screen_x = x * self.tile_size - camera_offset[0]
            screen_y = y * self.tile_size - camera_offset[1]

            # Draw only if on screen
            if -self.tile_size < screen_x < SCREEN_WIDTH and -self.tile_size < screen_y < SCREEN_HEIGHT:
                color = GREEN
                if tile_type == 'dirt':
                    color = (139, 69, 19)
                elif tile_type == 'stone':
                    color = GRAY

                rect = pygame.Rect(screen_x, screen_y, self.tile_size, self.tile_size)
                pygame.draw.rect(surface, color, rect)
                # Optional: Draw border
                pygame.draw.rect(surface, BLACK, rect, 1)
