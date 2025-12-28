
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from stickfight.src.skills import SkillTree
from stickfight.src.rpg import PlayerStats
from stickfight.src.content.skills_data import load_warrior_skills

def test_skills():
    tree = SkillTree()
    load_warrior_skills(tree)
    stats = PlayerStats()
    stats.stat_points = 10 # Give enough points

    # Try unlock root
    if not tree.unlock("w_root", stats):
        print("FAIL: Could not unlock root")
        sys.exit(1)

    if stats.bonus_stats["str"] != 2:
        print("FAIL: Stats not applied")
        sys.exit(1)

    # Try unlock tier 2
    if not tree.unlock("w_off_1", stats):
        print("FAIL: Could not unlock tier 2")
        sys.exit(1)

    # Try unlock without parent
    if tree.unlock("w_active_1", stats):
        print("FAIL: Unlocked without parent dependency")
        sys.exit(1)

    print("Skill Tree tests passed")

if __name__ == "__main__":
    test_skills()
