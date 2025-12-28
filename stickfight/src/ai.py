
import random
import pygame
import random
import pygame
from stickfight.src.entities import Stickman
from stickfight.src.magic import SpellType

class AIState:
    IDLE = 0
    CHASE = 1
    ATTACK = 2
    RETREAT = 3

class AIController:
    def __init__(self, entity, target, game_context=None):
        self.entity = entity
        self.target = target
        self.game_context = game_context
        self.state = AIState.IDLE
        self.timer = 0
        self.reaction_time = 200 # ms
        self.last_reaction = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        dist = self.entity.position.distance_to(self.target.position)

        # Decide state
        if current_time - self.last_reaction > self.reaction_time:
            self.last_reaction = current_time
            if dist < 50:
                self.state = AIState.ATTACK
            elif dist < 300:
                self.state = AIState.CHASE
            else:
                self.state = AIState.IDLE

        # Execute state
        if self.state == AIState.CHASE:
            if self.entity.position.x < self.target.position.x:
                self.entity.move(1)
            else:
                self.entity.move(-1)

        elif self.state == AIState.ATTACK:
            # Face target
            if self.entity.position.x < self.target.position.x:
                self.entity.facing_right = True
            else:
                self.entity.facing_right = False

            # Attack logic
            if not self.entity.is_attacking:
                 if random.random() < 0.1: # Chance to attack
                     self.entity.attack()

        elif self.state == AIState.RETREAT:
             # Block while retreating sometimes
             if dist < 100:
                 self.entity.block(True)
             else:
                 self.entity.block(False)

             if self.entity.position.x < self.target.position.x:
                self.entity.move(-1)
             else:
                self.entity.move(1)

class RangedAI(AIController):
    def update(self):
        current_time = pygame.time.get_ticks()
        dist = self.entity.position.distance_to(self.target.position)

        # Ranged behavior: Keep distance ~300
        if dist < 200:
            self.state = AIState.RETREAT
        elif dist > 400:
            self.state = AIState.CHASE
        else:
            self.state = AIState.ATTACK

        # Face target
        if self.entity.position.x < self.target.position.x:
            self.entity.facing_right = True
        else:
            self.entity.facing_right = False

        if self.state == AIState.RETREAT:
            # Move away
            if self.entity.position.x < self.target.position.x:
                self.entity.move(-1)
            else:
                self.entity.move(1)

        elif self.state == AIState.CHASE:
             # Move closer
            if self.entity.position.x < self.target.position.x:
                self.entity.move(1)
            else:
                self.entity.move(-1)

        elif self.state == AIState.ATTACK:
            # Stop moving
            self.entity.velocity.x *= 0.5

            # Cast Spell if available
            spell = self.entity.spellbook.get_active()
            if spell and spell.can_cast(self.entity, current_time):
                spell.cast(self.entity, self.target.position, current_time, self.game_context)
