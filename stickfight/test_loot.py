
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stickfight.src.items import LootGenerator
from stickfight.src.inventory import Inventory

def test_loot():
    gen = LootGenerator()
    inv = Inventory()

    print("Generating 10 items...")
    for i in range(10):
        item = gen.generate_weapon(level=5)
        print(f"Looted: {item.name} ({item.rarity}) - DMG: {item.damage}")
        if not inv.add_item(item):
            print("Inventory Full!")

    if len(inv.items) != 10:
        print("FAIL: Items not added")
        sys.exit(1)

    # Equip logic
    best_weapon = inv.items[0]
    inv.equip(best_weapon)

    if inv.equipped["weapon"] != best_weapon:
        print("FAIL: Equip failed")
        sys.exit(1)

    if best_weapon in inv.items:
        print("FAIL: Equipped item still in bag")
        sys.exit(1)

    print("Loot & Inventory tests passed")

if __name__ == "__main__":
    test_loot()
