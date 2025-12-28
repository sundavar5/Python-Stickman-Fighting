
import math

class StatType:
    STRENGTH = "str" # Melee Dmg
    DEXTERITY = "dex" # Speed, Crit
    VITALITY = "vit" # Health, Stamina
    INTELLIGENCE = "int" # Skill Cooldown, Mana (if added)

class PlayerStats:
    def __init__(self, str_val=5, dex_val=5, vit_val=5, int_val=5):
        self.base_stats = {
            StatType.STRENGTH: str_val,
            StatType.DEXTERITY: dex_val,
            StatType.VITALITY: vit_val,
            StatType.INTELLIGENCE: int_val
        }
        self.bonus_stats = {
            StatType.STRENGTH: 0,
            StatType.DEXTERITY: 0,
            StatType.VITALITY: 0,
            StatType.INTELLIGENCE: 0
        }

        self.level = 1
        self.experience = 0
        self.xp_to_next = 100
        self.stat_points = 0

    def get_total(self, stat_type):
        return self.base_stats.get(stat_type, 0) + self.bonus_stats.get(stat_type, 0)

    def add_xp(self, amount):
        self.experience += amount
        leveled_up = False
        while self.experience >= self.xp_to_next:
            self.experience -= self.xp_to_next
            self.level_up()
            leveled_up = True
        return leveled_up

    def level_up(self):
        self.level += 1
        self.xp_to_next = int(self.xp_to_next * 1.5)
        self.stat_points += 5
        # Auto stat growth?
        self.base_stats[StatType.STRENGTH] += 1
        self.base_stats[StatType.VITALITY] += 1

    def get_max_health(self):
        return 50 + (self.get_total(StatType.VITALITY) * 10) + (self.level * 5)

    def get_max_stamina(self):
        return 50 + (self.get_total(StatType.VITALITY) * 2) + (self.get_total(StatType.DEXTERITY) * 3)

    def get_damage_multiplier(self):
        return 1.0 + (self.get_total(StatType.STRENGTH) * 0.05)

    def get_crit_chance(self):
        return 0.01 * self.get_total(StatType.DEXTERITY)

    def get_move_speed_mult(self):
        return 1.0 + (self.get_total(StatType.DEXTERITY) * 0.01)

class CharacterClass:
    WARRIOR = "warrior"
    ROGUE = "rogue"
    TANK = "tank"

    @staticmethod
    def get_starting_stats(class_name):
        if class_name == CharacterClass.WARRIOR:
            return PlayerStats(str_val=8, dex_val=4, vit_val=6, int_val=2)
        elif class_name == CharacterClass.ROGUE:
            return PlayerStats(str_val=4, dex_val=10, vit_val=4, int_val=2)
        elif class_name == CharacterClass.TANK:
            return PlayerStats(str_val=6, dex_val=2, vit_val=10, int_val=2)
        return PlayerStats()
