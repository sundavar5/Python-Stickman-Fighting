import pygame
import random
from engine.settings import *

class CombatSystem:
    """
    Handles combat logic like attacking, hitboxes, and damage dealing.
    """
    def __init__(self, particle_system, asset_manager, quest_manager=None):
        self.particles = particle_system
        self.assets = asset_manager
        self.quests = quest_manager

    def perform_attack(self, attacker, targets):
        """
        Executes an attack from an attacker against a list of potential targets.
        Returns a list of hit entities.
        """
        hit_entities = []

        # Determine hitbox based on attacker facing direction
        attack_range = 40 # Default range
        damage = 10 # Default damage
        knockback_force = 5

        # Check for weapon
        if hasattr(attacker, 'inventory') and attacker.inventory:
            # Simplification: assume weapon is equipped or first item is weapon
            # In a real system we'd check attacker.equipment['main_hand']
            pass

        attack_rect = pygame.Rect(0, 0, attack_range, attacker.rect.height)
        if hasattr(attacker, 'facing_right') and attacker.facing_right:
            attack_rect.midleft = attacker.rect.center
        else:
            attack_rect.midright = attacker.rect.center

        for target in targets:
            if target == attacker:
                continue

            # Team Check
            if 'player' in attacker.tags and 'player' in target.tags:
                continue
            if 'enemy' in attacker.tags and 'enemy' in target.tags:
                continue

            if attack_rect.colliderect(target.rect):
                # Defense Check (Blocking)
                blocked = False
                if hasattr(target, 'is_blocking') and target.is_blocking:
                    # Check facing
                    if (attacker.rect.centerx < target.rect.centerx and not target.facing_right) or \
                       (attacker.rect.centerx > target.rect.centerx and target.facing_right):
                        blocked = True

                if blocked:
                    print(f"{target} blocked attack from {attacker}!")
                    self.particles.create_hit_spark(target.rect.centerx, target.rect.centery)
                    # Reduced damage or 0 damage
                    actual_damage = int(damage * 0.1)
                else:
                    # Critical hit chance
                    is_crit = random.random() < 0.1
                    if is_crit:
                        damage *= 2
                        print("CRITICAL HIT!")

                    actual_damage = damage

                    # Apply damage
                    if hasattr(target, 'stats'):
                        target.stats.take_damage(actual_damage)

                        # Death check
                        if target.stats.current_hp <= 0:
                            target.kill()
                            # XP Reward
                            if hasattr(attacker, 'stats'):
                                attacker.stats.gain_xp(20)

                            # Quest Progress
                            if self.quests and hasattr(attacker, 'tags') and 'player' in attacker.tags:
                                if 'enemy' in target.tags:
                                    if isinstance(target.__class__.__name__, str):
                                        enemy_name = target.__class__.__name__.lower()
                                        if "stickman" in enemy_name:
                                            self.quests.on_enemy_killed("stickman")
                                        elif "slime" in enemy_name:
                                            self.quests.on_enemy_killed("slime")

                    # Visuals
                    self.particles.create_blood(target.rect.centerx, target.rect.centery)
                    color = (255, 0, 0) if is_crit else (255, 255, 255)
                    font = self.assets.get_font('default')
                    self.particles.create_text(target.rect.centerx, target.rect.top - 20, f"-{actual_damage}", color, font)

                    # Knockback
                    if attacker.rect.centerx < target.rect.centerx:
                        target.vel[0] = knockback_force
                    else:
                        target.vel[0] = -knockback_force
                    target.vel[1] = -3

                hit_entities.append(target)
                print(f"{attacker} hit {target} for {actual_damage} damage!")

        return hit_entities

    def draw_attack_debug(self, surface, attacker, camera_offset):
        """Debug helper to draw attack hitboxes."""
        attack_range = 40
        attack_rect = pygame.Rect(0, 0, attack_range, attacker.rect.height)
        if hasattr(attacker, 'facing_right') and attacker.facing_right:
            attack_rect.midleft = attacker.rect.center
        else:
            attack_rect.midright = attacker.rect.center

        screen_x = attack_rect.x - camera_offset[0]
        screen_y = attack_rect.y - camera_offset[1]

        pygame.draw.rect(surface, (255, 0, 0), (screen_x, screen_y, attack_rect.width, attack_rect.height), 1)
