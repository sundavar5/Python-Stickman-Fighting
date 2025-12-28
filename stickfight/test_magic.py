
import sys
import os
import pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stickfight.src.magic import Spell, SpellType
from stickfight.src.entities import Stickman

# Mock Game Context
class GameContext:
    def __init__(self):
        self.projectiles = []

def test_magic():
    # Setup
    caster = Stickman(100, 100)
    caster.mana = 20

    spell = Spell("TestFire", 10, 1000, SpellType.PROJECTILE, damage=10)

    # Test Cast Success
    ctx = GameContext()
    if not spell.can_cast(caster, 0):
        print("FAIL: Should be able to cast")
        sys.exit(1)

    spell.cast(caster, (200, 100), 0, ctx)

    if caster.mana != 10:
        print("FAIL: Mana not drained")
        sys.exit(1)

    if len(ctx.projectiles) != 1:
        print("FAIL: Projectile not created")
        sys.exit(1)

    # Test Cooldown
    if spell.can_cast(caster, 500):
        print("FAIL: Cooldown ignored")
        sys.exit(1)

    if not spell.can_cast(caster, 1100):
        print("FAIL: Cooldown should be over")
        sys.exit(1)

    print("Magic System tests passed")

if __name__ == "__main__":
    test_magic()
