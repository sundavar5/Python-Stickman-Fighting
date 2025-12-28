
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stickfight.src.entities import Stickman

def test_single_hit():
    p1 = Stickman(100, 600)
    p2 = Stickman(120, 600)

    # Attack and hit once
    p1.attack()
    if not p1.check_hit(p2):
        print("FAIL: First hit not registered")
        sys.exit(1)

    # Try to hit again in same attack
    if p1.check_hit(p2):
        print("FAIL: Second hit registered (should be single hit per attack)")
        sys.exit(1)

    print("Single hit logic passed")

if __name__ == "__main__":
    test_single_hit()
