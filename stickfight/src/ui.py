
import pygame
from stickfight.src.constants import *
from stickfight.src.states import GameState

class UIManager:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.large_font = pygame.font.SysFont("Arial", 40)

    def draw(self, surface):
        if self.game.state == GameState.PLAYING:
            self._draw_player_status(surface)
            self._draw_wave_info(surface)
            self._draw_controls(surface)
        elif self.game.state == GameState.INVENTORY:
            self._draw_inventory(surface)

    def _draw_inventory(self, surface):
        # Dim background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))

        title = self.large_font.render("INVENTORY", True, WHITE)
        surface.blit(title, (50, 50))

        # Draw Stats
        stats = self.game.player.stats
        y = 120
        texts = [
            f"Level: {stats.level}",
            f"XP: {stats.experience} / {stats.xp_to_next}",
            f"STR: {stats.get_total('str')}",
            f"DEX: {stats.get_total('dex')}",
            f"VIT: {stats.get_total('vit')}",
            f"INT: {stats.get_total('int')}",
            f"Gold: {self.game.player.inventory.gold}"
        ]

        for t in texts:
            render = self.font.render(t, True, WHITE)
            surface.blit(render, (50, y))
            y += 30

        # Draw Items
        y = 120
        x = 400
        inv_title = self.font.render("Items (Press I to close):", True, WHITE)
        surface.blit(inv_title, (x, 80))

        for item in self.game.player.inventory.items:
            color = WHITE
            if item.rarity == "rare": color = BLUE
            elif item.rarity == "legendary": color = (255, 215, 0)

            i_text = self.small_font.render(f"- {item.name} ({item.value}g)", True, color)
            surface.blit(i_text, (x, y))
            y += 25

    def _draw_player_status(self, surface):
        # Health Bar Background
        pygame.draw.rect(surface, (50, 0, 0), (50, 50, 200, 20))
        # Health Bar Foreground
        health_width = (self.game.player.health / self.game.player.max_health) * 200
        pygame.draw.rect(surface, RED, (50, 50, max(0, health_width), 20))

        # Stamina Bar Background
        pygame.draw.rect(surface, (0, 0, 50), (50, 75, 150, 10))
        # Stamina Bar Foreground
        stamina_width = (self.game.player.stamina / self.game.player.max_stamina) * 150
        pygame.draw.rect(surface, BLUE, (50, 75, max(0, stamina_width), 10))

        # Weapon Name
        w_text = self.small_font.render(f"Weapon: {self.game.player.weapon.name}", True, BLACK)
        surface.blit(w_text, (50, 90))

    def _draw_wave_info(self, surface):
        wave_text = self.font.render(f"Wave {self.game.wave_manager.wave_number}", True, BLACK)
        surface.blit(wave_text, (SCREEN_WIDTH / 2 - wave_text.get_width() / 2, 50))

        enemies_left = len(self.game.wave_manager.enemies)
        count_text = self.small_font.render(f"Enemies: {enemies_left}", True, GRAY)
        surface.blit(count_text, (SCREEN_WIDTH / 2 - count_text.get_width() / 2, 80))

    def _draw_controls(self, surface):
        controls = [
            "Arrows: Move",
            "Space: Jump",
            "Z: Attack",
            "X: Block"
        ]

        y = SCREEN_HEIGHT - 120
        for line in controls:
            text = self.small_font.render(line, True, GRAY)
            surface.blit(text, (20, y))
            y += 20
