from enum import Enum
from Player import Player
from Maze import Maze

class GameLoop:
    def __init__(self, player: Player, maze: Maze) -> None:
        """Constructor for GameLoop

        Args:
            player (Player): player playing the game
            maze (Maze): maze generated for the game
        """
        self.player: Player = player
        self.maze: Maze = maze
        self.action: str = None
        self.is_step_called: bool = False
        self.has_ended: bool = False
    
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

            if self.action =='UP':
                self.player.move_up()
            elif self.action == 'RIGHT':
                self.player.move_right()
            elif self.action =='DOWN':
                self.player.move_down()
            elif self.action =='LEFT':
                self.player.move_left()
            elif self.action =='BOMB':
                self.player.use_bomb()
            else:
                print('Invalid action')
            print(f'move player to: ({self.player.x}, {self.player.y})')

            self.player.touching_coin()

            if self.player.all_coins_collected():
                print("All coins collected")
                self.has_ended = True
                break
            
            while True:
                if self.is_step_called == True:
                    self.is_step_called = False
                    break
                
    def reset(self, seed):
        self.maze = Maze(self.maze.size, self.maze.coin_amount, seed)
        state = {
            'player_position' : (self.player.x, self.player.y),
            'player_vision' : self.maze.generate_fog(self.player.x, self.player.y, self.fog_size),
            'all_coins_collected' : self.player.all_coins_collected(),
            'nearest_coin' : self.player.get_nearest_coin()
            }
        return state
    
    def step(self, action):
        self.is_step_called = True
        self.action = action
        state = {
            'player_position' : (self.player.x, self.player.y),
            'player_vision' : self.maze.generate_fog(self.player.x, self.player.y, self.fog_size),
            'all_coins_collected' : self.player.all_coins_collected(),
            'nearest_coin' : self.player.get_nearest_coin()
            }
        ### None is placeholder
        return(state, None, self.has_ended, None)
        