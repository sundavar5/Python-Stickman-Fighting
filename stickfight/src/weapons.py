
import pygame
import math
from stickfight.src.constants import *

class WeaponType:
    FIST = "fist"
    SWORD = "sword"
    SPEAR = "spear"
    AXE = "axe"

class Weapon:
    def __init__(self, name, w_type, damage, range_val, speed, color):
        self.name = name
        self.type = w_type
        self.damage = damage
        self.range = range_val
        self.speed = speed # Multiplier for attack duration (lower is faster)
        self.color = color

    def draw(self, surface, x, y, angle, facing_right):
        pass

class Sword(Weapon):
    def __init__(self):
        super().__init__("Sword", WeaponType.SWORD, 15, 80, 1.0, (100, 100, 100))

    def draw(self, surface, x, y, angle, facing_right):
        # Draw a line extending from hand
        rad = math.radians(angle)

        # Hand pos (x,y)
        blade_len = 40
        handle_len = 10

        # If facing left, flip angle logic handled by caller usually, but let's see
        # Caller passes angle which is already flipped?

        end_x = x + math.sin(rad) * blade_len
        end_y = y + math.cos(rad) * blade_len

        handle_x = x - math.sin(rad) * handle_len
        handle_y = y - math.cos(rad) * handle_len

        pygame.draw.line(surface, self.color, (handle_x, handle_y), (end_x, end_y), 4)

        # Crossguard
        cross_x = x
        cross_y = y
        perp_rad = rad + math.pi/2
        cw = 10
        p1 = (cross_x + math.sin(perp_rad)*cw, cross_y + math.cos(perp_rad)*cw)
        p2 = (cross_x - math.sin(perp_rad)*cw, cross_y - math.cos(perp_rad)*cw)
        pygame.draw.line(surface, BLACK, p1, p2, 2)

class Spear(Weapon):
    def __init__(self):
        super().__init__("Spear", WeaponType.SPEAR, 10, 120, 1.2, (139, 69, 19))

    def draw(self, surface, x, y, angle, facing_right):
        rad = math.radians(angle)
        length = 80

        end_x = x + math.sin(rad) * length
        end_y = y + math.cos(rad) * length

        back_x = x - math.sin(rad) * 20
        back_y = y - math.cos(rad) * 20

        pygame.draw.line(surface, self.color, (back_x, back_y), (end_x, end_y), 3)

        # Tip
        pygame.draw.circle(surface, GRAY, (int(end_x), int(end_y)), 4)

class Axe(Weapon):
    def __init__(self):
        super().__init__("Battle Axe", WeaponType.AXE, 25, 70, 1.5, GRAY)

    def draw(self, surface, x, y, angle, facing_right):
        rad = math.radians(angle)
        length = 50

        end_x = x + math.sin(rad) * length
        end_y = y + math.cos(rad) * length

        pygame.draw.line(surface, (100, 50, 0), (x, y), (end_x, end_y), 4)

        # Head
        pygame.draw.circle(surface, self.color, (int(end_x), int(end_y)), 15)

class Fists(Weapon):
    def __init__(self):
        super().__init__("Fists", WeaponType.FIST, 5, 50, 0.8, BLACK)

    def draw(self, surface, x, y, angle, facing_right):
        # Just a larger hand circle maybe?
        pass
