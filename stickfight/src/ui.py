
import pygame
from stickfight.src.constants import *

class UIManager:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)

    def draw(self, surface):
        self._draw_player_status(surface)
        self._draw_wave_info(surface)
        self._draw_controls(surface)

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
