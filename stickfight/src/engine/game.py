import pygame
import sys
import os
from engine.settings import *
from engine.input import InputManager
from engine.assets import AssetManager

from world.tilemap import TileMap
from systems.physics import PhysicsEngine
from systems.combat import CombatSystem
from systems.stats import Stats
from systems.inventory import Inventory
from systems.particles import ParticleSystem
from systems.magic import MagicSystem
from systems.skills import SkillTree
from systems.quests import QuestManager
from systems.economy import Economy
from entities.player import Player
from entities.enemy import StickmanEnemy, SlimeEnemy, FlyingEnemy
from entities.boss import Boss
from world.interactables import Chest, Door
from ui.interface import Interface

class Game:
    """
    Main game class handling initialization, the game loop, and updating/drawing systems.
    """
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()
        except pygame.error:
            print("Warning: Audio device not found. Sound disabled.")

        # Determine if we are running in a headless environment
        driver = os.environ.get('SDL_VIDEODRIVER')
        if driver == 'dummy':
            self.screen = pygame.display.set_mode((1, 1))
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.input = InputManager()
        self.assets = AssetManager()
        self.physics = PhysicsEngine()
        self.particles = ParticleSystem()
        self.quests = QuestManager()
        self.combat = CombatSystem(self.particles, self.assets, self.quests)
        self.magic = MagicSystem(self.particles)

        # State
        self.entities = []
        self.interactables = []
        self.tilemap = None
        self.player = None
        self.ui = None
        self.camera_offset = [0, 0]

    def init_game(self):
        """Initializes game entities and world."""
        print("Initializing game world...")
        self.assets.load_font('default', None, 24)

        # World
        self.tilemap = TileMap(width=200, height=50)

        # Player
        self.player = Player(100, 100, self.input, self.physics, self.tilemap)
        self.player.stats = Stats(hp=100, mana=50)
        self.player.inventory = Inventory()
        self.player.economy = Economy()
        self.player.skills = SkillTree()
        self.entities.append(self.player)

        # Enemies
        for i in range(5):
            enemy = StickmanEnemy(400 + i * 200, 100, self.physics, self.tilemap)
            enemy.stats = Stats(hp=30)
            self.entities.append(enemy)

        slime = SlimeEnemy(800, 100, self.physics, self.tilemap)
        slime.stats = Stats(hp=20)
        self.entities.append(slime)

        # Boss
        boss = Boss(1200, 100, "The Big Stick", self.physics, self.tilemap, self.particles)
        boss.stats = Stats(hp=500)
        self.entities.append(boss)

        # Interactables
        self.interactables.append(Chest(600, 100))
        self.interactables.append(Door(50, 100, "Level 2"))

        # UI
        self.ui = Interface(self.assets)

    def run(self):
        """Main game loop."""
        self.init_game()

        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds

            self.handle_input()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()

    def handle_input(self):
        """Delegates input handling."""
        self.input.update()
        if self.input.quit_requested:
            self.running = False

        # Debug: Spawn enemy
        if self.input.is_key_just_pressed(pygame.K_p):
            enemy = StickmanEnemy(self.player.rect.x + 100, 100, self.physics, self.tilemap)
            enemy.stats = Stats(hp=30)
            self.entities.append(enemy)
            print("Spawned Enemy")

        # Combat Input
        if self.input.is_key_just_pressed(pygame.K_z): # Attack
             self.combat.perform_attack(self.player, self.entities)

        if self.input.is_key_just_pressed(pygame.K_x): # Magic
             self.magic.cast_fireball(self.player)

        # Interact
        if self.input.is_key_just_pressed(pygame.K_e):
            for obj in self.interactables:
                if self.player.rect.colliderect(obj.rect):
                    obj.interact(self.player)

    def update(self, dt):
        """Updates all game systems."""
        # Update particles
        self.particles.update()

        # Update magic
        self.magic.update(dt, self.tilemap, self.entities)

        # Update entities
        active_entities = []
        for entity in self.entities:
            entity.update(dt)
            if entity.is_active:
                active_entities.append(entity)
        self.entities = active_entities

        # Camera Follow
        target_x = self.player.rect.centerx - SCREEN_WIDTH // 2
        target_y = self.player.rect.centery - SCREEN_HEIGHT // 2
        self.camera_offset[0] += (target_x - self.camera_offset[0]) * 0.1
        self.camera_offset[1] += (target_y - self.camera_offset[1]) * 0.1

        # Update UI
        self.ui.update(self.player)

    def draw(self):
        """Draws the game frame."""
        self.screen.fill(DARK_GRAY)

        # Draw World
        self.tilemap.draw(self.screen, self.camera_offset)

        # Draw Interactables
        for obj in self.interactables:
            obj.draw(self.screen, self.camera_offset)

        # Draw Entities
        for entity in self.entities:
            entity.draw(self.screen, self.camera_offset)

        # Draw Magic
        self.magic.draw(self.screen, self.camera_offset)

        # Draw Particles
        self.particles.draw(self.screen, self.camera_offset)

        # Draw UI
        self.ui.draw(self.screen)

        # Debug info
        font = self.assets.get_font('default')
        if font:
            fps_text = font.render(f"FPS: {int(self.clock.get_fps())}", True, WHITE)
            self.screen.blit(fps_text, (10, 10))

            pos_text = font.render(f"Pos: {self.player.rect.x}, {self.player.rect.y}", True, WHITE)
            self.screen.blit(pos_text, (10, 40))

        pygame.display.flip()
