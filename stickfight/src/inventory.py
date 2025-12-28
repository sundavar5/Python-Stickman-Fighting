
from stickfight.src.items import ItemType

class Inventory:
    def __init__(self, capacity=20):
        self.capacity = capacity
        self.items = []
        self.equipped = {
            "weapon": None,
            "armor": None
        }
        self.gold = 0

    def add_item(self, item):
        if len(self.items) >= self.capacity:
            return False
        self.items.append(item)
        return True

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def equip(self, item):
        if item.type == ItemType.WEAPON:
            if self.equipped["weapon"]:
                self.unequip("weapon")
            self.equipped["weapon"] = item
            if item in self.items:
                self.items.remove(item)

    def unequip(self, slot):
        item = self.equipped.get(slot)
        if item:
            if len(self.items) < self.capacity:
                self.items.append(item)
                self.equipped[slot] = None
                return True
        return False
