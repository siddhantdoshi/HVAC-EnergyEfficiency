import gym
from gym import error, spaces, utils
from gym.utils import seeding

import math
import random
import numpy as np

class HeaterEnv4(gym.Env):
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

		self.total_energy = 0.0
		self.total_energy_absorbed = 0.0
		self.target_energy = self.mass * self.specific_heat_capacity * (self.set_point - self.init_temp)
		
		# self.energy_history = []
		# self.absorption_lag = 0.5

		self.max_voltage = 9.66
		self.resistance = 4.0

		self.time_step = 1.0

		self.observation_space = spaces.Box(0, self.set_point + 3.0, shape = (1,), dtype = np.float32)
		self.action_space = spaces.Discrete(26)

	def step(self, action, max_settling_time, steps):
		
		# print(f"Performing action: {action}")

		episode_done = False

		voltage = ((self.max_voltage) / 26) * action

		energy_supplied = ((voltage ** 2) * self.time_step) / self.resistance
		energy_dissipated = 0.9

		# print(f"Energy supplied: {energy_supplied}")

		self.total_energy += energy_supplied - energy_dissipated

		# print(f"Total energy absorbed: {self.total_energy}")

		self.temperature += 0.032 * (self.total_energy - self.total_energy_absorbed) / (self.mass * self.specific_heat_capacity)
		self.rounded_temp = round(self.temperature / self.precision) * self.precision

		self.total_energy_absorbed = (self.rounded_temp - self.init_temp) * self.mass * self.specific_heat_capacity

		self.delta_temp = self.rounded_temp - self.prev_temp

		# print(f"Temperature change: {self.delta_temp}")

		self.prev_temp = self.rounded_temp

		# print(f"Temperature: {self.rounded_temp}")

		reward = self.reward(max_settling_time, steps)

		if self.rounded_temp >= self.set_point + 3.0:
			episode_done = True

		return self.rounded_temp, reward, episode_done, {} 

	def reward(self, max_settling_time, steps):
		error_temp = (self.rounded_temp - self.set_point) / (self.set_point - self.init_temp)
		error_energy = (self.total_energy - self.total_energy_absorbed) / (self.mass * self.specific_heat_capacity)
		# error_time = ((steps * self.time_step) - max_settling_time) / max_settling_time

		if error_temp <= - 0.3:
			reward_temp = 10 * self.delta_temp

		elif error_temp >= 0.3:
			reward_temp = -100 * self.delta_temp

		else:
			reward_temp = - abs(error_temp) * self.delta_temp

		reward_energy = - (error_energy ** 2)

		# if not self.reached_target:
		# 	if error_temp >= 0:

		# 		self.reached_target = True
		# 		reward_time = 0
				
		# 	elif (steps * self.time_step) <= max_settling_time:	
		# 		reward_time = - error_time
		# 		# print("In elif")

		# 	else:
		# 		reward_time = - 10
		# 		# print("In first else")

		# else:
		# 	reward_time = 0
			# print("In second else")

		# if error_temp > 0:
		# 	reward_temp *= -100

		# reward = 0.7 * reward_temp + 0.3 * reward_energy

		return reward_temp

	def reset(self, over_heated = False):

		self.total_energy_absorbed = 0.0
		self.total_energy = 0.0
		self.reached_target = False

		self.prev_temp = 25.0

		if not over_heated:
			self.temperature = 25.0

		else:
			self.temperature = 31.5

		return self.temperature

	def render(self, mode = 'human', close = False):
		pass
	
	def close(self):
		pass
