import pygame

class Interactable:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.active = True

    def interact(self, player):
        pass

    def draw(self, surface, camera_offset):
        pass

class Chest(Interactable):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 32)
        self.opened = False
        self.color = (139, 69, 19) # Brown

    def interact(self, player):
        if not self.opened:
            self.opened = True
            print("Chest opened! Found Gold.")
            # Give loot (mock)
            if hasattr(player, 'stats'):
                player.stats.gain_xp(50)
            return True
        return False

    def draw(self, surface, camera_offset):
        screen_x = self.rect.x - camera_offset[0]
        screen_y = self.rect.y - camera_offset[1]
        color = (255, 215, 0) if self.opened else self.color
        pygame.draw.rect(surface, color, (screen_x, screen_y, 32, 32))

class Door(Interactable):
    def __init__(self, x, y, destination_map=None):
        super().__init__(x, y, 32, 64)
        self.destination = destination_map

    def interact(self, player):
        print("Interacting with door...")
        if self.destination:
            print(f"Travel to {self.destination}")
            # Logic to switch maps would go here
        return True

    def draw(self, surface, camera_offset):
        screen_x = self.rect.x - camera_offset[0]
        screen_y = self.rect.y - camera_offset[1]
        pygame.draw.rect(surface, (100, 50, 0), (screen_x, screen_y, 32, 64))
