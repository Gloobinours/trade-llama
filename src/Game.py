from enum import Enum
from Player import Player
from Maze import Maze
import dqlearning
import torch.optim as optim

class GameLoop:
    def __init__(self, player: Player, maze: Maze) -> None:
        """Constructor for GameLoop

        Args:
            player (Player): player playing the game
            maze (Maze): maze generated for the game
        """
        self.player: Player = player
        self.maze: Maze = maze
    
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
            action = input("take action $> ").upper()

            if action =='UP':
                self.player.move_up()
            elif action == 'RIGHT':
                self.player.move_right()
            elif action =='DOWN':
                self.player.move_down()
            elif action =='LEFT':
                self.player.move_left()
            elif action =='BOMB':
                self.player.use_bomb()
            else:
                print('Invalid action')
            print(f'move player to: ({self.player.x}, {self.player.y})')

            self.player.touching_coin()

            if self.player.all_coins_collected():
                print("All coins collected")
                break


if __name__ == '__main__':
    # Init the game
    maze: Maze = Maze(15, 1)
    player: Player = Player(0, 0, maze)
    gameloop: GameLoop = GameLoop(player, maze)

    BATCH_SIZE = 128 # the number of transitions sampled from the replay buffer
    GAMMA = 0.99 # discount factor
    EPS_START = 0.9 # the starting value of epsilon
    EPS_END = 0.05 # the final value of epsilon
    EPS_DECAY = 1000 # controls the rate of exponential decay of epsilon, higher means a slower decay
    TAU = 0.005 # the update rate of the target network
    LR = 1e-4 # the learning rate of the ``AdamW`` optimizer

    fog_size = 2
    fog_cells = maze.generate_fog(player.x, player.y, fog_size)
    print([str(cell) for cell in fog_cells])

    n_actions = 5 # number of actions (TOP,RIGHT,DOWN,LEFT,BOMB)
    state = {
        'player_position' : (player.x, player.y),
        'player_vision' : maze.generate_fog(player.x, player.y, fog_size),
        'all_coins_collected' : player.all_coins_collected(),
        'nearest_coin' : player.get_nearest_coin()
    }

    player_position_features = 2
    player_vision_features = 8 if fog_size == 1 else (fog_size**2+1)**2
    all_coins_collected_features = 1
    nearest_coin_features = 2

    # Number of observations
    n_observations = (player_position_features + player_vision_features + all_coins_collected_features + nearest_coin_features)

    policy_net = dqlearning.DQN(n_observations, n_actions).to(dqlearning.device)
    target_net = dqlearning.DQN(n_observations, n_actions).to(dqlearning.device)
    target_net.target_net.load_state_dict(policy_net.state_dict())

    optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
    memory = dqlearning.ReplayMemory(10000)

