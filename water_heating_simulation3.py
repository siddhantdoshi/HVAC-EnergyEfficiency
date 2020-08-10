import sys

import gym
from gym import spaces

from gym_heaterenv.envs import heater_env3

import numpy as np
import pandas as pd

import math
import random

import matplotlib.pyplot as plt

def obv_to_state(precision, temp, init_temp):
	return int((temp - init_temp) / precision)

env = gym.make('HeaterEnv-v2')

total_episodes = 3000
max_steps = 500

qtable = np.zeros((75, 256))
# qtable[: 51, 255] = 100
# qtable[61: , 0] = 100
print(qtable.shape)
print(qtable)

final_temp = []
test_temp = []

learning_rate = 0.8
discount_rate = 0.9

epsilon = 1.0				# Exploration rate
max_epsilon = 1.0			# Exploration probability at start
min_epsilon = 0.01			# Minimum exploration probability 
decay_rate = 0.003			# Exponential decay rate for exploration prob


# Training

for episode in range(total_episodes):
	temperature = env.reset()
	state = obv_to_state(env.precision, temperature, env.init_temp)

	print(episode)
	# print(f"Temperature: {temperature}")

	for step in range(max_steps):

		tradeoff = random.uniform(0, 1)
		num_steps = episode * max_steps + step + 1

		if (num_steps <= 100000) or tradeoff <= epsilon:
			action = env.action_space.sample()

		else:
			action = np.argmax(qtable[state, :])

		# print(f"State: {state}")
		# print(f"Action: {action}")

		# print(f"Qtable value: {qtable[state, action]}")		

		new_temp, reward, done, info = env.step(action, 100, step + 1)
		new_state = obv_to_state(env.precision, new_temp, env.init_temp)

		# print(f"New state: {new_observation}")

		qtable[state, action] = qtable[state, action] + learning_rate * (reward + discount_rate * np.max(qtable[new_state, :]) - qtable[state, action])

		temperature = new_temp
		state = obv_to_state(env.precision, temperature, env.init_temp)

		if done or (step == max_steps - 1):
			final_temp.append(temperature)

			print("Episode finished after {} timesteps".format(step + 1))
			break

		if num_steps > 100000:
			epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode - (round((num_steps - step - 1) / max_steps)))

qtable[54: , 0] = 100

np.savetxt("qtable_temp_energy.csv", qtable, delimiter = ",")


#Testing

qtable_final = pd.read_csv("qtable_temp_energy.csv")
temperature = env.reset()
state = obv_to_state(env.precision, temperature, env.init_temp)

for step in range(max_steps):

		# if temperature >= env.set_point:
		# 	action = 0

		# else:
		# 	action = 255

		action = np.argmax(qtable_final.iloc[state])
		new_temp, reward, done, info = env.step(action, 100, step + 1)

		temperature = new_temp
		state = obv_to_state(env.precision, temperature, env.init_temp)

		test_temp.append(temperature)

		if done:

			print("Episode finished after {} timesteps".format(step + 1))
			break

final_actions = [np.argmax(qtable_final.iloc[i]) for i in range(74)]

plt.plot(np.arange(0, total_episodes), final_temp, "ro")
plt.show()

plt.plot(np.arange(0, len(test_temp)), test_temp)
plt.show()

print(final_actions)

for obv, action in enumerate(final_actions):
	print(obv, action)
