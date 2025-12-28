import pygame

class CombatSystem:
    """
    Handles combat logic like attacking, hitboxes, and damage dealing.
    """
    def __init__(self):
        pass

    def perform_attack(self, attacker, targets):
        """
        Executes an attack from an attacker against a list of potential targets.
        Returns a list of hit entities.
        """
        hit_entities = []

        # Determine hitbox based on attacker facing direction
        attack_range = 40 # Default range
        # If attacker has a weapon, use its range (mock logic for now)

        attack_rect = pygame.Rect(0, 0, attack_range, attacker.rect.height)
        if hasattr(attacker, 'facing_right') and attacker.facing_right:
            attack_rect.midleft = attacker.rect.center
        else:
            attack_rect.midright = attacker.rect.center

        for target in targets:
            if target == attacker:
                continue

            # Simple team check based on tags
            if 'player' in attacker.tags and 'player' in target.tags:
                continue
            if 'enemy' in attacker.tags and 'enemy' in target.tags:
                continue

            if attack_rect.colliderect(target.rect):
                damage = 10 # Default damage
                # Calculate damage based on stats/equipment

                # Apply damage (mock logic if stats component exists)
                if hasattr(target, 'stats'):
                    target.stats.take_damage(damage)

                # Knockback
                knockback_force = 5
                if attacker.rect.centerx < target.rect.centerx:
                    target.vel[0] = knockback_force
                else:
                    target.vel[0] = -knockback_force
                target.vel[1] = -2 # Slight lift

                hit_entities.append(target)
                print(f"{attacker} hit {target} for {damage} damage!")

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
