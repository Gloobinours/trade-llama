from collections import deque, namedtuple
from itertools import count
import math
import random
import matplotlib
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from Game import GameLoop, Action
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
        self.layer1 = nn.Linear(n_observations, 128)
        self.layer2 = nn.Linear(128, 128)
        self.layer3 = nn.Linear(128, n_actions)

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


class DQNAgent:
    def __init__(self, batch_size, gamma, eps_start, eps_end, eps_decay, tau, learning_rate) -> None:
        self.batch_size = batch_size
        self.gamma = gamma
        self.eps_start = eps_start
        self.eps_end = eps_end
        self.eps_decay = eps_decay
        self.tau = tau
        self.learning_rate = learning_rate
        self.policy_net = DeepQNetwork(self.get_n_observations(fog_size), self.get_n_actions()).to(device)
        self.target_net = DeepQNetwork(self.get_n_observations(fog_size), self.get_n_actions()).to(device)
        self.update_target_network()
        self.optimizer = optim.AdamW(self.policy_net.parameters(), lr=LR, amsgrad=True)
        self.memory = ReplayMemory(10000)
        self.steps_done = 0
    
    def update_target_network(self):
        """Step 2: Makes policy and target network the same
        """
        self.target_net.load_state_dict(self.policy_net.state_dict())

    def get_n_observations(self, fog_size):
        player_position_features = 2
        all_coins_collected_features = 1
        nearest_coin_features = 2
        player_vision_features = 8*2 if fog_size == 1 else ((fog_size*2+1)**2)*2
        return (player_position_features + player_vision_features + all_coins_collected_features + nearest_coin_features)

    def get_n_actions(self):
        return len(Action)
    
    def select_action(self, state):
        """Select action using Epsilon-Greedy algorithm

        Args:
            state (_type_): _description_

        Returns:
            torch.tensor: _description_
        """
        self.eps_threshold = self.eps_end + (self.eps_start - self.eps_end) * \
            math.exp(-1. * self.steps_done / self.eps_decay)
        self.steps_done += 1
        if random.random() > self.eps_threshold:
            # Select best action
            with torch.no_grad():
                return self.policy_net(state).max(1).indices.view(1, 1)
        else:
            # Select random action
            return torch.tensor([[random.choice(actions).value]], device=device, dtype=torch.long)
        
    def optimize_model(self):
        if len(self.memory) < self.batch_size:
            return
        transitions = self.memory.sample(self.batch_size)
        # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
        # detailed explanation). This converts batch-array of Transitions
        # to Transition of batch-arrays.
        batch = Transition(*zip(*transitions))

        # Compute a mask of non-final states and concatenate the batch elements
        # (a final state would've been the one after which simulation ended)
        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                            batch.next_state)), device=device, dtype=torch.bool)
        non_final_next_states = torch.cat([s for s in batch.next_state
                                                    if s is not None])
        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)

        # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
        # columns of actions taken. These are the actions which would've been taken
        # for each batch state according to policy_net
        state_action_values = self.policy_net(state_batch).gather(1, action_batch)

        # Compute V(s_{t+1}) for all next states.
        # Expected values of actions for non_final_next_states are computed based
        # on the "older" target_net; selecting their best reward with max(1).values
        # This is merged based on the mask, such that we'll have either the expected
        # state value or 0 in case the state was final.
        next_state_values = torch.zeros(self.batch_size, device=device)
        with torch.no_grad():
            next_state_values[non_final_mask] = self.target_net(non_final_next_states).max(1).values
        # Compute the expected Q values
        expected_state_action_values = (next_state_values * GAMMA) + reward_batch

        # Compute Huber loss
        criterion = nn.SmoothL1Loss()
        loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()
        # In-place gradient clipping
        torch.nn.utils.clip_grad_value_(self.policy_net.parameters(), 100)
        self.optimizer.step()
    

BATCH_SIZE = 128 # the number of transitions sampled from the replay buffer
GAMMA = 0.99 # discount factor
EPS_START = 1.0 # the starting value of epsilon
EPS_END = 0.01 # the final value of epsilon
EPS_DECAY = 10000 # controls the rate of exponential decay of epsilon, higher means a slower decay
TAU = 0.005 # the update rate of the target network
LR = 1e-4 # the learning rate of the ``AdamW`` optimizer

# Init the game - TRAINING AGENT
maze: Maze = Maze.Maze(9, 5, a_seed= 1)
player: Player = Player(0, 0, maze)
fog_size = 2
gameloop: GameLoop = GameLoop(player, maze, fog_size = fog_size)

actions = [Action.UP, Action.RIGHT, Action.DOWN, Action.LEFT]

agent = DQNAgent(BATCH_SIZE, GAMMA, EPS_START, EPS_END, EPS_DECAY, TAU, LR)


   
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

if torch.cuda.is_available() or torch.backends.mps.is_available():
    num_episodes = 600
else:
    num_episodes = 60

step_count = 0

for i_episode in range(num_episodes):
    # Initialize the environment and get its state
    state = gameloop.reset(10)
    state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
    truncated = False # True when agent takes more than n actions
    terminated = False # True when agent gets all coins
    total_reward = 0

    t = 0
    # Agent naviguates the maze until truncated or terminated
    for _ in range(10000):

        # print(" Step: ", step_count)
        # Select action using Epsilon-Greedy Algorithm
        action = agent.select_action(state)

        # Execute action
        observation, reward, terminated = gameloop.step(action.item())
        reward = torch.tensor([reward], device=device)
        done = terminated

        if terminated:
            next_state = None
        else:
            next_state = torch.tensor(observation, dtype=torch.float32, device=device).unsqueeze(0)

        total_reward += reward

        # Store the transition in memory (save experience in memory)
        agent.memory.push(state, action, next_state, reward)

        # Move to the next state
        state = next_state

        # Perform one step of the optimization (on the policy network)
        agent.optimize_model()

        # Soft update of the target network's weights
        # θ′ ← τ θ + (1 −τ )θ′
        target_net_state_dict = agent.target_net.state_dict()
        policy_net_state_dict = agent.policy_net.state_dict()
        for key in policy_net_state_dict:
            target_net_state_dict[key] = policy_net_state_dict[key]*agent.tau + target_net_state_dict[key]*(1-agent.tau)
        agent.target_net.load_state_dict(target_net_state_dict)

        if done:
            episode_durations.append(t + 1)
            plot_durations()
            break
        
        # Increment step count
        step_count += 1
    print(f'Episode: {i_episode}, Total reward: {total_reward}, Epsilon {agent.eps_threshold}')

print('Complete')
plot_durations(show_result=True)
plt.ioff()
plt.show()