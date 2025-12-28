
import pygame
import math
from stickfight.src.constants import *

class SpellType:
    PROJECTILE = "projectile"
    SELF_BUFF = "self_buff"
    AOE = "aoe"

class Spell:
    def __init__(self, name, mana_cost, cooldown, s_type, damage=0, effect_func=None):
        self.name = name
        self.mana_cost = mana_cost
        self.cooldown = cooldown # in ms
        self.type = s_type
        self.damage = damage
        self.effect_func = effect_func # Custom logic
        self.last_cast_time = -cooldown # Allow immediate cast

    def can_cast(self, caster, current_time):
        if caster.mana < self.mana_cost:
            return False
        if current_time - self.last_cast_time < self.cooldown:
            return False
        return True

    def cast(self, caster, target_pos, current_time, game_context):
        self.last_cast_time = current_time
        caster.mana -= self.mana_cost

        if self.type == SpellType.PROJECTILE:
            # Calculate direction
            start_pos = pygame.Vector2(caster.position.x, caster.position.y - 30)
            direction = pygame.Vector2(target_pos) - start_pos
            if direction.length() > 0:
                direction.normalize_ip()

            proj = Projectile(start_pos.x, start_pos.y, direction, self.damage, caster)
            game_context.projectiles.append(proj)

        elif self.type == SpellType.SELF_BUFF:
             if self.effect_func:
                 self.effect_func(caster)

class Projectile:
    def __init__(self, x, y, direction, damage, owner):
        self.position = pygame.Vector2(x, y)
        self.direction = direction
        self.damage = damage
        self.owner = owner
        self.speed = 10
        self.radius = 5
        self.color = BLUE
        self.life = 2000 # ms

    def update(self, dt):
        self.position += self.direction * self.speed * (dt / 16.0)
        self.life -= dt

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.position.x), int(self.position.y)), self.radius)

class SpellBook:
    def __init__(self):
        self.spells = []
        self.active_spell_index = 0

    def add_spell(self, spell):
        self.spells.append(spell)

    def get_active(self):
        if not self.spells: return None
        return self.spells[self.active_spell_index]

    def cycle(self):
        if not self.spells: return
        self.active_spell_index = (self.active_spell_index + 1) % len(self.spells)
