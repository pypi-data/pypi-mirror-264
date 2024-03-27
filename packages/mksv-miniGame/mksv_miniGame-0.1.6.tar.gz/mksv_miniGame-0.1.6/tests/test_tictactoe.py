import pytest
import sys
import pygame
from src.minigame import tictactoe

@pytest.fixture
def screen_dimensions():
    return 600, 600

def test_tie_game():
    tictactoe.board = [[1, 2, 1], [1, 2, 2], [2, 1, 1]]
    tictactoe.check_winner()
    assert tictactoe.game_tie == True, "The game is tied."
    assert tictactoe.winner == 0, "The winner is not 0 when it should be."

def test_horizontal_winner():
    tictactoe.board = [[1, 1, 1], [2, 2, 0], [0, 0, 0]]
    tictactoe.check_winner()
    assert tictactoe.game_won == True, "The game is not over when it should be."
    assert tictactoe.winner == 1, "The winner is not 1 when it should be."

def test_vertical_winner():
    tictactoe.board = [[1, 2, 0], [1, 2, 0], [1, 0, 0]]
    tictactoe.check_winner()
    assert tictactoe.game_won == True, "The game is not over when it should be."
    assert tictactoe.winner == 1, "The winner is not 1 when it should be."

def test_diagonal_winner():
    tictactoe.board = [[1, 2, 0], [2, 1, 0], [0, 0, 1]]
    tictactoe.check_winner()
    assert tictactoe.game_won == True, "The game is not over when it should be."
    assert tictactoe.winner == 1, "The winner is not 1 when it should be."


