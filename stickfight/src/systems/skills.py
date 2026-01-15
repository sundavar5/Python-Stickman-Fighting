class Skill:
    def __init__(self, name, description, max_rank=1):
        self.name = name
        self.description = description
        self.max_rank = max_rank
        self.current_rank = 0
        self.unlocked = False

class SkillTree:
    def __init__(self):
        self.skills = {
            "strength": Skill("Muscle Up", "Increases Strength by 5 per rank.", 5),
            "vitality": Skill("Iron Skin", "Increases Max HP by 20 per rank.", 5),
            "magic": Skill("Arcane Knowledge", "Unlocks Fireball spell.", 1),
            "agility": Skill("Double Jump", "Allows jumping in mid-air.", 1)
        }
        self.skill_points = 0

    def unlock(self, skill_name, player):
        if self.skill_points <= 0:
            print("No skill points available.")
            return False

        skill = self.skills.get(skill_name)
        if skill and skill.current_rank < skill.max_rank:
            skill.current_rank += 1
            skill.unlocked = True
            self.skill_points -= 1
            self.apply_effect(skill_name, player)
            print(f"Unlocked {skill.name} Rank {skill.current_rank}")
            return True
        return False

    def apply_effect(self, skill_name, player):
        skill = self.skills[skill_name]
        if skill_name == "strength":
            player.stats.strength += 5
        elif skill_name == "vitality":
            player.stats.max_hp += 20
            player.stats.current_hp += 20
        elif skill_name == "agility":
            player.max_jumps = 2 # Logic needs to be in Player class
