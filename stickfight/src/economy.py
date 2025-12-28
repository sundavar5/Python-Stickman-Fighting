
import random
from stickfight.src.items import LootGenerator

class Shop:
    def __init__(self, level):
        self.level = level
        self.inventory = [] # Items available
        self.refresh_stock()

    def refresh_stock(self):
        gen = LootGenerator()
        self.inventory = []
        for _ in range(5):
            self.inventory.append(gen.generate_weapon(self.level))

    def buy_item(self, player_inventory, item_index):
        if item_index < 0 or item_index >= len(self.inventory):
            return False

        item = self.inventory[item_index]
        if player_inventory.gold >= item.value:
            player_inventory.gold -= item.value
            player_inventory.add_item(item)
            self.inventory.pop(item_index)
            return True
        return False

    def sell_item(self, player_inventory, item):
        if player_inventory.remove_item(item):
            player_inventory.gold += int(item.value * 0.5)
            return True
        return False
