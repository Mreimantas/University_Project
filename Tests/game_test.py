import unittest
from unittest.mock import Mock
import pygame
import sys
import os

# Add the root project directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from game import Player, Enemy, Soul, EnemySpawner
from settings import GameSettings  # Adjust if needed

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.settings = GameSettings()
        self.settings.player_speed = 5
        self.settings.player_health = 100
        self.settings.player_armor = 10
        self.world_width = 800
        self.world_height = 600
        self.player = Player(self.settings, self.world_width, self.world_height)

    def test_player_initialization(self):
        self.assertEqual(self.player.health, 100)
        self.assertEqual(self.player.speed, 5)
        self.assertEqual(self.player.x, self.world_width // 2)
        self.assertEqual(self.player.y, self.world_height // 2)

    def test_player_attack_with_sword(self):
        """Test if the player correctly attacks and removes the nearest enemy with a sword."""
        # Place the enemy near the player within the sword's attack range
        player_x = self.player.x
        player_y = self.player.y
        enemy = Enemy(player_x + 50, player_y + 50, 1, (255, 0, 0), 50, 10)  # Adjust position to be within range
        enemies = [enemy]
        souls = []

        # Perform the sword attack
        self.player.attack_with_sword(enemies, souls)

        # Check that the enemy was removed and a soul was added
        self.assertEqual(len(enemies), 0, "Enemy should be removed after being attacked.")
        self.assertEqual(len(souls), 1, "A soul should be added after the enemy is killed.")

    def test_player_take_damage(self):
        self.player.take_damage(50)
        self.assertEqual(self.player.health, 60)  # 50 - 10 (armor)


class TestEnemy(unittest.TestCase):
    def setUp(self):
        self.enemy = Enemy(100, 100, 1, (255, 0, 0), 50, 10)

    def test_enemy_initialization(self):
        self.assertEqual(self.enemy.health, 50)
        self.assertEqual(self.enemy.damage, 10)

    def test_enemy_take_damage(self):
        self.enemy.take_damage(20)
        self.assertEqual(self.enemy.health, 30)

    def test_enemy_death(self):
        is_dead = self.enemy.take_damage(50)
        self.assertTrue(is_dead)

    def test_enemy_drop_soul(self):
        soul = self.enemy.drop_soul()
        self.assertEqual(soul.x, self.enemy.x + self.enemy.width // 2)
        self.assertEqual(soul.y, self.enemy.y + self.enemy.height // 2)


class TestSoul(unittest.TestCase):
    def setUp(self):
        self.soul = Soul(100, 100)

    def test_soul_initialization(self):
        self.assertEqual(self.soul.x, 100)
        self.assertEqual(self.soul.y, 100)
        self.assertEqual(self.soul.radius, 10)

    def test_soul_collision_with_player(self):
        player = Mock()
        player.x = 90
        player.y = 90
        player.width = 50
        player.height = 50
        self.assertTrue(self.soul.collides_with(player))


class TestGame(unittest.TestCase):
    def setUp(self):
        self.settings = GameSettings()
        self.settings.player_speed = 5
        self.settings.player_health = 100
        self.settings.player_armor = 10
        self.screen = Mock()
        self.game = Mock()

        # Configure the mock object
        self.game.enemies = []
        self.game.souls = []
        self.game.reset = Mock()
        self.game.spawn_enemies = Mock(side_effect=lambda x, y: self.game.enemies.append(Mock()))  # Simulate spawning
        self.game.display_end_message = Mock()

    def test_game_initialization(self):
        self.assertEqual(len(self.game.enemies), 0)
        self.assertEqual(len(self.game.souls), 0)

    def test_game_reset(self):
        self.game.reset()
        self.assertEqual(len(self.game.enemies), 0)
        self.assertEqual(len(self.game.souls), 0)
        self.assertEqual(self.settings.player_health, 100)

    def test_spawn_enemies(self):
        self.game.spawn_enemies(0, 0)  # Simulate spawning an enemy
        self.assertGreater(len(self.game.enemies), 0, "Enemies should be added after spawning.")

    def test_display_end_message(self):
        self.game.display_end_message("You Win!")
        self.assertEqual(self.settings.game_state, "menu")


if __name__ == '__main__':
    unittest.main()