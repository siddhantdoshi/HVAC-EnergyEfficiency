import gym
from gym import error, spaces, utils
from gym.utils import seeding

import math
import random
import numpy as np

class HeaterEnv5(gym.Env):
	meta_data = {'render.modes': ['human']}

	def __init__(self):

		self.mass = 0.05
		self.specific_heat_capacity = 4180.0

		self.init_temp = 25.0
		self.temperature = 25.0
		self.set_point = 30.0
		self.reached_target = False

		self.temp_precision = 0.1
		self.rounded_temp = 25.0
		self.prev_temp = 25.0

		self.delta_temp = 0.0
		self.delta_temp_history = []
		self.delta_temp_moving_average = 0.0
		self.rate_precision = 0.01

		self.total_energy = 0.0
		self.total_energy_absorbed = 0.0

		self.max_voltage = 9.66
		self.resistance = 4.0

		self.max_error = 5.0
		self.max_velocity = 0.1075

		self.time_step = 1.0

		self.observation_space = spaces.Box(0, 1701, shape = (1,), dtype = np.float32)
		self.action_space = spaces.Discrete(26)

	def step(self, action):
		
		# print(f"Performing action: {action}")

		episode_done = False

		voltage = ((self.max_voltage) / 26) * action

		energy_supplied = ((voltage ** 2) * self.time_step) / self.resistance
		energy_dissipated = 0.9

		# print(f"Energy supplied: {energy_supplied}")

		self.total_energy += energy_supplied - energy_dissipated

		# print(f"Total energy absorbed: {self.total_energy}")

		self.temperature += 0.032 * (self.total_energy - self.total_energy_absorbed) / (self.mass * self.specific_heat_capacity)
		self.rounded_temp = round(self.temperature / self.temp_precision) * self.temp_precision

		self.total_energy_absorbed = (self.rounded_temp - self.init_temp) * self.mass * self.specific_heat_capacity

		self.delta_temp = self.rounded_temp - self.prev_temp

		self.delta_temp_history.insert(0, self.delta_temp)
		self.delta_temp_history = self.delta_temp_history[:10]

		self.delta_temp_moving_average = round(sum(self.delta_temp_history) / (len(self.delta_temp_history) * self.rate_precision)) * self.rate_precision

		# print(f"Average temperature change: {self.delta_temp_moving_average}")

		self.prev_temp = self.rounded_temp

		# print(f"Temperature: {self.rounded_temp}")

		error_ratio = (self.rounded_temp - self.set_point) / self.max_error
		velocity_ratio1 = self.delta_temp / self.max_velocity
		velocity_ratio2 = self.delta_temp_moving_average / self.max_velocity

		state1 = self.state1(error_ratio, velocity_ratio1)
		state2 = self.state2(error_ratio, velocity_ratio2)

		reward1 = self.reward(error_ratio, velocity_ratio1)
		reward2 = self.reward(error_ratio, velocity_ratio2)

		if self.rounded_temp >= self.set_point + 3.0:
			episode_done = True

		return state2, reward2, episode_done, {}

	def state1(self, error_ratio, velocity_ratio):
		observation = int(1000 * error_ratio + velocity_ratio + 1001)
		state = int(((observation // 20) * 3) + (observation % 10))

		return state

	def state2(self, error_ratio, velocity_ratio):
		observation = int(10000 * error_ratio + 10 * velocity_ratio + 10010)
		state = int(((observation // 200) * 21) + (observation % 100))

		return state


	def reward(self, error_ratio, velocity_ratio):
		if abs(error_ratio) >= 0.0 and abs(error_ratio) <= 0.3:
			if error_ratio <= 0:
				if self.delta_temp < 0:
					reward = -0.5

				else:
					reward = 20 * velocity_ratio * abs(error_ratio) - 40 * velocity_ratio

			else:
				reward = -20 * velocity_ratio * abs(error_ratio) - 40 * velocity_ratio

		else:
			if error_ratio <= 0:
				reward = 8 * velocity_ratio

			else:
				reward = -70 * velocity_ratio

		if error_ratio > 0:
			reward *= 10

		return reward

	def reset(self, over_heated = False):

		self.total_energy_absorbed = 0.0
		self.total_energy = 0.0
		self.reached_target = False

		self.prev_temp = 25.0

		if not over_heated:
			self.temperature = 25.0

		else:
			self.temperature = 31.5

		return 10

	def render(self, mode = 'human', close = False):
		pass
	
	def close(self):
		pass
