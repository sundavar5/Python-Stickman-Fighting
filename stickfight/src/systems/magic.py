import pygame
import math

class Projectile:
    def __init__(self, x, y, angle, speed, damage, color, life=60, owner=None):
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.damage = damage
        self.color = color
        self.life = life
        self.owner = owner
        self.rect = pygame.Rect(x, y, 10, 10)
        self.active = True

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.life -= 1
        if self.life <= 0:
            self.active = False

    def draw(self, surface, camera_offset):
        screen_x = self.rect.x - camera_offset[0]
        screen_y = self.rect.y - camera_offset[1]
        pygame.draw.circle(surface, self.color, (screen_x + 5, screen_y + 5), 5)

class MagicSystem:
    def __init__(self, particle_system):
        self.projectiles = []
        self.particles = particle_system

    def cast_fireball(self, caster):
        if not hasattr(caster, 'stats') or caster.stats.current_mana < 10:
            print("Not enough mana!")
            return False

        caster.stats.use_mana(10)

        # Determine angle
        angle = 0 if caster.facing_right else 3.14159

        # Create projectile
        proj = Projectile(caster.rect.centerx, caster.rect.centery, angle, 10, 25, (255, 100, 0), owner=caster)
        self.projectiles.append(proj)

        # Visuals
        self.particles.create_hit_spark(caster.rect.centerx, caster.rect.centery)
        print(f"{caster} cast Fireball!")
        return True

    def update(self, dt, tilemap, entities):
        for p in self.projectiles:
            p.update()

            # Collision with walls
            if tilemap.get_tile(int(p.x // tilemap.tile_size), int(p.y // tilemap.tile_size)):
                p.active = False
                self.particles.create_dust(p.x, p.y)
                continue

            # Collision with entities
            for ent in entities:
                if ent == p.owner or not ent.is_active:
                    continue

                # Team check
                if 'player' in p.owner.tags and 'player' in ent.tags: continue
                if 'enemy' in p.owner.tags and 'enemy' in ent.tags: continue

                if p.rect.colliderect(ent.rect):
                    p.active = False
                    if hasattr(ent, 'stats'):
                        ent.stats.take_damage(p.damage)
                        self.particles.create_text(ent.rect.centerx, ent.rect.top, f"-{p.damage}", (255, 100, 0), None)
                    break

        self.projectiles = [p for p in self.projectiles if p.active]

    def draw(self, surface, camera_offset):
        for p in self.projectiles:
            p.draw(surface, camera_offset)
