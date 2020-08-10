import sys

import gym
from gym import spaces

from gym_heaterenv.envs import heater_env

import numpy as np
import pandas as pd

import math
import random

import matplotlib.pyplot as plt

env = gym.make('HeaterEnv-v1')

total_episodes = 1#5000
max_steps = 900

qtable = np.zeros((150, 256))
qtable[: 101, 255] = 10
qtable[101: , 0] = 10
print(qtable.shape)
print(qtable)

final_energy = []
test_energy = []
final_energy = []

learning_rate = 0.8
discount_rate = 0.9

epsilon = 1.0				# Exploration rate
max_epsilon = 1.0			# Exploration probability at start
min_epsilon = 0.01			# Minimum exploration probability 
decay_rate = 0.005			# Exponential decay rate for exploration prob

for episode in range(total_episodes):
	observation = round(env.reset())

	print(episode)
	# print(f"State: {observation}")

	for step in range(max_steps):

		tradeoff = random.uniform(0, 1)

		if tradeoff > epsilon:
			action = np.argmax(qtable[observation, :])

		else:
			action = env.action_space.sample()

		# print(f"Action: {action}")


		new_observation, reward, done, info = env.step(action, 100, step + 1)
		new_observation = round(new_observation)

		# print(f"New state: {new_observation}")

		qtable[observation, action] = qtable[observation, action] + learning_rate * (reward + discount_rate * np.max(qtable[new_observation, :]) - qtable[observation, action])

		observation = new_observation

		if done or (step == max_steps - 1):
			final_energy.append(observation)

			print("Episode finished after {} timesteps".format(step + 1))
			break

		epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)

# np.savetxt("qtable_energy_conservation2.csv", qtable, delimiter = ",")

qtable_final = pd.read_csv("qtable_energy_conservation2.csv")

observation = round(env.reset())

for step in range(max_steps):
		if observation > 5.0 * 0.05 * 4180.0:
			action = 0

		else:
			action = 255

		# action = np.argmax(qtable_final.iloc[round(observation)])

		new_observation, reward, done, info = env.step(action, 100, step + 1)

		observation = new_observation

		test_energy.append(observation)

		if done:

			print("Episode finished after {} timesteps".format(step + 1))
			break

final_actions = [np.argmax(qtable_final.iloc[i]) for i in range(149)]

# plt.plot(np.arange(0, total_episodes), final_energy, "ro")
# plt.show()

plt.plot(np.arange(0, len(test_energy)), test_energy)
plt.show()

print(final_actions)

for obv, action in enumerate(final_actions):
	print(obv, action)

