class Item:
    """Base class for all items."""
    def __init__(self, name, description, value=0, stackable=False):
        self.name = name
        self.description = description
        self.value = value
        self.stackable = stackable

class Weapon(Item):
    """Weapon items."""
    def __init__(self, name, description, damage, speed, range, value=0):
        super().__init__(name, description, value, stackable=False)
        self.damage = damage
        self.speed = speed
        self.range = range

class Potion(Item):
    """Consumable potions."""
    def __init__(self, name, description, effect_type, effect_amount, value=10):
        super().__init__(name, description, value, stackable=True)
        self.effect_type = effect_type # 'health', 'mana'
        self.effect_amount = effect_amount

class Inventory:
    """
    Manages a collection of items.
    """
    def __init__(self, capacity=20):
        self.capacity = capacity
        self.items = [] # List of Item objects

    def add_item(self, item):
        """Adds an item to the inventory."""
        if len(self.items) < self.capacity:
            self.items.append(item)
            print(f"Added {item.name} to inventory.")
            return True
        else:
            print("Inventory is full!")
            return False

    def remove_item(self, item_name):
        """Removes an item by name."""
        for i, item in enumerate(self.items):
            if item.name == item_name:
                removed = self.items.pop(i)
                print(f"Removed {removed.name} from inventory.")
                return removed
        return None

    def list_items(self):
        """Returns a list of item names."""
        return [item.name for item in self.items]
