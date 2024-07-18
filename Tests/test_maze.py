import unittest
from src import Maze
from src import main

class TestMazeMethod(unittest.TestCase):
    def test_generate_maze(self):
        self.assertEqual(True)

    def test_generate_coins(self):
        maze: Maze.Maze = Maze.Maze(10, 3)
        coins = maze.generate_coins()
        print(coins)