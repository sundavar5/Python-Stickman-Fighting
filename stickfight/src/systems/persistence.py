import json
import os

class Persistence:
    @staticmethod
    def save_game(player, filepath="savegame.json"):
        data = {
            "stats": {
                "hp": player.stats.current_hp,
                "max_hp": player.stats.max_hp,
                "mana": player.stats.current_mana,
                "xp": player.stats.experience,
                "level": player.stats.level
            },
            "inventory": [item.name for item in player.inventory.items],
            "position": {"x": player.rect.x, "y": player.rect.y}
        }

        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            print("Game Saved!")
        except Exception as e:
            print(f"Failed to save game: {e}")

    @staticmethod
    def load_game(player, filepath="savegame.json"):
        if not os.path.exists(filepath):
            print("No save file found.")
            return False

        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            player.stats.current_hp = data["stats"]["hp"]
            player.stats.max_hp = data["stats"]["max_hp"]
            player.stats.current_mana = data["stats"]["mana"]
            player.stats.experience = data["stats"]["xp"]
            player.stats.level = data["stats"]["level"]

            player.rect.x = data["position"]["x"]
            player.rect.y = data["position"]["y"]

            # Inventory loading would require looking up item objects by name
            # Skipping for this prototype as it requires a global item registry

            print("Game Loaded!")
            return True
        except Exception as e:
            print(f"Failed to load game: {e}")
            return False
