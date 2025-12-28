import sys
import pygame
from stickfight.src.constants import *
from stickfight.src.entities import Stickman
from stickfight.src.ai import AIController
from stickfight.src.particles import ParticleManager
from stickfight.src.weapons import Sword, Spear, Axe
from stickfight.src.world import load_test_level
from stickfight.src.waves import WaveManager
from stickfight.src.ui import UIManager
from stickfight.src.rpg import PlayerStats, CharacterClass
from stickfight.src.states import GameState
from stickfight.src.magic import Spell
from stickfight.src.content.spells_data import SPELLS
from stickfight.src.quests import QuestManager
from stickfight.src.content.quests_data import QUESTS

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Stickman RPG")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.PLAYING

        # Systems
        self.particles = ParticleManager()
        self.level = load_test_level()
        self.projectiles = []

        # Entities
        stats = CharacterClass.get_starting_stats(CharacterClass.WARRIOR)
        self.player = Stickman(200, GROUND_Y, color=BLACK, stats=stats)
        self.player.equip_weapon(Sword())
        self.player.level = self.level
        self.player.spellbook.add_spell(SPELLS[0]) # Start with Fireball

        # Inject Particle Manager into Player
        self.player.particles = self.particles

        # Quests
        self.quest_manager = QuestManager(self.player)
        self.quest_manager.add_quest(QUESTS[0])

        # Waves
        self.wave_manager = WaveManager(self)

        # UI
        self.ui = UIManager(self)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                # Toggle UI states
                if event.key == pygame.K_i:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.INVENTORY
                    elif self.state == GameState.INVENTORY:
                        self.state = GameState.PLAYING

                if self.state == GameState.PLAYING:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    elif event.key == pygame.K_z:
                        self.player.attack()
                    elif event.key == pygame.K_c:
                        # Cast Spell
                        spell = self.player.spellbook.get_active()
                        # Cast towards nearest enemy or forward
                        target_pos = (self.player.position.x + 300, self.player.position.y)
                        if not self.player.facing_right:
                             target_pos = (self.player.position.x - 300, self.player.position.y)

                        if spell and spell.can_cast(self.player, pygame.time.get_ticks()):
                            spell.cast(self.player, target_pos, pygame.time.get_ticks(), self)

        if self.state == GameState.PLAYING:
            # Continuous input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move(-1)
            if keys[pygame.K_RIGHT]:
                self.player.move(1)

            if keys[pygame.K_x]:
                self.player.block(True)
            else:
                self.player.block(False)

    def update(self):
        dt = self.clock.get_time() # Time since last tick in ms

        if self.state == GameState.PLAYING:
            self.particles.update(dt)
            self.level.update(dt)
            self.player.update(dt)

            # Projectiles
            for p in self.projectiles:
                p.update(dt)
            # Remove dead projectiles
            self.projectiles = [p for p in self.projectiles if p.life > 0]

            self.wave_manager.update(dt)

            # Combat Checks against Wave Enemies
            for data in self.wave_manager.enemies:
                enemy = data['entity']

                # Projectile Collisions
                for p in self.projectiles:
                    if p.owner == self.player: # Player Shot
                        if p.position.distance_to(enemy.position) < 30:
                            enemy.take_damage(p.damage)
                            self.particles.create_spark(enemy.position.x, enemy.position.y)
                            p.life = 0 # Destroy projectile
                    elif p.owner == enemy: # Enemy shot
                         if p.position.distance_to(self.player.position) < 30:
                            self.player.take_damage(p.damage)
                            p.life = 0

                # Player hits Enemy

                # Player hits Enemy
                if self.player.check_hit(enemy):
                    dmg = int(self.player.weapon.damage * self.player.stats.get_damage_multiplier())
                    enemy.take_damage(dmg)
                    self.particles.create_blood(enemy.position.x, enemy.position.y - 40)
                    self.particles.create_spark(enemy.position.x, enemy.position.y - 40)

                    if enemy.health <= 0:
                        # XP Gain
                        self.player.gain_xp(20)
                        self.quest_manager.on_enemy_killed("enemy")

                # Enemy hits Player
                if enemy.check_hit(self.player):
                    self.player.take_damage(enemy.weapon.damage)
                    self.particles.create_blood(self.player.position.x, self.player.position.y - 40)
                    self.particles.create_spark(self.player.position.x, self.player.position.y - 40)

            # Game Over Check
            if self.player.health <= 0:
                self._reset_game()

    def _reset_game(self):
        stats = CharacterClass.get_starting_stats(CharacterClass.WARRIOR)
        self.player = Stickman(200, GROUND_Y, color=BLACK, stats=stats)
        self.player.equip_weapon(Sword())
        self.player.level = self.level
        self.player.particles = self.particles

        self.wave_manager = WaveManager(self)
        self.particles.particles.clear()

    def draw(self):
        self.screen.fill(WHITE)
        # Draw ground
        pygame.draw.line(self.screen, BLACK, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)

        # Draw Level
        self.level.draw(self.screen)

        # Draw Particles (Behind entities?) or In front
        self.particles.draw(self.screen)

        # Draw Projectiles
        for p in self.projectiles:
            p.draw(self.screen)

        # Draw Entities
        self.player.draw(self.screen)
        self.wave_manager.draw(self.screen)

        # UI
        self.ui.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()
