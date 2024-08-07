from enum import Enum
from Player import Player
from Maze import Maze

class Action(Enum):
    BOMB = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

class GameLoop:
    def __init__(self, player: Player, maze: Maze, fog_size: int = 1) -> None:
        """Constructor for GameLoop

        Args:
            player (Player): player playing the game
            maze (Maze): maze generated for the game
        """
        self.player: Player = player
        self.maze: Maze = maze
        self.action: Action = None
        self.is_step_called: bool = False
        self.has_ended: bool = False
        self.reward = 0
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

    def loop(self) -> None:
        """Main game loop function
        """
        while True:
            self.draw_maze()

            if self.action == Action.UP:
                if self.player.move_up() == False:
                    reward -= 5
            elif self.action == Action.RIGHT:
                if self.player.move_right() == False:
                    reward -= 5
            elif self.action == Action.DOWN:
                if self.player.move_down() == False:
                    reward -= 5
            elif self.action == Action.LEFT:
                if self.player.move_left() == False:
                    reward -= 5
            elif self.action == Action.BOMB:
                self.player.use_bomb
            else:
                print('Invalid action')
            print(f'move player to: ({self.player.x}, {self.player.y})')

            if self.player.touching_coin():
                self.reward += 10

            if self.player.all_coins_collected():
                print("All coins collected")
                self.reward += 50
                self.has_ended = True
                break
            
            while True:
                if self.is_step_called == True:
                    self.is_step_called = False
                    break
                
    def reset(self, seed):
        self.maze = Maze(self.maze.size, self.maze.coin_amount, seed)
        self.reward = 0
        self.player.x = 0
        self.player.y = 0
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
    
    def step(self, action):
        self.is_step_called = True
        self.action = action
        self.reward -= 0.1
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

        return(state, self.reward, self.has_ended)
        