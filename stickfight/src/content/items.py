from systems.inventory import Weapon, Potion

# Weapons
SWORD_WOODEN = Weapon("Wooden Sword", "A basic practice sword.", damage=5, speed=1.0, range=40, value=10)
SWORD_IRON = Weapon("Iron Sword", "A standard soldier's sword.", damage=15, speed=1.1, range=45, value=50)
SWORD_STEEL = Weapon("Steel Sword", "A sharp, reliable blade.", damage=25, speed=1.2, range=45, value=150)
SWORD_DIAMOND = Weapon("Diamond Sword", "Extremely sharp and durable.", damage=50, speed=1.3, range=50, value=500)

AXE_RUSTY = Weapon("Rusty Axe", "Heavy and slow.", damage=20, speed=0.7, range=35, value=20)
AXE_BATTLE = Weapon("Battle Axe", "Designed for war.", damage=40, speed=0.8, range=40, value=120)

DAGGER_IRON = Weapon("Iron Dagger", "Fast but short range.", damage=10, speed=2.0, range=20, value=40)

# Potions
POTION_HEALTH_SMALL = Potion("Small Health Potion", "Restores 20 HP.", "health", 20, value=15)
POTION_HEALTH_LARGE = Potion("Large Health Potion", "Restores 50 HP.", "health", 50, value=40)
POTION_MANA_SMALL = Potion("Small Mana Potion", "Restores 20 Mana.", "mana", 20, value=20)

ALL_ITEMS = [
    SWORD_WOODEN, SWORD_IRON, SWORD_STEEL, SWORD_DIAMOND,
    AXE_RUSTY, AXE_BATTLE,
    DAGGER_IRON,
    POTION_HEALTH_SMALL, POTION_HEALTH_LARGE, POTION_MANA_SMALL
]
