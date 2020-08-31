import sys

import gym
from gym import spaces

from gym_heaterenv.envs import heater_env3

import numpy as np
import pandas as pd

import math
import random

import matplotlib.pyplot as plt

env = gym.make('HeaterEnv-v7')

total_episodes = 1
max_steps = 900


final_temp = []
test_temp = []


#Testing

for i in np.arange(0.0, 0.1, 0.01):
	print(i)
	state = env.reset()
	temperature, delta_temp = state
	env.set_multiplier(i)
	test_temp.clear()

	for step in range(2 * max_steps):

			# if temperature >= env.set_point + 0.3:
			# 	action = 0
			# else:
			# 	action = np.argmax(qtable[index, :])

			if temperature >= env.set_point:
				action = 0

			else:
				action = 255

			temperature, delta_temp = state
			# print(f"Error: {temperature}")

			temperature = round(temperature*10)/10
			# print(f"Rounded Error: {temperature}")

			temperature += env.set_point
			# print(f"Water Temperature: {temperature}")

			new_state, reward, done, info = env.step(action)
			state = new_state

			test_temp.append(temperature)
			plt.plot(np.arange(0, len(test_temp)), test_temp, label=i)



plt.show()

# print(final_actions)

# for obv, action in enumerate(final_actions):
# 	print(obv, action)
