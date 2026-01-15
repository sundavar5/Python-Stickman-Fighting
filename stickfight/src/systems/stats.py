class Stats:
    """
    Manages RPG statistics for an entity.
    """
    def __init__(self, hp=100, mana=50, stamina=100, strength=10, dexterity=10, intelligence=10):
        self.max_hp = hp
        self.current_hp = hp
        self.max_mana = mana
        self.current_mana = mana
        self.max_stamina = stamina
        self.current_stamina = stamina

        # Attributes
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence

        self.level = 1
        self.experience = 0
        self.next_level_xp = 100

    def take_damage(self, amount):
        """Reduces HP by amount."""
        self.current_hp -= amount
        if self.current_hp < 0:
            self.current_hp = 0

    def heal(self, amount):
        """Restores HP by amount."""
        self.current_hp += amount
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

    def use_mana(self, amount):
        """Consumes mana."""
        if self.current_mana >= amount:
            self.current_mana -= amount
            return True
        return False

    def gain_xp(self, amount):
        """Adds experience and checks for level up."""
        self.experience += amount
        while self.experience >= self.next_level_xp:
            self.level_up()

    def level_up(self):
        """Increases stats and resets XP."""
        self.experience -= self.next_level_xp
        self.level += 1
        self.next_level_xp = int(self.next_level_xp * 1.5)

        # Stat growth
        self.max_hp += 10
        self.max_mana += 5
        self.strength += 2
        self.dexterity += 2
        self.intelligence += 2

        # Full heal on level up
        self.current_hp = self.max_hp
        self.current_mana = self.max_mana
        print(f"Level Up! Now Level {self.level}")
