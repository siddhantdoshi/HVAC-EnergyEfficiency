import sys

import gym
from gym import spaces

from gym_heaterenv.envs import heater_env

import numpy as np
import pandas as pd

import math
import random

import matplotlib.pyplot as plt

# np.set_printoptions(threshold = sys.maxsize)

env = gym.make('HeaterEnv-v0')

total_episodes = 1#50000
max_steps = 900

qtable = np.zeros((750, 256))
print(qtable.shape)

final_temp = []
test_temps = []
final_actions = []

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

		# print(new_state)

		qtable[observation, action] = qtable[observation, action] + learning_rate * (reward + discount_rate * np.max(qtable[new_observation, :]) - qtable[observation, action])

		observation = new_observation
		state = new_state

		if done or (step == max_steps - 1):
			final_temp.append((observation + 2500.0) / 100.0)

			print("Episode finished after {} timesteps".format(step + 1))
			break

		epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)

	# if episode == total_episodes - 1:
	# print(qtable)
	# print("\n\n\n")

# np.savetxt("qtable_dissipation.csv", qtable, delimiter = ",")

qtable_final = pd.read_csv("qtable_dissipation.csv")

state = env.reset()
observation = int((state * 100) + 0.5) - 2500

for step in range(max_steps):
		# env.render()
		# if state > 30:
		# 	action = 0

		# else:
		# 	action = 255

		action = np.argmax(qtable_final.iloc[observation])

		new_state, reward, done, info = env.step(action, 100, step + 1)
		new_observation = int((new_state * 100) + 0.5) - 2500		

		# print(new_state)

		# qtable[observation, action] = qtable[observation, action] + learning_rate * (reward + discount_rate * np.max(qtable[new_observation, :]) - qtable[observation, action])

		observation = new_observation
		state = new_state

		test_temps.append((observation + 2500.0) / 100.0)

		if done:

			print("Episode finished after {} timesteps".format(step + 1))
			break

final_actions = [np.argmax(qtable_final.iloc[i]) for i in range(749)]

# plt.plot(np.arange(0, total_episodes), final_temp, "ro")
# plt.show()

# print(test_temps)

print(len(final_actions))
print(final_actions)

plt.plot(np.arange(0, len(test_temps)), test_temps)
plt.show()

