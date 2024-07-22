from Maze import Maze, Cell, CellState
import math

class Player:

    def __init__(self, x: int, y: int, maze: Maze) -> None:
        self.x: int = x
        self.y: int = y
        self.maze: Maze = maze

    def is_walkable(self, x: int, y: int) -> bool:
        """ Check if a cell in the maze is walkable given its coordinates

        Args:
            x (int): The x-coordinate of the cell
            y (int): The y-coordinate of the cell

        Returns:
            bool: False if the cell is not walkable (wall or out of bounds),
                True if the cell is walkable (passage or coin)
        """
        if (y < 0 or y >= self.maze.size): 
            print(f"Out of bounds: ({x}, {y})")
            return False
        if (x < 0 or x >= self.maze.size): 
            print(f"Out of bounds: ({x}, {y})")
            return False
        
        if self.maze.grid[x][y].state == CellState.WALL:
            print(f"Wall at: ({x}, {y})")
            return False
        
        # The cell is walkable
        return True

    def move_left(self):
        if (self.is_walkable(self.x-1, self.y)):
            self.x -= 1
    def move_right(self):
        if (self.is_walkable(self.x+1, self.y)):
            self.x += 1
    def move_up(self):
        if (self.is_walkable(self.x, self.y-1)):
            self.y -= 1
    def move_down(self):
        if (self.is_walkable(self.x, self.y+1)):
            self.y += 1

    def get_nearest_coin(self) -> Cell:
        closest_dist = -1
        for coin in self.maze.coin_list:
            dist = math.dist([self.x, self.y], [coin.x, coin.y])
            if (closest_dist == 1):
                closest_dist = dist
                closest_coin = coin
                continue
            if (dist < closest_dist):
                closest_dist = dist
                closest_coin = coin
        return closest_coin
    
    def all_coins_collected(self) -> bool:
        return len(self.maze.coin_list) == 0
    
    def touching_coin(self) -> None:
        if self.maze.grid[self.x][self.y].state == CellState.COIN:
            self.maze.delete_coin(self.x, self.y)
