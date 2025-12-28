
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stickfight.src.entities import Stickman

def test_stamina_and_block():
    p1 = Stickman(100, 600)

    # Test Stamina Drain on Attack
    start_stam = p1.stamina
    p1.attack()
    if p1.stamina >= start_stam:
        print("FAIL: Stamina did not drain on attack")
        sys.exit(1)

    print("Stamina drain OK")

    # Test Block Damage Reduction
    p1.stamina = 100
    p1.block(True)
    p1.take_damage(20)

    if p1.health != 100:
        print("FAIL: Health reduced while blocking")
        sys.exit(1)

    if p1.stamina >= 100:
         print("FAIL: Stamina not drained when blocking damage")
         sys.exit(1)

    print("Block logic OK")

if __name__ == "__main__":
    test_stamina_and_block()
