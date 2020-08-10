import sys

import gym
from gym import spaces

from gym_heaterenv.envs import heater_env3

import numpy as np
import pandas as pd

import math
import random

import matplotlib.pyplot as plt

env = gym.make('HeaterEnv-v4')

total_episodes = 100000
max_steps = 900

qtable = np.zeros((1701, 26))
# qtable[: 51, 255] = 100
# qtable[61: , 0] = 100
print(qtable.shape)
print(qtable)

final_temp = []
test_temp = []

learning_rate = 0.8
discount_rate = 0.95

epsilon = 1.0				# Exploration rate
max_epsilon = 1.0			# Exploration probability at start
min_epsilon = 0.01			# Minimum exploration probability 
decay_rate = 0.002			# Exponential decay rate for exploration prob


# Training

for episode in range(total_episodes):
	state = env.reset()

	print(episode)
	# print(f"Temperature: {temperature}")

	for step in range(max_steps):

		tradeoff = random.uniform(0, 1)

		if tradeoff > epsilon:
			action = np.argmax(qtable[state, :])

		else:
			action = env.action_space.sample()

		# temperature = env.set_point + (((state // 3) * 20) - 1000) / 200.0
		temperature = env.set_point + (((state // 21) * 200) - 10000) / 2000.0
		
		# print(f"State: {state}")
		# print(f"Temperature: {temperature}")
		# print(f"Action: {action}")

		# print(f"Qtable value: {qtable[state, action]}")		

		new_state, reward, done, info = env.step(action)

		# print(f"New state: {new_observation}")

		qtable[state, action] = qtable[state, action] + learning_rate * (reward + discount_rate * np.max(qtable[new_state, :]) - qtable[state, action])

		state = new_state

		if done or (step == max_steps - 1):
			final_temp.append(temperature)

			print(f"Episode finished after {step + 1} timesteps with temperature: {temperature} degrees")
			break

		epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)

# qtable[1113: , 0] = 100

np.savetxt("qtable_multistate.csv", qtable, delimiter = ",")


#Testing

# qtable_final = pd.read_csv("qtable_multistate.csv")
state = env.reset()

for step in range(max_steps):

		# if temperature >= env.set_point:
		# 	action = 0

		# else:
		# 	action = 255

		action = np.argmax(qtable[state, :])
		# temperature = env.set_point + (((state // 3) * 20) - 1000) / 200.0
		temperature = env.set_point + (((state // 21) * 200) - 10000) / 2000.0

		new_state, reward, done, info = env.step(action)
		state = new_state

		test_temp.append(temperature)

		if done:

			print("Episode finished after {} timesteps".format(step + 1))
			break

final_actions = [np.argmax(qtable[i, :]) for i in range(1701)]

plt.plot(np.arange(0, total_episodes), final_temp, "ro")
plt.show()

plt.plot(np.arange(0, len(test_temp)), test_temp)
plt.show()

print(final_actions)

for obv, action in enumerate(final_actions):
	print(obv, action)
