import gym
from gym import error, spaces, utils
from gym.utils import seeding

import math
import random
import numpy as np

class HeaterEnv2(gym.Env):
	meta_data = {'render.modes': ['human']}

	def __init__(self):

		self.mass = 0.05
		self.specific_heat_capacity = 4180.0
		self.delta_temp = 5.0

		"""
		self.init_temp = 25.0
		self.temperature = 25.0
		self.set_point = 30.0
		"""

		self.energy_absorbed = 0.0
		self.target_energy = self.mass * self.specific_heat_capacity * self.delta_temp

		self.max_voltage = 9.66
		self.resistance = 3.8

		self.time_step = 1.0
		self.count = 0

		self.observation_space = spaces.Box(0, self.target_energy * 0.14, shape = (1,), dtype = np.float32)
		self.action_space = spaces.Discrete(256)

	def step(self, action, max_settling_time, steps):
		
		# print(f"Performing action: {action}")

		episode_done = False

		voltage = ((self.max_voltage) / 255) * action

		energy_supplied = ((voltage ** 2) * self.time_step) / self.resistance
		energy_dissipated = 1

		# print(f"Dissipated energy: {dissipation}")

		self.energy_absorbed += energy_supplied - energy_dissipated

		# print(f"Energy absorbed: {self.energy_absorbed}")

		reward = self.reward(max_settling_time, steps)

		if self.energy_absorbed >= self.target_energy * 1.4:
			episode_done = True

		return int(self.energy_absorbed / 10), reward, episode_done, {} 

	def reward(self, max_settling_time, steps):
		delta_energy = self.energy_absorbed - self.target_energy
		
		if delta_energy <= self.mass * self.specific_heat_capacity:
			reward = - abs(delta_energy)

		else:
			reward = - (delta_energy) ** 2			

		if delta_energy > 0:
			self.count += 1

			reward *= 4

		if (self.count == 0) and ((steps * self.time_step) <= max_settling_time):
			reward -= 10

		return reward


	def reset(self):
		self.energy_absorbed = 0.0
		self.count = 0

		return 0

	def render(self, mode = 'human', close = False):
		pass
	
	def close(self):
		pass
