
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stickfight.src.quests import Quest, QuestManager
from stickfight.src.entities import Stickman

def test_quests():
    p = Stickman(0, 0)
    qm = QuestManager(p)

    q = Quest("kill_10", "Kill Goblins", "Slay 10 enemies", 100, 50)
    q.target = 2
    qm.add_quest(q)

    # Kill 1
    qm.on_enemy_killed("goblin")
    if q.progress != 1:
        print("FAIL: Progress not updated")
        sys.exit(1)

    # Kill 2 (Complete)
    start_gold = p.inventory.gold
    qm.on_enemy_killed("goblin")

    if q not in qm.completed_quests:
        print("FAIL: Quest not marked completed")
        sys.exit(1)

    if p.inventory.gold != start_gold + 100:
        print("FAIL: Reward gold not granted")
        sys.exit(1)

    print("Quest System tests passed")

if __name__ == "__main__":
    test_quests()
