import math
import numpy as np
from enum import Enum
from Player import Player
from Maze import Maze, Cell, CellState

class Action(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    # BOMB = 4

class GameLoop:
    def __init__(self, player: Player, maze: Maze, fog_size: int = 1) -> None:
        """Constructor for GameLoop

        Args:
            player (Player): player playing the game
            maze (Maze): maze generated for the game
        """
        self.player: Player = player
        self.maze: Maze = maze
        self.fog_size: int = fog_size
        self.visited_cells: list[Cell] = []
    
    def draw_maze(self) -> None:
        """Draws the player on the maze
        """
        new_maze = []
        for x in range(self.maze.size):
            row = []
            for y in range(self.maze.size):
                if x == self.player.x and y == self.player.y:
                    row.append('\033[34m#\033[0m')
                elif self.maze.grid[x][y].state == CellState.PASSAGE:
                    row.append(' ')
                elif self.maze.grid[x][y].state == CellState.WALL:
                    row.append('■')
                elif self.maze.grid[x][y].state == CellState.COIN:
                    row.append('\033[33m©\033[0m')
            new_maze.append(row)
        
        print('■ '*(self.maze.size))
        for row in new_maze:
            print(' '.join(row))
        print('■ '*(self.maze.size))

    def step(self, action):
        """Makes a step in the main game loop

        Args:
            action (_type_): _description_
        """
        # self.draw_maze()
        # print('<------------------------------------>')

        reward = 0
        is_done = False

        # print("Action: ", action, ", ", Action(action).name)
        if (action == Action.UP) or (action == Action.UP.value):
            if self.player.move_up() == False:
                reward -= 10
        elif (action == Action.RIGHT) or (action == Action.RIGHT.value):
            if self.player.move_right() == False:
                reward -= 10
        elif (action == Action.DOWN) or (action == Action.DOWN.value):
            if self.player.move_down() == False:
                reward -= 10
        elif (action == Action.LEFT) or (action == Action.LEFT.value):
            if self.player.move_left() == False:
                reward -= 10
        # elif (action == Action.BOMB) or (action == Action.BOMB.value):
        #     self.player.use_bomb
        # else:
        #     print('Invalid action')
        # print(f'move player to: ({self.player.x}, {self.player.y})')


        # Reward points when agent visits unvisited cells
        if self.maze.grid[self.player.x][self.player.y].visited == False:
            reward += 2
            self.maze.grid[self.player.x][self.player.y].visited = True
        else:
            reward -= 1

        # Punishment for each step
        reward -= 0.5

        if self.player.touching_coin() == True:
            self.reward += 100
        # else:
        #     # Subtract points when agent gets further from closest coin
        #     nearest = self.player.get_nearest_coin()
        #     dist = math.dist([self.player.x, self.player.y], [nearest.x, nearest.y])
        #     reward -= dist * 0.1
        # print([str(c) for c in self.maze.coin_list], ", Amount: ", self.maze.coin_amount)

        if self.player.all_coins_collected():
            print("All coins collected")
            reward += 300
            is_done = True


        # print('Reward: ', reward)

        if is_done == False:
            self.state = self.get_state()
        return self.state, reward, is_done

    def get_state(self) -> np.array:
        """State at step t, what the player is aware of

        Returns:
            np.array: state
        """
        state = [
            self.player.x, 
            self.player.y,
            int(self.player.all_coins_collected()),
            self.player.get_nearest_coin().x,
            self.player.get_nearest_coin().y,
            self.player.get_nearest_coin().state.value
        ]
        for cell in self.maze.generate_fog(self.player.x, self.player.y, self.fog_size):
            state.append(cell.x - self.player.x)
            state.append(cell.y - self.player.y)
            state.append(cell.state.value)
            # state.append(int(cell.visited))
            
        max_visited_cells = len(self.maze.get_passages())
        visited_cells = self.visited_cells[:max_visited_cells]
        for cell in visited_cells:
            state.append(cell.x - self.player.x)
            state.append(cell.y - self.player.y)
            state.append(cell.state.value)
        
        # Fill the remaining slots if there are
        for _ in range(max_visited_cells - len(visited_cells)):
            state.extend([-1, -1, -1])

        return np.array(state)
                
    def reset(self, seed: int = None) -> list[int]:
        """Rests the maze to initial step

        Args:
            seed (int): seed of the maze

        Returns:
            list[int]: State of the game
        """
        self.reward = 0
        self.player.x = 0
        self.player.y = 0
        self.maze = Maze(self.maze.size, self.maze.coin_amount, seed)
        self.player.maze = self.maze
        self.state = self.get_state()

        return self.state