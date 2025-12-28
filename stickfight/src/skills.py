
class SkillEffect:
    PASSIVE_STAT = "passive_stat" # {stat: val}
    ACTIVE_ABILITY = "active_ability" # unlock ability name

class SkillNode:
    def __init__(self, s_id, name, description, cost, effect_type, effect_data, parent_ids=None):
        self.id = s_id
        self.name = name
        self.description = description
        self.cost = cost
        self.effect_type = effect_type
        self.effect_data = effect_data
        self.parent_ids = parent_ids or []
        self.unlocked = False

class SkillTree:
    def __init__(self):
        self.nodes = {} # id: SkillNode

    def add_node(self, node):
        self.nodes[node.id] = node

    def can_unlock(self, node_id, player_points):
        node = self.nodes.get(node_id)
        if not node: return False
        if node.unlocked: return False
        if player_points < node.cost: return False

        # Check parents
        for pid in node.parent_ids:
            if not self.nodes[pid].unlocked:
                return False

        return True

    def unlock(self, node_id, player_stats):
        if self.can_unlock(node_id, player_stats.stat_points):
            node = self.nodes[node_id]
            player_stats.stat_points -= node.cost
            node.unlocked = True
            self._apply_effect(node, player_stats)
            return True
        return False

    def _apply_effect(self, node, player_stats):
        if node.effect_type == SkillEffect.PASSIVE_STAT:
            for k, v in node.effect_data.items():
                player_stats.bonus_stats[k] = player_stats.bonus_stats.get(k, 0) + v
        elif node.effect_type == SkillEffect.ACTIVE_ABILITY:
            # Handle ability unlock via callback or event
            pass
