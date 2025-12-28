
from stickfight.src.skills import SkillNode, SkillEffect

def load_warrior_skills(tree):
    # Root
    tree.add_node(SkillNode("w_root", "Training", "Gain 2 STR", 1, SkillEffect.PASSIVE_STAT, {"str": 2}))

    # Branch A: Offense
    tree.add_node(SkillNode("w_off_1", "Heavy Swing", "Gain 3 STR", 2, SkillEffect.PASSIVE_STAT, {"str": 3}, ["w_root"]))
    tree.add_node(SkillNode("w_off_2", "Brutal Force", "Gain 5 STR", 3, SkillEffect.PASSIVE_STAT, {"str": 5}, ["w_off_1"]))
    tree.add_node(SkillNode("w_active_1", "Spin Attack", "Unlock Spin Attack", 5, SkillEffect.ACTIVE_ABILITY, "spin_attack", ["w_off_2"]))

    # Branch B: Defense
    tree.add_node(SkillNode("w_def_1", "Iron Skin", "Gain 3 VIT", 2, SkillEffect.PASSIVE_STAT, {"vit": 3}, ["w_root"]))
    tree.add_node(SkillNode("w_def_2", "Thick Hide", "Gain 5 VIT", 3, SkillEffect.PASSIVE_STAT, {"vit": 5}, ["w_def_1"]))

    # ... Imagine 50 more nodes ...
