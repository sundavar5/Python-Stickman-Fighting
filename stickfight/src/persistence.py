
import json
import os
from stickfight.src.rpg import PlayerStats

class SaveManager:
    @staticmethod
    def save_game(player, filename="savegame.json"):
        data = {
            "stats": {
                "str": player.stats.base_stats["str"],
                "dex": player.stats.base_stats["dex"],
                "vit": player.stats.base_stats["vit"],
                "int": player.stats.base_stats["int"],
                "level": player.stats.level,
                "xp": player.stats.experience,
                "points": player.stats.stat_points
            },
            "inventory": {
                "gold": player.inventory.gold,
                # Serialization of items is complex, skipping strict item serialization for prototype
                # Would need item IDs and reconstruction logic
                "items": [item.name for item in player.inventory.items]
            }
        }

        with open(filename, 'w') as f:
            json.dump(data, f)
            return True

    @staticmethod
    def load_game(player, filename="savegame.json"):
        if not os.path.exists(filename):
            return False

        with open(filename, 'r') as f:
            data = json.load(f)

        stats_data = data["stats"]
        player.stats.base_stats["str"] = stats_data["str"]
        player.stats.base_stats["dex"] = stats_data["dex"]
        player.stats.base_stats["vit"] = stats_data["vit"]
        player.stats.base_stats["int"] = stats_data["int"]
        player.stats.level = stats_data["level"]
        player.stats.experience = stats_data["xp"]
        player.stats.stat_points = stats_data["points"]

        player.inventory.gold = data["inventory"]["gold"]

        # Recalculate derived stats
        player.max_health = player.stats.get_max_health()
        player.health = player.max_health

        return True
