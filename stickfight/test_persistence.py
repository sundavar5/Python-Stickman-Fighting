
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stickfight.src.persistence import SaveManager
from stickfight.src.entities import Stickman

def test_persistence():
    p1 = Stickman(0, 0)
    p1.stats.level = 5
    p1.stats.base_stats["str"] = 20
    p1.inventory.gold = 500

    SaveManager.save_game(p1, "test_save.json")

    p2 = Stickman(0, 0)
    if not SaveManager.load_game(p2, "test_save.json"):
        print("FAIL: Load failed")
        sys.exit(1)

    if p2.stats.level != 5:
        print("FAIL: Level mismatch")
        sys.exit(1)

    if p2.stats.base_stats["str"] != 20:
        print("FAIL: STR mismatch")
        sys.exit(1)

    if p2.inventory.gold != 500:
        print("FAIL: Gold mismatch")
        sys.exit(1)

    print("Persistence tests passed")
    os.remove("test_save.json")

if __name__ == "__main__":
    test_persistence()
