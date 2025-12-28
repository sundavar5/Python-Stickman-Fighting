
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stickfight.src.entities import Stickman

def test_combat():
    p1 = Stickman(100, 600)
    p2 = Stickman(120, 600)

    # Test Attack Init
    p1.attack()
    if not p1.is_attacking:
        print("FAIL: Attack did not start")
        sys.exit(1)

    # Test Hit Detection (Within range and facing)
    p1.facing_right = True
    if not p1.check_hit(p2):
        print("FAIL: Hit not detected")
        sys.exit(1)

    # Test Damage
    p2.take_damage(10)
    if p2.health != 90:
        print("FAIL: Damage not taken")
        sys.exit(1)

    print("Combat tests passed")

if __name__ == "__main__":
    test_combat()
