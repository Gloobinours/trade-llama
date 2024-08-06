from collections import deque, namedtuple
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
import dqlearning
import torch.optim as optim
from Game import GameLoop
import Maze
import Player

# if GPU is to be used
device = torch.device(
    "cuda" if torch.cuda.is_available() else
    "mps" if torch.backends.mps.is_available() else
    "cpu"
)

Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))

class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        """Select a random batch of transitions for training

        Args:
            batch_size (_type_): _description_

        Returns:
            _type_: _description_
        """
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)
    
class DeepQNetwork(nn.Module):
    def __init__(self, n_observations, n_actions):
        super(DeepQNetwork, self).__init__()
        self.layer1 = nn.Linear(n_observations, 64)
        self.layer2 = nn.Linear(64, 64)
        self.layer3 = nn.Linear(64, n_actions)

    def forward(self, x):
        """Called with either one element to determine next action,
        or a batch during optimization

        Args:
            x (_type_): _description_

        Returns:
            tensor([[left0exp,right0exp]...]): Tensor
        """
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.layer3(x)
    
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

