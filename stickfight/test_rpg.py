
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stickfight.src.rpg import PlayerStats, CharacterClass, StatType

def test_rpg():
    # Test Class Creation
    warrior = CharacterClass.get_starting_stats(CharacterClass.WARRIOR)
    if warrior.base_stats[StatType.STRENGTH] != 8:
        print("FAIL: Warrior STR invalid")
        sys.exit(1)

    print(f"Lvl 1 HP: {warrior.get_max_health()}")

    # Test Leveling
    leveled = warrior.add_xp(150) # Need 100
    if not leveled or warrior.level != 2:
        print("FAIL: Did not level up correctly")
        sys.exit(1)

    if warrior.stat_points != 5:
        print("FAIL: Stat points not awarded")
        sys.exit(1)

    print(f"Lvl 2 HP: {warrior.get_max_health()}")

    # Test Stat Impact
    base_dmg = warrior.get_damage_multiplier()
    warrior.bonus_stats[StatType.STRENGTH] = 10
    new_dmg = warrior.get_damage_multiplier()

    if new_dmg <= base_dmg:
        print("FAIL: Bonus stats did not increase damage")
        sys.exit(1)

    print("RPG Core tests passed")

if __name__ == "__main__":
    test_rpg()
