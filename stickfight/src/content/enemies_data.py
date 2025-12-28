
from stickfight.src.rpg import PlayerStats

class EnemyDef:
    def __init__(self, name, level_mod, stats, weapon_type=None):
        self.name = name
        self.level_mod = level_mod # Multiplier for stats
        self.stats = stats
        self.weapon_type = weapon_type

ENEMIES = {
    "weak_goblin": EnemyDef("Goblin Runt", 0.8, PlayerStats(2, 2, 2, 0)),
    "goblin_warrior": EnemyDef("Goblin Warrior", 1.0, PlayerStats(4, 3, 4, 0)),
    "orc_grunt": EnemyDef("Orc Grunt", 1.2, PlayerStats(6, 2, 6, 0), "Axe"),
    "orc_chieftain": EnemyDef("Orc Chieftain", 1.5, PlayerStats(8, 4, 10, 0), "Axe"),
    "skeleton_archer": EnemyDef("Skeleton", 0.9, PlayerStats(2, 6, 2, 0), "Spear"),
    "elite_knight": EnemyDef("Dark Knight", 2.0, PlayerStats(10, 8, 10, 2), "Sword"),
    # ...
}
