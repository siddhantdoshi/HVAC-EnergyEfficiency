import gym
from gym import error, spaces, utils
from gym.utils import seeding

import math
import random
import numpy as np

class HeaterEnv(gym.Env):
	meta_data = {'render.modes': ['human']}

	def __init__(self):
	 	# mass, init_temp, set_point, max_voltage, resistance, time_step, num_oscillations):

		self.mass = 0.05

		self.init_temp = 25.0
		self.temperature = 25.0
		self.set_point = 30.0

		self.max_voltage = 12.0
		self.resistance = 3.6

		self.time_step = 1.0
		self.num_oscillations = 5
		self.count = 5

		self.observation_space = spaces.Box(self.init_temp, self.set_point + 3.0, shape = (1,), dtype = np.float32)
		self.action_space = spaces.Discrete(256)

		self.action_history = []

	def step(self, action, max_settling_time, steps):
		# print(f"Performing action: {action}")

		episode_done = False

		if len(self.action_history) < 5:
			self.action_history.append(action)

		else:
			self.action_history = self.action_history[1:]
			self.action_history.append(action)

		# weighted_action = sum([(0.7 ** i) * self.action_history[5 - i] for i in range(5)])

		energy = 0

		for index, action in enumerate(self.action_history[:: -1]):
			voltage = (12.0 / 255) * action

			energy += (0.35 ** index) * ((voltage ** 2) * self.time_step / self.resistance)

		dissipation = (self.temperature - self.init_temp) * 0.05
		# print(f"Dissipated energy: {dissipation}")
		delta_temp = (energy - dissipation) / (self.mass * 4180.0)

		prev_temp = self.temperature
		self.temperature += delta_temp

		reward = self.reward(max_settling_time, steps)

		if (self.temperature >= self.set_point) and (prev_temp < self.set_point):
			self.count -= 1

		if (self.count == 0) or (self.temperature >= self.set_point + 3.0):
			episode_done = True

		# print(f"Temperature: {self.temperature}")
		return self.temperature, reward, episode_done, {} 

	def reward(self, max_settling_time, steps):
		delta_temp = (self.temperature - self.set_point)
		
		if delta_temp <= 1:
			reward = - abs(self.temperature - self.set_point)

		else:
			reward = - (self.temperature - self.set_point) ** 2			

		if self.temperature < self.set_point:
			# reward = math.pow(delta_temp, 3.0)

			# reward = -energy

			if self.count == 5:
				if (steps * self.time_step) <= max_settling_time:
					reward *= 1.2

				else:
					reward -= 10

		else:
			reward *= 2

		return reward


	def reset(self):
		self.temperature = self.init_temp
		self.count = self.num_oscillations

		return self.init_temp

	def render(self, mode = 'human', close = False):
		pass
	
	def close(self):
		pass
