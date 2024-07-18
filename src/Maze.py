import numpy as np
import random

class Maze:

    def __init__(self, size: int, coin_amount : int) -> None:
        """Constructor for Maze

        Args:
            size (int): _description_
            coin_amount (int): _description_
        """
        self.size: int = size
        self.coin_amount = coin_amount
        self.maze_mtx : np.matrix = self.generate_matrix()
        self.add_coin_to_maze(coin_amount)

    def generate_matrix(self) -> np.matrix:
        """Generate a square maze."""
        maze = np.ones((self.size, self.size), dtype=int)
        start = (0, 0)
        end = (self.size - 1, self.size - 1)
        maze[start] = 0  # Start point
        stack = [start]
        while stack:
            current = stack[-1]
            maze[current] = 0
            neighbors = []
            row, col = current
            if row > 1 and maze[row - 2, col] == 1:
                neighbors.append((row - 2, col))
            if row < self.size - 2 and maze[row + 2, col] == 1:
                neighbors.append((row + 2, col))
            if col > 1 and maze[row, col - 2] == 1:
                neighbors.append((row, col - 2))
            if col < self.size - 2 and maze[row, col + 2] == 1:
                neighbors.append((row, col + 2))
            if neighbors:
                next_cell = random.choice(neighbors)
                wall_between = ((current[0] + next_cell[0]) // 2, (current[1] + next_cell[1]) // 2)
                maze[wall_between] = 0
                stack.append(next_cell)
            else:
                stack.pop()
        
        # Ensure the exit is connected
        row, col = end
        while maze[row, col] == 1:
            if row > 0 and maze[row - 1, col] == 0:
                maze[row, col] = 0
                break
            if col > 0 and maze[row, col - 1] == 0:
                maze[row, col] = 0
                break
            if maze[row - 1, col] == 1 and maze[row, col - 1] == 1:
                if random.choice([True, False]):
                    maze[row - 1, col] = 0
                else:
                    maze[row, col - 1] = 0
            row -= 1
            col -= 1
        
        maze[end] = 0  # Ensure exit point is 0

        return maze
    
    def check_adjacent(self, row, col) -> bool:
        """return true if excatly 3 adjacent wall to point

        Args:
            row (_type_): _description_
            col (_type_): _description_

        Returns:
            bool: _description_
        """
        rows = len(self.maze_mtx)
        cols = len(self.maze_mtx[0])

        directions = [(-1, 0), (1,0), (0, -1), (0, 1)]

        count_walls = 0

        for d in directions:
            new_row = row + d[0]
            new_col = col + d[1]

            if (0 <= new_row < rows) and (0 <= new_col < cols) and (self.maze_mtx[new_row][new_col] == 1):
                count_walls += 1
        
        return count_walls == 3