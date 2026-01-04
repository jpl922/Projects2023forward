# -*- coding: utf-8 -*-
"""
Created on Sat Jan  3 17:38:47 2026
# Sandbox for testing around with Gymnasium 
# checking out the classical control examples
@author: Jason
"""

import gymnasium as gym 

#%% doc example 

env = gym.make('CartPole-v1', render_mode="human") #.make creates env

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

