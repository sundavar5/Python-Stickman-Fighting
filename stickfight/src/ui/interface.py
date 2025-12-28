import pygame
from ui.elements import ProgressBar, Button
from engine.settings import *

class Interface:
    """
    Manages the HUD and User Interface layers.
    """
    def __init__(self, asset_manager):
        self.assets = asset_manager
        self.elements = []

        # HUD Elements
        self.hp_bar = ProgressBar(20, 20, 200, 20, RED, 100)
        self.mana_bar = ProgressBar(20, 50, 150, 15, BLUE, 50)
        self.xp_bar = ProgressBar(0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 10, YELLOW, 100)

        self.elements.append(self.hp_bar)
        self.elements.append(self.mana_bar)
        self.elements.append(self.xp_bar)

    def update(self, player):
        """Updates UI elements based on player state."""
        if hasattr(player, 'stats'):
            self.hp_bar.update_value(player.stats.current_hp, player.stats.max_hp)
            self.mana_bar.update_value(player.stats.current_mana, player.stats.max_mana)
            self.xp_bar.update_value(player.stats.experience, player.stats.next_level_xp)

    def draw(self, surface):
        for element in self.elements:
            element.draw(surface)

        # Draw text labels
        font = self.assets.get_font('default')
        # if font:
        #     hp_text = font.render(f"{int(self.hp_bar.current_value)}/{self.hp_bar.max_value}", True, WHITE)
        #     surface.blit(hp_text, (230, 20))
