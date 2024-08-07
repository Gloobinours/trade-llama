import threading
from enum import Enum
from Player import Player
from Maze import Maze

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
                reward -= 1
            else:
                reward += 1
        elif (action == Action.RIGHT) or (action == Action.RIGHT.value):
            if self.player.move_right() == False:
                reward -= 1
        elif (action == Action.DOWN) or (action == Action.DOWN.value):
            if self.player.move_down() == False:
                reward -= 1
            else:
                reward += 1
        elif (action == Action.LEFT) or (action == Action.LEFT.value):
            if self.player.move_left() == False:
                reward -= 1
            else:
                reward += 1
        # elif (action == Action.BOMB) or (action == Action.BOMB.value):
        #     self.player.use_bomb
        # else:
        #     print('Invalid action')
        # print(f'move player to: ({self.player.x}, {self.player.y})')


        # Subtract points when agent goes back on visited cell
        if Cell(self.player.x, self.player.y) not in self.visited_cells:
            self.visited_cells.append(Cell(self.player.x, self.player.y))
        else:
            reward -= 0.4

        reward -= 0.1

        if self.player.touching_coin() == True:
            self.reward += 20
        else:
            # Subtract points when agent gets further from closest coin
            nearest = self.player.get_nearest_coin()
            dist = math.dist([self.player.x, self.player.y], [nearest.x, nearest.y])
            reward -= dist * 0.1
        # print([str(c) for c in self.maze.coin_list], ", Amount: ", self.maze.coin_amount)

        if self.player.all_coins_collected():
            print("All coins collected")
            reward += 50
            is_done = True

        # print('Reward: ', reward)

        self.state = self.get_state()
        return self.state, reward, is_done

    def get_state(self):
        state = [
            self.player.x, 
            self.player.y,
            int(self.player.all_coins_collected()),
            self.player.get_nearest_coin().x,
            self.player.get_nearest_coin().y
        ]
        for cell in self.maze.generate_fog(self.player.x, self.player.y, self.fog_size):
            state.append(cell.x)
            state.append(cell.y)

        return state
                
    def reset(self, seed: int = None) -> list[int]:
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
        