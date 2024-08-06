from collections import deque, namedtuple
import math
import random
import matplotlib
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from Game import GameLoop
import Maze
from Player import Player

# set up matplotlib
is_ipython = 'inline' in matplotlib.get_backend()
if is_ipython:
    from IPython import display

plt.ion()

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

BATCH_SIZE = 128 # the number of transitions sampled from the replay buffer
GAMMA = 0.99 # discount factor
EPS_START = 0.9 # the starting value of epsilon
EPS_END = 0.05 # the final value of epsilon
EPS_DECAY = 1000 # controls the rate of exponential decay of epsilon, higher means a slower decay
TAU = 0.005 # the update rate of the target network
LR = 1e-4 # the learning rate of the ``AdamW`` optimizer

# Init the game
maze: Maze = Maze.Maze(15, 1)
player: Player = Player(0, 0, maze)
gameloop: GameLoop = GameLoop(player, maze)
fog_size = 2

actions = ['UP', 'RIGHT', 'DOWN', 'LEFT', 'BOMB']

n_actions = len(actions) # number of actions (TOP,RIGHT,DOWN,LEFT,BOMB)
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

policy_net = DeepQNetwork(n_observations, n_actions).to(device)
target_net = DeepQNetwork(n_observations, n_actions).to(device)
target_net.load_state_dict(policy_net.state_dict())

optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
memory = ReplayMemory(10000)


steps_done = 0


def select_action(state):
    global steps_done
    sample = random.random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * \
        math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1
    if sample > eps_threshold:
        with torch.no_grad():
            # t.max(1) will return the largest column value of each row.
            # second column on max result is index of where max element was
            # found, so we pick action with the larger expected reward.
            return policy_net(state).max(1).indices.view(1, 1)
    else:
        return torch.tensor([[random.choice(actions)]], device=device, dtype=torch.long)
    
episode_durations = []

def plot_durations(show_result=False):
    plt.figure(1)
    durations_t = torch.tensor(episode_durations, dtype=torch.float)
    if show_result:
        plt.title('Result')
    else:
        plt.clf()
        plt.title('Training...')
    plt.xlabel('Episode')
    plt.ylabel('Duration')
    plt.plot(durations_t.numpy())
    # Take 100 episode averages and plot them too
    if len(durations_t) >= 100:
        means = durations_t.unfold(0, 100, 1).mean(1).view(-1)
        means = torch.cat((torch.zeros(99), means))
        plt.plot(means.numpy())

    plt.pause(0.001)  # pause a bit so that plots are updated
    if is_ipython:
        if not show_result:
            display.display(plt.gcf())
            display.clear_output(wait=True)
        else:
            display.display(plt.gcf())
