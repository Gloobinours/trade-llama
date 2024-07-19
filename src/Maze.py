import random
from enum import Enum

class CellState(Enum):
    PASSAGE = 0
    WALL = 1
    COIN = 2

    def __str__(self) -> str:
        return f"{self.value}"

class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.state: CellState = CellState.WALL

    def change_state_to_wall(self):
        self.state = CellState.WALL
    def change_state_to_coin(self):
        self.state = CellState.COIN

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y
    def __str__(self) -> str:
        return f"{self.state}"


class Maze:
    def __init__(self, size: int, coin_amount : int) -> None:
        """Constructor for Maze

        Args:
            size (int): _description_
            coin_amount (int): _description_
        """
        self.size: int = size
        self.coin_amount: int = coin_amount
        self.maze_mtx = self.generate_maze_matrix()
        self.coin_list = []
        self.add_coin_to_maze(coin_amount)

    def generate_matrix(self) -> list:
        matrix = []
        for x in range(self.size):
            matrix.append([])
            for y in range(self.size):
                cell: Cell = Cell(x, y)
                matrix[x].append(cell)
        return matrix

    def generate_maze_matrix(self) -> list:
        """Generate a square matrix

        Returns:
            np.matrix: _description_
        """
        maze = self.generate_matrix()
        start = Cell(0,0)
        end = Cell(self.size - 1, self.size - 1)
        maze[start.x][start.y] = CellState.PASSAGE  # Start point
        stack = [start]
        while stack:
            current = stack[-1]
            maze[current.x][current.y].state = CellState.PASSAGE
            neighbors = []
            row, col = current.x, current.y
            if row > 1 and maze[row - 2][col].state == CellState.WALL:
                neighbors.append(maze[row - 2][col])
            if row < self.size - 2 and maze[row + 2][col].state == CellState.WALL:
                neighbors.append(maze[row + 2][col])
            if col > 1 and maze[row][col - 2].state == CellState.WALL:
                neighbors.append(maze[row][col - 2])
            if col < self.size - 2 and maze[row][col + 2].state == CellState.WALL:
                neighbors.append(maze[row][col + 2])
            if neighbors:
                next_cell = random.choice(neighbors)
                wall_between = maze[(current.x + next_cell.x) // 2][(current.y + next_cell.y) // 2]
                maze[wall_between.x][wall_between.y].state = CellState.PASSAGE
                stack.append(next_cell)
            else:
                stack.pop()
        
        # Ensure the exit is connected
        row, col = end.x, end.y
        while maze[row][col].state == CellState.WALL:
            if row > 0 and maze[row - 1][col].state == CellState.PASSAGE:
                maze[row][col].state = CellState.PASSAGE
                break
            if col > 0 and maze[row][col - 1].state == CellState.PASSAGE:
                maze[row][col].state = CellState.PASSAGE
                break
            if maze[row - 1][col].state == CellState.WALL and maze[row][col - 1].state == CellState.WALL:
                if random.choice([True, False]):
                    maze[row - 1][col].state = CellState.PASSAGE
                else:
                    maze[row][col - 1].state = CellState.PASSAGE
            row -= 1
            col -= 1
        
        maze[end.x][end.y].state = CellState.PASSAGE  # Ensure exit point is a passage

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

            if (0 <= new_row < rows) and (0 <= new_col < cols) and (self.maze_mtx[new_row][new_col].state == CellState.WALL):
                count_walls += 1
        
        return count_walls == 3
    
    def generate_coins(self, coin_amount) -> list:
        """Generate coins when 3 walls around

        Args:
            coin_amount (_type_): _description_

        Returns:
            list: _description_
        """
        possible_points = []
        for x in range(len(self.maze_mtx)):
            for y in range(len(self.maze_mtx[0])):
                if (self.check_adjacent(x, y) and self.maze_mtx[x][y].state == CellState.PASSAGE):
                    possible_points.append((x,y))

        return random.sample(possible_points, coin_amount)
    
    def add_coin_to_maze(self, coin_amount) -> None:
        """Append coins to maze matrix

        Args:
            coin_amount (_type_): _description_
        """
        coin_pos = self.generate_coins(coin_amount)
        for x in range(len(self.maze_mtx)):
            for y in range(len(self.maze_mtx[0])):
                for pos in coin_pos:
                    if (x == pos[0] and y == pos[1]):
                        self.maze_mtx[x][y].state = CellState.COIN
                        self.coin_list.append(self.maze_mtx[x][y])
    
    def __str__(self) -> str:
        return '\n'.join(' '.join(str(cell) for cell in row) for row in self.maze_mtx)
