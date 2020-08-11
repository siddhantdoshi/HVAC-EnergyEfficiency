import gym
from gym import error, spaces, utils
from gym.utils import seeding

import math
import random
import numpy as np

class HeaterEnv6(gym.Env):
	meta_data = {'render.modes': ['human']}

	def __init__(self):

		self.mass = 0.05
		self.specific_heat_capacity = 4180.0

		self.init_temp = 25.0
		self.set_point = 30.0
		self.temp_precision = 0.01

		self.total_energy = 0.0
		self.total_energy_absorbed = 0.0

		self.max_voltage = 9.66
		self.resistance = 4.0

		self.max_error = 5.0
		self.max_velocity = 0.1

		self.time_step = 1.0

		self.state = (self.init_temp, 0.0)

		threshold = np.array([self.max_error, self.max_velocity])

		self.observation_space = spaces.Box(-threshold, threshold, dtype = np.float32)
		self.action_space = spaces.Discrete(255)

	def step(self, action):
		
		# print(f"Performing action: {action}")

		episode_done = False

		voltage = ((self.max_voltage) / 255) * action

		error, delta_temp = self.state

		energy_supplied = ((voltage ** 2) * self.time_step) / self.resistance
		energy_dissipated = 0.9

		# print(f"Energy supplied: {energy_supplied}")

		self.total_energy += energy_supplied - energy_dissipated

		# print(f"Total energy absorbed: {self.total_energy}")

		delta_temp = round((0.032 * (self.total_energy - self.total_energy_absorbed)) / ((self.mass * self.specific_heat_capacity) * self.temp_precision)) * self.temp_precision
		error += delta_temp
		error = round(error / self.temp_precision) * self.temp_precision

		self.total_energy_absorbed = (self.max_error + error) * self.mass * self.specific_heat_capacity
		
		self.state = (error, delta_temp)

		reward = self.reward(error, delta_temp)

		if error >= 3.0:
			episode_done = True

		return np.array(self.state), reward, episode_done, {}

	def reward(self, error, velocity):
		if abs(error) >= 0.0 and abs(error) <= 0.3:
			if error <= 0:
				if velocity < 0:
					reward = -0.5

				else:
					reward = 20 * velocity * abs(error) - 40 * velocity

			else:
				reward = -20 * velocity * abs(error) - 40 * velocity

		else:
			if error <= 0:
				reward = 8 * velocity

			else:
				reward = -70 * velocity

		if error > 0:
			reward *= 10

		return reward

	def reset(self):
		self.total_energy_absorbed = 0.0
		self.total_energy = 0.0

		self.state = (self.init_temp - self.set_point, 0.0)

		return np.array(self.state)

	def render(self, mode = 'human', close = False):
		pass
	
	def close(self):
		pass
