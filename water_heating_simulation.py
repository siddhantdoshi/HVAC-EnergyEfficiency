import sys

import gym
from gym import spaces

from gym_heaterenv.envs import heater_env

import numpy as np
# import pandas as pd

import math
import random

# np.set_printoptions(threshold = sys.maxsize)

env = gym.make('HeaterEnv-v0')

total_episodes = 15000
max_steps = 180

qtable = np.zeros((1000, 256))
print(qtable.shape)

action_history = []

learning_rate = 0.8
discount_rate = 0.9

epsilon = 1.0				# Exploration rate
max_epsilon = 1.0			# Exploration probability at start
min_epsilon = 0.01			# Minimum exploration probability 
decay_rate = 0.005			# Exponential decay rate for exploration prob

for episode in range(total_episodes):
	state = env.reset()
	observation = int((state * 100) + 0.5) - 2500

	# print(observation)
	print(episode)

	for step in range(max_steps):
		# env.render()

		tradeoff = random.uniform(0, 1)

		if tradeoff > epsilon:
			action = np.argmax(qtable[observation, :])

		else:
			action = env.action_space.sample()

		new_state, reward, done, info = env.step(action, 100, step + 1)
		new_observation = int((new_state * 100) + 0.5) - 2500

		# if step == max_steps - 1:
		print(new_state)

		qtable[observation, action] = qtable[observation, action] + learning_rate * (reward + discount_rate * np.max(qtable[new_observation, :]) - qtable[observation, action])

		observation = new_observation
		state = new_state

		if done:
			print("Episode finished after {} timesteps".format(step + 1))
			break

		epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)

	# if episode == total_episodes - 1:
	print(qtable)
	print("\n\n\n")

np.savetxt("qtable_dissipation.csv", qtable, delimiter = ",")
