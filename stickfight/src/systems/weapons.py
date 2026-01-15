import random

class WeaponDefinition:
    def __init__(self, name, min_dmg, max_dmg, speed, range_val, rarity="Common", element=None):
        self.name = name
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        self.speed = speed
        self.range = range_val
        self.rarity = rarity
        self.element = element

class WeaponGenerator:
    """
    Generates procedural weapons.
    """
    prefixes = ["Rusty", "Old", "Shiny", "Sharp", "Heavy", "Light", "Brutal", "Legendary", "Cursed", "Divine"]
    base_types = [
        {"name": "Dagger", "min": 2, "max": 5, "speed": 1.5, "range": 20},
        {"name": "Sword", "min": 5, "max": 10, "speed": 1.0, "range": 40},
        {"name": "Axe", "min": 8, "max": 15, "speed": 0.8, "range": 35},
        {"name": "Spear", "min": 4, "max": 12, "speed": 0.9, "range": 60},
        {"name": "Hammer", "min": 10, "max": 25, "speed": 0.5, "range": 30}
    ]
    suffixes = ["of Speed", "of Power", "of the Bear", "of the Eagle", "of Fire", "of Ice"]

    @staticmethod
    def generate_weapon(level):
        base = random.choice(WeaponGenerator.base_types)
        prefix = random.choice(WeaponGenerator.prefixes)

        # Stat multiplier based on level and prefix
        multiplier = 1.0 + (level * 0.1)
        if prefix == "Legendary": multiplier += 0.5
        elif prefix == "Rusty": multiplier -= 0.2

        min_dmg = int(base["min"] * multiplier)
        max_dmg = int(base["max"] * multiplier)
        name = f"{prefix} {base['name']}"

        # 30% chance for suffix
        if random.random() < 0.3:
            suffix = random.choice(WeaponGenerator.suffixes)
            name += f" {suffix}"
            multiplier += 0.2

        rarity = "Common"
        if multiplier > 2.0: rarity = "Legendary"
        elif multiplier > 1.5: rarity = "Epic"
        elif multiplier > 1.2: rarity = "Rare"

        return WeaponDefinition(name, min_dmg, max_dmg, base["speed"], base["range"], rarity)

# Pre-generate a massive cache of weapons
WEAPON_CACHE = [WeaponGenerator.generate_weapon(level) for level in range(1, 50) for _ in range(10)]
