
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stickfight.src.entities import Stickman
from stickfight.src.weapons import Sword, Spear

def test_weapon_equip():
    p1 = Stickman(100, 600)
    sword = Sword()
    p1.equip_weapon(sword)

    if p1.weapon.name != "Sword":
        print("FAIL: Weapon not equipped")
        sys.exit(1)

    print(f"Equipped {p1.weapon.name} OK")

    spear = Spear()
    p1.equip_weapon(spear)
    if p1.weapon.name != "Spear":
        print("FAIL: Weapon swap failed")
        sys.exit(1)

    print(f"Swapped to {p1.weapon.name} OK")

if __name__ == "__main__":
    test_weapon_equip()
