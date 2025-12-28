
from stickfight.src.magic import Spell, SpellType

SPELLS = [
    Spell("Fireball", 10, 1000, SpellType.PROJECTILE, damage=25),
    Spell("IceShard", 5, 500, SpellType.PROJECTILE, damage=12),
    Spell("ThunderBolt", 20, 2000, SpellType.PROJECTILE, damage=50),
    Spell("Heal", 30, 5000, SpellType.SELF_BUFF, effect_func=lambda c: setattr(c, 'health', min(c.max_health, c.health + 30))),
    Spell("ArcaneMissile", 8, 300, SpellType.PROJECTILE, damage=15),
    Spell("ShadowBolt", 12, 1200, SpellType.PROJECTILE, damage=30),
    Spell("HolyLight", 25, 3000, SpellType.PROJECTILE, damage=40),
    Spell("PoisonDart", 5, 200, SpellType.PROJECTILE, damage=5),
    # ... Imagine 50 more lines
]
