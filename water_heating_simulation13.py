import sys

import gym
from gym import spaces

from gym_heaterenv.envs import heater_env3

import numpy as np
import pandas as pd

import math
import random
import time

import matplotlib.pyplot as plt

env = gym.make('HeaterEnv-v9')

total_episodes = 20000
max_steps = 900

qtable = np.zeros((800, 256))

print(qtable.shape)
print(qtable)

final_temp = []
test_temp = []

learning_rate = 0.5
discount_rate = 0.8

epsilon = 1.0				# Exploration rate
max_epsilon = 1.0			# Exploration probability at start
min_epsilon = 0.01			# Minimum exploration probability
decay_rate = 0.0002			# Exponential decay rate for exploration prob

def state_to_index(state):
	error, delta_temp, acceleration = state

	# print(f"State: {state}")
	# print(f"Error: {error}; Temp change: {delta_temp}")

	# for precision of 0.1 and delta_temp -0.1 to 0.1
	error = round(error * 10) / 10.0
	delta_temp = round(delta_temp * 10) / 10.0
	acceleration = round(acceleration * 10) / 10.0
	
	if (delta_temp > 0.1):
		delta_temp = 0.1

	elif delta_temp < -0.1:
		delta_temp = -0.1

	if (acceleration > 0.1):
		acceleration = 0.1

	elif acceleration < -0.1:
		acceleration = -0.1

	conjugate = 1000 * error + 100 * delta_temp + 10 * acceleration + 5011
	index = 9 * (conjugate // 100) + 3 * ((conjugate // 10) % 10) + (conjugate % 10)

	# for precision of 0.1 and delta_temp -0.2 to 0.2
	# error = round(error * 10) / 10.0
	# delta_temp = round(delta_temp * 10) / 10.0
	# conjugate = 1000 * error + 10 * delta_temp + 5002
	# index = ((conjugate // 100) * 5) + (conjugate % 100)

	# for precision of 0.01
	# conjugate = 10000 * error + 100 * delta_temp + 50010
	# index = ((conjugate // 100) * 21) + (conjugate % 100)

	# print(f"Conjugate: {conjugate}")
	# print(f"Index: {index}")

	return int(index)

# def index_to_state(index):
# 	# conjugate =
# 	return -1
# Training


for episode in range(total_episodes):
	state = env.reset()
	env.set_multiplier(0.03)
	index = state_to_index(state)

	# print(f"Episode: {episode}")

	# print(f"Temperature: {temperature}")

	for step in range(max_steps):

		tradeoff = random.uniform(0, 1)

		# if tradeoff > epsilon:
		# 	action = np.argmax(qtable[index, :])

		# else:
		# 	action = env.action_space.sample()

		if tradeoff > epsilon:
			action = np.argmax(qtable[index, :])

		else:
			action = env.action_space.sample()

		temperature, delta_temp, acceleration = state
		temperature = round(temperature * 10) / 10.0
		delta_temp = round(delta_temp * 10) / 10.0
		acceleration = round(acceleration * 10) / 10.0

		temperature += env.set_point

		if temperature >= env.set_point + 0.2:
			action = 0

		index = state_to_index(state)

		# print("-------------")
		# print(f"Index: {index}")
		# print(f"episode: {episode} , step {step}")
		# print(f"Temperature: {temperature}")
		# print(f"Temperature change: {delta_temp}")

		new_state, reward, done, info = env.step(action)

		new_index = state_to_index(new_state)

		# print(f"Action: {action}")
		# print(f"New state: {new_state}")
		# print(f"Reward: {reward}")
		# print(f"new_index: {new_index}")

		qtable[index, action] = qtable[index, action] + learning_rate * (reward + discount_rate * np.max(qtable[new_index, :]) - qtable[index, action])

		# print(f"Qtable value: {qtable[index, action]}")

		state = new_state

		if done or (step == max_steps - 1):
			final_temp.append(temperature)
			print(f"Episode {episode} finished after {step + 1} timesteps with temperature: {temperature} degrees")

			break

	if episode > 2551:
		epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * (episode))
	
	# print(f"epsilon: {epsilon}")

# qtable[1113: , 0] = 100

filename_suffix = time.strftime("%Y%m%d-%H%M%S")
np.savetxt("Data/22-Aug-2020/Raw/qtable_multistate_13_" + filename_suffix + ".csv", qtable, delimiter=", ")


#Testing

# qtable_final = pd.read_csv("qtable_multistate.csv")

index = state_to_index(state)
state = env.reset()
test_temp.clear()
for step in range(2 * max_steps):

		if temperature >= env.set_point + 0.1:
			action = 0
		
		else:
			action = np.argmax(qtable[index, :])

		# if temperature >= env.set_point:
		# 	action = 0

		# else:
		# 	action = 255

		temperature, delta_temp, acceleration = state
		temperature = round(temperature * 10) / 10.0
		delta_temp = round(delta_temp * 10) / 10.0
		acceleration = round(acceleration * 10) / 10.0

		temperature += env.set_point

		index = state_to_index(state)

		new_state, reward, done, info = env.step(action)
		state = new_state

		test_temp.append(temperature)

		# if done:
		# 	print(f"Episode finished after {step + 1} timesteps with temperature: {temperature}")

		# 	break

final_actions = [np.argmax(qtable[i, :]) for i in range(700)]

plt.plot(np.arange(0, total_episodes), final_temp, "ro")
# plt.show()
plt.savefig('Data/22-Aug-2020/Raw/final_training13_' + filename_suffix + '.png')
plt.clf()


plt.plot(np.arange(0, len(test_temp)), test_temp)
plt.savefig('Data/22-Aug-2020/Raw/simulation13_' + filename_suffix + '.png')
plt.show()

print(final_actions)
# np.savetxt("final_actions_9.csv", final_actions, delimiter=",")

with open('Data/22-Aug-2020/Raw/final_actions_13_' + filename_suffix + '.txt', 'w') as f:
		f.write(str(final_actions))
		f.write("\n")

		for index, item in enumerate(final_actions):
			f.write(f"{index}: {item}\n")

for obv, action in enumerate(final_actions):
	print(obv, action)
