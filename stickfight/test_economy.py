
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stickfight.src.economy import Shop
from stickfight.src.inventory import Inventory

def test_economy():
    inv = Inventory()
    inv.gold = 1000
    shop = Shop(level=1)

    # Test Buy
    item_to_buy = shop.inventory[0]
    cost = item_to_buy.value

    if not shop.buy_item(inv, 0):
        print("FAIL: Could not buy item")
        sys.exit(1)

    if inv.gold != 1000 - cost:
        print("FAIL: Gold not deducted")
        sys.exit(1)

    if item_to_buy not in inv.items:
        print("FAIL: Item not in inventory")
        sys.exit(1)

    # Test Sell
    if not shop.sell_item(inv, item_to_buy):
        print("FAIL: Could not sell item")
        sys.exit(1)

    expected_gold = 1000 - cost + int(cost * 0.5)
    if inv.gold != expected_gold:
        print(f"FAIL: Gold incorrect after sell. Got {inv.gold}, expected {expected_gold}")
        sys.exit(1)

    print("Economy tests passed")

if __name__ == "__main__":
    test_economy()
