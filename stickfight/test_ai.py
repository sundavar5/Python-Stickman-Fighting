
import sys
import os
import pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stickfight.src.ai import RangedAI, AIState
from stickfight.src.entities import Stickman
from stickfight.src.magic import Spell, SpellType

class GameContext:
    def __init__(self):
        self.projectiles = []

def test_ai():
    # Setup
    target = Stickman(0, 0)
    enemy = Stickman(100, 0)
    enemy.mana = 100

    # Give enemy a spell
    spell = Spell("Fire", 10, 100, SpellType.PROJECTILE)
    enemy.spellbook.add_spell(spell)

    ctx = GameContext()
    ai = RangedAI(enemy, target, ctx)

    # Initial state (distance 100 < 200) -> Should RETREAT
    ai.update()
    if ai.state != AIState.RETREAT:
        print(f"FAIL: Should retreat at dist 100. State: {ai.state}")
        sys.exit(1)

    # Move far away (distance 500 > 400) -> Should CHASE
    enemy.position.x = 500
    ai.update()
    if ai.state != AIState.CHASE:
        print(f"FAIL: Should chase at dist 500. State: {ai.state}")
        sys.exit(1)

    # Move to optimal range (300) -> Should ATTACK
    enemy.position.x = 300
    ai.update()
    if ai.state != AIState.ATTACK:
        print(f"FAIL: Should attack at dist 300. State: {ai.state}")
        sys.exit(1)

    # Check if spell was cast
    if len(ctx.projectiles) != 1:
        print("FAIL: AI did not cast spell")
        sys.exit(1)

    print("Advanced AI tests passed")

if __name__ == "__main__":
    test_ai()
