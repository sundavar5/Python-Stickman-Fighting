
import random

class NodeType:
    START = "start"
    BATTLE = "battle"
    ELITE = "elite"
    SHOP = "shop"
    REST = "rest"
    BOSS = "boss"

class MapNode:
    def __init__(self, n_id, n_type, layer, children=None):
        self.id = n_id
        self.type = n_type
        self.layer = layer # Depth in map
        self.children = children or [] # IDs of nodes in next layer
        self.visited = False

class CampaignMap:
    def __init__(self):
        self.nodes = {}
        self.current_node_id = None
        self.layers = 10
        self.width = 3

    def generate(self):
        # Layer 0: Start
        start_node = MapNode(0, NodeType.START, 0)
        self.nodes[0] = start_node
        self.current_node_id = 0

        previous_layer_ids = [0]
        id_counter = 1

        for layer in range(1, self.layers):
            current_layer_ids = []
            # Determine width for this layer (random 2-4)
            width = random.randint(2, 4)
            if layer == self.layers - 1:
                width = 1 # Boss

            for w in range(width):
                n_type = self._get_random_type(layer)
                if layer == self.layers - 1:
                    n_type = NodeType.BOSS

                node = MapNode(id_counter, n_type, layer)
                self.nodes[id_counter] = node
                current_layer_ids.append(id_counter)
                id_counter += 1

            # Connect previous to current
            for prev_id in previous_layer_ids:
                # Ensure at least one connection
                target = random.choice(current_layer_ids)
                self.nodes[prev_id].children.append(target)

                # Chance for more
                for target_id in current_layer_ids:
                    if target_id != target and random.random() < 0.3:
                        self.nodes[prev_id].children.append(target_id)

            previous_layer_ids = current_layer_ids

    def _get_random_type(self, layer):
        roll = random.random()
        if roll < 0.5: return NodeType.BATTLE
        if roll < 0.65: return NodeType.SHOP
        if roll < 0.8: return NodeType.REST
        if roll < 0.9: return NodeType.ELITE
        return NodeType.BATTLE

    def get_available_paths(self):
        if self.current_node_id is None: return []
        return self.nodes[self.current_node_id].children

    def travel(self, node_id):
        if node_id in self.get_available_paths():
            self.current_node_id = node_id
            self.nodes[node_id].visited = True
            return True
        return False

    def print_map(self):
        # Debug print
        for nid, node in self.nodes.items():
            print(f"Node {nid} ({node.type}) L:{node.layer} -> {node.children}")
