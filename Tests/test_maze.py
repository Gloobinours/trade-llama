import unittest
import Maze

class TestMazeMethod(unittest.TestCase):
    def test_generate_maze(self):
        self.assertEqual(True)

    def test_generate_coins(self):
        maze: Maze.Maze = Maze.Maze(10, 3)
        coins = maze.generate_coins()
        print(coins)

    def test_explode_bomb(self):

        mtx = [[1 for y in range(0, 2)] for x in range(0, 2)]
        goal = [[0 for y in range(0, 2)] for x in range(0, 2)]
        x, y = 1
        for i in range(x-1,x+1):
            for j in range(y-1,y+1):
                if (i > 0 or j > 0) and (y >= self.size or x >= self.size):
                    if mtx[i][j] == 1:
                        mtx[i][j] = 0
        self.assertEqual(mtx, goal)