class Economy:
    def __init__(self):
        self.gold = 0

    def add_gold(self, amount):
        self.gold += amount
        print(f"Gained {amount} Gold. Total: {self.gold}")

    def spend_gold(self, amount):
        if self.gold >= amount:
            self.gold -= amount
            print(f"Spent {amount} Gold. Remaining: {self.gold}")
            return True
        print("Not enough gold!")
        return False

class Shop:
    def __init__(self, name, items):
        self.name = name
        self.items = items # List of (Item, Price) tuples

    def buy_item(self, player, item_index):
        if 0 <= item_index < len(self.items):
            item, price = self.items[item_index]
            if player.economy.spend_gold(price):
                player.inventory.add_item(item)
                print(f"Bought {item.name}")
