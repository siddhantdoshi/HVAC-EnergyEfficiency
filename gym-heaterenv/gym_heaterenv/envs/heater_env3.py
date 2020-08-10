import gym
from gym import error, spaces, utils
from gym.utils import seeding

import math
import random
import numpy as np

class HeaterEnv3(gym.Env):
	meta_data = {'render.modes': ['human']}

	def __init__(self):

		self.mass = 0.05
		self.specific_heat_capacity = 4180.0

		self.init_temp = 25.0
		self.temperature = 25.0
		self.set_point = 30.0
		self.reached_target = False

		self.precision = 0.1
		self.rounded_temp = 25.0
		self.prev_temp = 25.0
		self.delta_temp = 0.0

		self.energy_absorbed = 0.0
		self.total_energy = 0.0
		self.energy_history = []

		self.absorption_lag = 0.5

		self.max_voltage = 10.72
		self.resistance = 4.0

		self.time_step = 1.0

		self.observation_space = spaces.Box(0, self.set_point + 2.0, shape = (1,), dtype = np.float32)
		self.action_space = spaces.Discrete(256)

	def step(self, action, max_settling_time, steps):
		
		# print(f"Performing action: {action}")

		episode_done = False

		voltage = ((self.max_voltage) / 255) * action

		energy_supplied = ((voltage ** 2) * self.time_step) / self.resistance
		energy_dissipated = 0.7

		# print(f"Energy supplied: {energy_supplied}")

		self.energy_history.insert(0, energy_supplied)
		self.energy_history = self.energy_history[:5]
		self.energy_history = list(map(lambda x: self.absorption_lag * x, self.energy_history))

		self.energy_absorbed = sum(self.energy_history) - energy_dissipated
		self.total_energy += self.energy_absorbed

		# print(f"Energy absorbed: {self.energy_absorbed}")
		# print(f"Total energy absorbed: {self.total_energy}")

		self.temperature += self.energy_absorbed / (self.mass * self.specific_heat_capacity)
		self.rounded_temp = round(self.temperature / self.precision) * self.precision

		self.delta_temp = self.rounded_temp - self.prev_temp
		self.prev_temp = self.rounded_temp

		# print(f"Temperature: {self.rounded_temp}")

		reward = self.reward(max_settling_time, steps)

		if self.rounded_temp >= self.set_point + 2.0:
			episode_done = True

		return self.rounded_temp, reward, episode_done, {} 

	def reward(self, max_settling_time, steps):
		error = self.rounded_temp - self.set_point

		if abs(error) >= 0.0 and abs(error) <= 1.5:
			# reward = -20 * (self.delta_temp / (abs(error) + 0.5))
			if error <= 0:
				if self.delta_temp < 0:
					reward = -0.5

				else:
					reward = 20 * self.delta_temp * abs(error) - 40 * self.delta_temp

			else:
				reward = -20 * self.delta_temp * abs(error) - 40 * self.delta_temp

		else:
			if error <= 0:
				reward = 8 * (self.delta_temp - 0.1375)

			else:
				reward = -70 * self.delta_temp

		if not self.reached_target:
			if error >= 0:
				self.reached_target = True
				
			elif (steps * self.time_step) <= max_settling_time:	
				reward *= 1.01

			else:
				reward -= 10

		if error > 0:
			reward *= 10

		return reward


	def reset(self, over_heated = False):

		self.energy_absorbed = 0.0
		self.total_energy = 0.0
		self.reached_target = False

		if not over_heated:
			self.temperature = 25.0

		else:
			self.temperature = 31.5

		return self.temperature

	def render(self, mode = 'human', close = False):
		pass
	
	def close(self):
		pass
