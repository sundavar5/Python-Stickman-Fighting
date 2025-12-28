
import random
import uuid

class ItemRarity:
    COMMON = "common"
    RARE = "rare"
    LEGENDARY = "legendary"

class ItemType:
    WEAPON = "weapon"
    ARMOR = "armor"
    CONSUMABLE = "consumable"

class Item:
    def __init__(self, name, i_type, rarity, value, stats=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.type = i_type
        self.rarity = rarity
        self.value = value
        self.stats = stats or {} # {StatType.STR: 5}

class WeaponItem(Item):
    def __init__(self, name, rarity, value, w_class, damage, speed, range_val, stats=None):
        super().__init__(name, ItemType.WEAPON, rarity, value, stats)
        self.weapon_class = w_class # Sword, Axe etc
        self.damage = damage
        self.speed = speed
        self.range = range_val

class LootGenerator:
    def __init__(self):
        self.prefixes = {
            "Strong": {"str": 2},
            "Quick": {"dex": 2},
            "Hardy": {"vit": 2},
            "Sharp": {"str": 1, "dex": 1},
            "Heavy": {"str": 3, "dex": -1},
            "Legendary": {"str": 5, "dex": 5, "vit": 5}
        }
        self.suffixes = {
            "of the Bear": {"str": 2, "vit": 2},
            "of the Eagle": {"dex": 3},
            "of the Whale": {"vit": 5},
            "of Power": {"str": 5}
        }
        self.base_weapons = [
            {"name": "Sword", "class": "Sword", "dmg": 10, "spd": 1.0, "rng": 80},
            {"name": "Axe", "class": "Axe", "dmg": 18, "spd": 1.5, "rng": 70},
            {"name": "Spear", "class": "Spear", "dmg": 8, "spd": 0.8, "rng": 120},
            {"name": "Dagger", "class": "Sword", "dmg": 5, "spd": 0.5, "rng": 40}
        ]

    def generate_weapon(self, level):
        base = random.choice(self.base_weapons)
        rarity_roll = random.random()

        rarity = ItemRarity.COMMON
        affix_count = 0

        if rarity_roll < 0.05:
            rarity = ItemRarity.LEGENDARY
            affix_count = 2
        elif rarity_roll < 0.25:
            rarity = ItemRarity.RARE
            affix_count = 1

        name = base["name"]
        stats = {}

        # Add Prefix
        if affix_count > 0:
            prefix = random.choice(list(self.prefixes.keys()))
            name = f"{prefix} {name}"
            for k, v in self.prefixes[prefix].items():
                stats[k] = stats.get(k, 0) + v

        # Add Suffix
        if affix_count > 1:
            suffix = random.choice(list(self.suffixes.keys()))
            name = f"{name} {suffix}"
            for k, v in self.suffixes[suffix].items():
                stats[k] = stats.get(k, 0) + v

        # Scale by Level
        level_mult = 1 + (level * 0.1)
        dmg = int(base["dmg"] * level_mult)
        val = int(dmg * 10 * (1 + affix_count))

        return WeaponItem(
            name,
            rarity,
            val,
            base["class"],
            dmg,
            base["spd"],
            base["rng"],
            stats
        )
