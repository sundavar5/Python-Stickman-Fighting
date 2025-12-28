
import random
import pygame
from stickfight.src.entities import Stickman

class AIState:
    IDLE = 0
    CHASE = 1
    ATTACK = 2
    RETREAT = 3

class AIController:
    def __init__(self, entity, target):
        self.entity = entity
        self.target = target
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
