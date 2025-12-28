import pygame
import math
from stickfight.src.constants import *
from stickfight.src.physics import Vector2
from stickfight.src.animation import AnimationController, AnimationState

class Stickman:
    def __init__(self, x, y, color=BLACK):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.color = color
        self.facing_right = True
        self.on_ground = False
        self.health = 100
        self.is_attacking = False
        self.has_hit = False

        # Animation
        self.animator = AnimationController()

    def update(self, dt=16):
        # Apply Gravity
        self.velocity.y += GRAVITY

        # Apply Friction
        self.velocity.x *= FRICTION

        # Move
        self.position += self.velocity

        # Ground Collision
        if self.position.y > GROUND_Y:
            self.position.y = GROUND_Y
            self.velocity.y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        # Update Animation State
        if self.is_attacking:
            self.animator.state = AnimationState.ATTACK
            # Check for attack end
            if self.animator.timer > 300: # 300ms attack
                self.is_attacking = False
        elif not self.on_ground:
            self.animator.state = AnimationState.JUMP
        elif abs(self.velocity.x) > 0.5:
            self.animator.state = AnimationState.RUN
        else:
            self.animator.state = AnimationState.IDLE

        self.animator.update(dt)

    def attack(self):
        if not self.is_attacking:
            self.is_attacking = True
            self.has_hit = False
            self.animator.timer = 0

    def check_hit(self, target):
        if not self.is_attacking:
            return False

        if self.has_hit:
            return False

        # Simple distance check for now
        # Ideally we check hitbox of fist/sword
        dist = self.position.distance_to(target.position)
        if dist < 60: # Range
            # Facing check
            if (self.facing_right and target.position.x > self.position.x) or \
               (not self.facing_right and target.position.x < self.position.x):
                self.has_hit = True
                return True
        return False

    def take_damage(self, amount):
        self.health -= amount
        # Knockback
        self.velocity.x = -5 if self.facing_right else 5
        self.velocity.y = -5

    def _draw_limb(self, surface, start_pos, angle, length, color, thickness=2):
        rad = math.radians(angle)
        # Flip angle if facing left
        if not self.facing_right:
            rad = math.radians(180 - angle)

        end_x = start_pos[0] + math.sin(rad) * length
        end_y = start_pos[1] + math.cos(rad) * length
        pygame.draw.line(surface, color, start_pos, (end_x, end_y), thickness)
        return (end_x, end_y)

    def draw(self, surface):
        x, y = self.position.x, self.position.y

        # Get Animation Offsets
        # (l_arm, r_arm, l_leg, r_leg, bounce)
        anim_data = self.animator.get_offsets(self.animator.state, self.animator.timer)
        bounce = anim_data[4]

        # Adjust Y for bounce
        y += bounce

        # Skeleton positions
        pelvis_pos = (x, y - LEG_LENGTH)
        neck_pos = (x, pelvis_pos[1] - BODY_LENGTH)
        shoulder_pos = (x, neck_pos[1] + 10)

        # Draw Legs
        # Base angles: 20 degrees out
        self._draw_limb(surface, pelvis_pos, 20 + anim_data[3], LEG_LENGTH, self.color) # Right Leg
        self._draw_limb(surface, pelvis_pos, -20 + anim_data[2], LEG_LENGTH, self.color) # Left Leg

        # Torso
        pygame.draw.line(surface, self.color, neck_pos, pelvis_pos, 2)

        # Head
        pygame.draw.circle(surface, self.color, (int(neck_pos[0]), int(neck_pos[1] - HEAD_RADIUS)), HEAD_RADIUS, 2)

        # Draw Arms
        # Base angles: 30 degrees out
        self._draw_limb(surface, shoulder_pos, 30 + anim_data[1], ARM_LENGTH, self.color) # Right Arm
        self._draw_limb(surface, shoulder_pos, -30 + anim_data[0], ARM_LENGTH, self.color) # Left Arm

    def move(self, direction):
        self.velocity.x += direction * MOVE_SPEED * 0.2
        if direction > 0:
            self.facing_right = True
        elif direction < 0:
            self.facing_right = False

    def jump(self):
        if self.on_ground:
            self.velocity.y = JUMP_FORCE
            self.on_ground = False
