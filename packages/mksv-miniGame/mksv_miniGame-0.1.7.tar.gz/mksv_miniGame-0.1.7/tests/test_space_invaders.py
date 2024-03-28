import pygame
import sys
from src.minigame import space_invaders
import pytest

@pytest.fixture
def screen_dimensions():
    return 800, 600

# test that enemies are spawned
def test_generate_enemies_count(screen_dimensions):
    screen_width, screen_height = screen_dimensions
    for _ in range(1000):
        enemies = space_invaders.spawn_enemy()
        assert len(enemies) >= 1, "The generate_enemies function creates enemies < 1"

# test that the enemies are spawned within the game boundaries (width)
def test_generate_enemies_within_boundaries(): 
    screen_width, screen_height = 800, 600
    for _ in range(1000):
        enemies = space_invaders.spawn_enemy()
        for enemy in enemies:
            assert 0 <= enemy[0] <= screen_width, "Enemy x-coordinate is out of screen boundaries."

# test if enemy block is removed when it passes screen height
def test_enemy_removal_when_passed_height(screen_dimensions):
    screen_width, screen_height = screen_dimensions
    for _ in range(1000):
        enemy_x = screen_width // 2
        enemy_y = screen_height + 1  
        space_invaders.enemies = [[enemy_x, enemy_y]]  

        for enemy in space_invaders.enemies:
            enemy[1] += 3.5

        space_invaders.enemies = [enemy for enemy in space_invaders.enemies if enemy[1] <= screen_height]
        assert len(space_invaders.enemies) == 0, "Enemy block failed to get removed when passing screen height"


# test collision between player and enemy blocks
def test_collision_detection(screen_dimensions):
    screen_width, screen_height = screen_dimensions
    for _ in range(1000):
        player_x = screen_width // 2
        player_y = screen_height - 100
        enemy_x = player_x  
        enemy_y = player_y  
        space_invaders.enemies = [[enemy_x, enemy_y]]  
        space_invaders.game_active = True

        for enemy in space_invaders.enemies:
            if enemy[1] > screen_height:
                space_invaders.enemies.remove(enemy)
            elif (player_x < enemy[0] + 40 and
                player_x + 50 > enemy[0] and
                player_y < enemy[1] + 40 and
                player_y + 50 > enemy[1]):
                space_invaders.game_active = False

        assert not space_invaders.game_active, "Collision detection failed to end the game"

