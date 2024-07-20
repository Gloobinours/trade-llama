import random
from enum import Enum

class CellState(Enum):
    PASSAGE = 0
    WALL = 1
    COIN = 2

class Cell:
    def __init__(self, x: int, y: int,) -> None:
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
        return f"[({self.x}, {self.y}), {self.state}]"


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

    def generate_matrix(self) -> list[Cell]:
        matrix = []
        for x in range(self.size):
            matrix.append([])
            for y in range(self.size):
                cell: Cell = Cell(x, y)
                matrix[x].append(cell)
        return matrix

    def get_neighbors(self, cell: Cell, matrix) -> None:
        """_summary_

        Args:
            cell (Cell): _description_
            matrix (_type_): _description_

        Returns:
            list: list of cells
        """
        directions = [(-2, 0), (2,0), (0, -2), (0, 2)]
        neighbors = []
        for d in directions:
            new_row = cell.x + d[0]
            new_col = cell.y + d[1]

            if (0 <= new_row < self.size) and (0 <= new_col < self.size):
                neighbors.append(matrix[new_row][new_col])

        return neighbors

    def generate_maze_matrix(self) -> list:
        """Generate a square matrix

        Returns:
            np.matrix: _description_
        """
        maze = self.generate_matrix()
        # Choose the initial cell, mark it as visited and push it to the stack
        # random_row: int = random.randint(0, len(maze) - 1)
        # random_col: int = random.randint(0, len(maze[random_row]) - 1)
        random_cell = maze[0][0]
        random_cell.state = CellState.PASSAGE
        visited = [random_cell]
        stack = [random_cell]

        while stack:
            current_cell = stack.pop()
            # List of unvisited neighbors
            unvisited_neighbors :list = [n for n in self.get_neighbors(current_cell, maze) if n not in visited]
            # If the current cell has any neighbours which have not been visited
            if unvisited_neighbors:
                stack.append(current_cell)
                # Choose one of the unvisited neighbours
                chosen_cell = random.choice(unvisited_neighbors)
                # Remove the wall between the current cell and the chosen cell
                in_between_x = current_cell.x + (chosen_cell.x - current_cell.x) // 2
                in_between_y = current_cell.y + (chosen_cell.y - current_cell.y) // 2
                in_between = maze[in_between_x][in_between_y]
                in_between.state = CellState.PASSAGE
                chosen_cell.state = CellState.PASSAGE
                # Mark the chosen cell as visited and push it to the stack
                visited.append(chosen_cell)
                stack.append(chosen_cell)
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

        if len(possible_points) < coin_amount:
            coin_amount = len(possible_points)
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
        return '\n'.join(' '.join(str(cell.state.value) for cell in row) for row in self.maze_mtx)
