import numpy as np
import random

class Maze:

    def __init__(self, size: int) -> None:
        """Maze constructor.
        size : int
            size of the maze
        """
        self.size: int = size
        self.maze_mtx : np.matrix = self.generateMaze()

    def generateMaze(self) -> np.matrix:
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