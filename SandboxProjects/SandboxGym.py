# -*- coding: utf-8 -*-
"""
Created on Sat Jan  3 17:38:47 2026
# Sandbox for testing around with Gymnasium 
# checking out the classical control examples
@author: Jason
"""

import gymnasium as gym 

#%% docs Basic usage 

env = gym.make('CartPole-v1', render_mode="human") #.make creates env

# button presses (discrete)
print(f"Action space: {env.action_space}") # Discrete(2) L/R
print(f"Sample action: {env.action_space.sample()}") # 0 or 1

# box obs space (continuous)
print(f"Observation space: {env.observation_space}") # Box w/ 4 values
print(f"Sample observation: {env.observation_space.sample()}") # random valid obs





observation, info = env.reset()
# obsevation: what the agent sees; postion, angle, velocity
# info: extra debugging 

print(f"Starting observation: {observation}")
#[cart_position, cart_velo, pole_angle, pole_angvelo]

episode_over=False
total_reward=0

while not episode_over: 
    
    
    # choose an action 0 = push left, 1 = push right
    action = env.action_space.sample() # random action 
    
    # Apply action and respond
    observation, reward, terminated, truncated, info = env.step(action)
    
    # reward: +1 each step pole remains upright
    # terminated: True if pole falls too far (fail)
    # truncated: True if hit the time limit (500 steps)
    
    total_reward +=reward
    episode_over = terminated or truncated
    
print(f"Episode finished! Total reward: {total_reward}")
env.close()

#%% Modifying Environment
# flattening and shaping observation space into usable 1D array for algos
import gymnasium as gym
from gymnasium.wrappers import FlattenObservation

# Run in command line 
# start with complex obs space
env =gym.make("CarRacing-v3")
env.observation_space.shape

wrapped_env = FlattenObservation(env)
wrapped_env.observation_space.shape


#%% Training an Agent Q-learning 
from collections import defaultdict 
import gymnasium as gym 
import numpy as np 

# something missing or miscoded here the errors aren't lining up something to do with learning or initiation; pureloy random whole time 



class BlackjackAgent:
    def __init__(self, env: gym.Env,
                 learning_rate: float,
                 initial_epsilon: float,
                 epsilon_decay: float,
                 final_epsilon: float,
                 discount_factor: float = 0.95,
                 ):
        """Initialize a Q-Learning agent.

Args:
    env: The training environment
    learning_rate: How quickly to update Q-values (0-1)
    initial_epsilon: Starting exploration rate (usually 1.0)
    epsilon_decay: How much to reduce epsilon each episode
    final_epsilon: Minimum exploration rate (usually 0.1)
    discount_factor: How much to value future rewards (0-1)
"""
        self.env = env

        # Q-Table: maps (state, action) to expected reward
        # defaultdict automatically creates entries with zeros for new states
        self.q_values = defaultdict(lambda: np.zeros(env.action_space.n))
        self.lr = learning_rate
        self.discount_factor = discount_factor  # care about future reward
        # exploration params
        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon

        # track learning progress
        self.training_error = []

    def get_action(self, obs: tuple[int, int, bool]) -> int:
         """Choose an action using epsilon-greedy strategy.
         Returns:
             action: 0 (stand) or 1 (hit)
         """
         if np.random.random() < self.epsilon:
             return self.env.action_space.sample()
         # with probability epsilon: explore (random action)
    
      
            # with probability (1-epsilon): exploit best known action
         else:
            return int(np.argmax(self.q_values[obs]))

    def update(
        self,
        obs: tuple[int, int, bool],
        action: int,
        reward: float,
        terminated: bool,
        next_obs: tuple[int, int, bool],
    ):
         """Update Q-value based on experience.

This is the heart of Q-learning: learn from (state, action, reward, next_state)
"""
          # what is best for next state?
          # zero if episode ends - no future possiblity
         future_q_value = (not terminated)*np.max(self.q_values[next_obs])

           # what should Q-value be? bellman equation
         target = reward + self.discount_factor * future_q_value
          
          # how wrong was your current estimate  (indexing table)

         temporal_difference = target - self.q_values[obs][action]
          
          
            # update based on error
            # learning rate controls how big steps we take

         self.q_values[obs][action] = (
                self.q_values[obs][action]+self.lr * temporal_difference
            )
          # track learning progress
         self.training_error.append(temporal_difference)

            

            # self.q_values[a][b] is indexing into the table to access value
    def decay_epsilon(self):
         """Reduce exploration rate after each episode."""
         self.epsilon = max(self.final_epsilon,
                              self.epsilon-self.epsilon_decay)



# Training the agent

# Training hyperparameters
learning_rate = 0.1 # learning speed; higher = faster/ less stable
n_episodes = 100_000 # number of hands 
start_epsilon = 1.0 # 100% random actions 
epsilon_decay = start_epsilon / (n_episodes / 2) # reduce exploration rate
final_epsilon = 0.1 # always keep same exploration 

# create env and agent 
env = gym.make("Blackjack-v1", sab=False)
env = gym.wrappers.RecordEpisodeStatistics(env, buffer_length=n_episodes)

agent = BlackjackAgent(
    env=env,
    learning_rate = learning_rate,
    initial_epsilon = start_epsilon, 
    epsilon_decay = epsilon_decay,
    final_epsilon= final_epsilon)

from tqdm import tqdm # progress bar (nice)

for episode in tqdm(range(n_episodes)):
    # new hand 
    obs, info =  env.reset()
    done = False
    
    # play one complete hand 
    while not done: 
        # agent chooses action (random to intelligent)
        action = agent.get_action(obs)
        
        # take action and observe result
        next_obs, reward, terminated, truncated, info = env.step(action)
        
        # learn from this experience 
        agent.update(obs, action, reward, terminated, next_obs)
        
        # move to next state 
        done = terminated or truncated
        obs = next_obs
        
        # reduce exploration rate 
        agent.decay_epsilon 
        

# analyzing training results 
"""Need to look into this error somewhere"""
from matplotlib import pyplot as plt 

def get_moving_avgs(arr, window, convolution_mode):
    """ moving average to smooth noise"""
    return np.convolve(np.array(arr).flatten(), np.ones(window), mode=convolution_mode)/window

rolling_length = 500 
fig, axs = plt.subplots(ncols=3, figsize=(12,5))

# w/l performance 
axs[0].set_title("Episode rewards")
reward_moving_average = get_moving_avgs(
    env.return_queue, 
    rolling_length, 
    "valid"
    )

axs[0].plot(range(len(reward_moving_average)), reward_moving_average)
axs[0].set_ylabel("Average Reward")
axs[0].set_xlabel("Episode")

# episode length
axs[1].set_title("Episode lengths")
length_moving_average = get_moving_avgs(
    env.length_queue, rolling_length,
    "valid")


# episode length (action per hand)
axs[1].plot(range(len(length_moving_average)), length_moving_average)
axs[1].set_ylabel("Average Episode Length")
axs[1].set_xlabel("Episode")

# Training error (learning)
axs[2].set_title("Training Error")
training_error_moving_average = get_moving_avgs(agent.training_error, rolling_length, "same")

axs[2].plot(range(len(training_error_moving_average)), training_error_moving_average)
axs[2].set_ylabel("Temporal Difference Error")
axs[2].set_xlabel("Step")

plt.tight_layout()
plt.show()
 
        
        
        
        

