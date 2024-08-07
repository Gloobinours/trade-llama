import threading
from enum import Enum
from Player import Player
from Maze import Cell, Maze

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
        self.fog_size = fog_size
            
    def draw_maze(self) -> None:
        """Draws the player on the maze
        """
        new_maze = []
        for x in range(self.maze.size):
            row = []
            for y in range(self.maze.size):
                if x == self.player.x and y == self.player.y:
                    row.append('#')
                else:
                    row.append(str(self.maze.grid[x][y].state.value))
            new_maze.append(row)
        
        for row in new_maze:
            print(' '.join(row))

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
                reward -= 5
            else:
                reward += 10
        elif (action == Action.RIGHT) or (action == Action.RIGHT.value):
            if self.player.move_right() == False:
                reward -= 5
            else:
                reward += 10
        elif (action == Action.DOWN) or (action == Action.DOWN.value):
            if self.player.move_down() == False:
                reward -= 5
            else:
                reward += 10
        elif (action == Action.LEFT) or (action == Action.LEFT.value):
            if self.player.move_left() == False:
                reward -= 5
            else:
                reward += 10
        # elif (action == Action.BOMB) or (action == Action.BOMB.value):
        #     self.player.use_bomb
        # else:
        #     print('Invalid action')
        # print(f'move player to: ({self.player.x}, {self.player.y})')
            
        # Reward points when agent visits unvisited cells
        if self.maze.grid[self.player.x][self.player.y].visited == False:
            reward += 1
            self.maze.grid[self.player.x][self.player.y].visited = True             
            
        reward -= 1

        if self.player.touching_coin() == True:
            self.reward += 50000
        # print([str(c) for c in self.maze.coin_list], ", Amount: ", self.maze.coin_amount)

        if self.player.all_coins_collected():
            print("All coins collected")
            reward += 100000
            is_done = True

        # print('Reward: ', reward)

        self.state = self.get_state()
        return self.state, reward, is_done

    def get_state(self):
        if self.maze.coin_list:
            x_coin_state = self.player.get_nearest_coin().x
            y_coin_state = self.player.get_nearest_coin().y

        state = [
            self.player.x, 
            self.player.y,
            int(self.player.all_coins_collected())
        ]
        
        if x_coin_state != None:
            state.append(x_coin_state)
        else:
            state.append(0)
        if y_coin_state != None:
            state.append(y_coin_state)
        else:
            state.append(0)
            
        for cell in self.maze.generate_fog(self.player.x, self.player.y, self.fog_size):
            state.append(cell.x)
            state.append(cell.y)

        return state
                
    def reset(self, seed: int) -> list[int]:
        """Rests the maze to initial step

        Args:
            seed (int): seed of the maze

        Returns:
            list[int]: State of the game
        """
        self.maze = Maze(self.maze.size, self.maze.coin_amount, seed)
        self.reward = 0
        self.player.x = 0
        self.player.y = 0
        self.state = self.get_state()

        return self.state