import gym
from gym import error, spaces, utils
from gym.utils import seeding

import math
import random
import numpy as np


class HeaterEnv9(gym.Env):
	meta_data = {'render.modes': ['human']}

	def __init__(self):

		self.mass = 0.05
		self.specific_heat_capacity = 4180.0

		self.room_temp = 23.5
		self.init_temp = 25.0
		self.set_point = 30.0
		self.temp_precision = 0.01
		self.multiplier = 0.03

		self.total_energy = 0.0
		self.total_energy_absorbed = 0.0

		self.max_voltage = 10.72
		self.resistance = 4.0

		self.max_error = 5.0
		self.max_velocity = 0.1

		self.time_step = 1.0

		self.state = (self.init_temp, 0.0)

		self.temp_history = []
		self.velocity_history = []

		threshold = np.array([self.max_error, self.max_velocity])

		self.observation_space = spaces.Box(-threshold, threshold, dtype=np.float32)
		self.action_space = spaces.Discrete(255)

	def set_multiplier(self, multiplier):
		self.multiplier = multiplier

	def step(self, action):

		# print(f"Performing action: {action}")

		episode_done = False

		error, delta_temp = self.state

		voltage = ((self.max_voltage) / 255) * action

		energy_supplied = ((voltage ** 2) * self.time_step) / self.resistance

		# energy_dissipated = -0.9

		x = (self.set_point + error) - self.init_temp
		# energy_dissipated = (8E-12 * (x ** 3) - 3E-08 * (x ** 2) + 3E-05 * x - 0.02) * (self.mass * self.specific_heat_capacity)

		energy_dissipated = -0.64 - 0.18 * x

		# energy disipated is negative as per above equation, change it to positive

		#print("---- Step ----")
		#print(f"State: {self.state}")
		#print(f"Action: {action}")
		#print(f"Energy Dissipated: {energy_dissipated}")
		# print(f"Energy supplied: {energy_supplied}")

		self.total_energy += energy_supplied + energy_dissipated

		# print(f"Total energy : {self.total_energy}")

		delta_temp_calculated = round((self.multiplier * (self.total_energy - self.total_energy_absorbed)) / ((self.mass * self.specific_heat_capacity) * self.temp_precision)) * self.temp_precision
		delta_temp = np.random.normal(loc = delta_temp_calculated, scale = 0.01)
		# print(f"delta_temp: {delta_temp}")
		error += delta_temp
		error = round(error / self.temp_precision) * self.temp_precision
		# print(f"Error: {error}")

		self.total_energy_absorbed = (
			self.max_error + error) * self.mass * self.specific_heat_capacity
		# print(f"Total energy absorbed: {self.total_energy_absorbed}")

		self.state = (error, delta_temp)

		self.temp_history.append(error)
		self.velocity_history.append(delta_temp)

		if error >= 3.0:
			episode_done = True

		if len(self.temp_history) > 60:
			last_sixty_errors = self.temp_history[-60:]
			avg_error = sum(last_sixty_errors) / 60.0
			max_error = max(last_sixty_errors)
			min_error = min(last_sixty_errors)
			# print(f"avg_error: {avg_error}")
			# print(f"max_error: {max_error}")
			# print(f"min_error: {min_error}")

			if abs(avg_error) <= 0.1 and max_error <= 0.2 and min_error >= -0.2:
				episode_done = True

		reward = self.old_reward(error, delta_temp)

		return np.array(self.state), reward, episode_done, {}

	def reward(self, error, velocity):

		last_ten_errors = self.temp_history[-10:]
		avg_error = sum(last_ten_errors) / 10.0
		max_error = max(last_ten_errors)
		min_error = min(last_ten_errors)

		if abs(avg_error) <= 0.1 and max_error <= 0.2 and min_error >= -0.2:
			return 10000

		if error > 0:
			# reward = -ve and proportional to velocity and error
			# reward = -10000 - (1000 * velocity * error)
			# print(f"Overshoot: reward {reward}")
			return -1000 - (1000 * velocity * error)

		if error > -0.75:
			if velocity == 0:
				return 15000

			else:
				return 100.0 / velocity

		if error > -1.5:
			if velocity == 0:
				return 0

			else:
				return 10.0 / velocity

		if error > -2.5:
			if velocity == 0:
				return 0

			else:
				return 1.0 / velocity

		if error < 0:
			return 100 * velocity

		return 0

	def old_reward(self, error, velocity):
		last_ten_errors = self.temp_history[-10:]
		avg_error = sum(last_ten_errors) / 10.0
		max_error = max(last_ten_errors)
		min_error = min(last_ten_errors)

		if abs(avg_error) <= 0.2 and max_error <= 0.2 and min_error >= -0.2:
			return 100

		if abs(error) >= 0.0 and abs(error) <= 2.0:
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

		if error > 0.3:
			reward *= 10

		return reward

	def reset(self):
		self.total_energy_absorbed = 0.0
		self.total_energy = 0.0

		self.temp_history = []
		self.velocity_history = []

		self.state = (self.init_temp - self.set_point, 0.0)

		return np.array(self.state)

	def render(self, mode='human', close=False):
		pass

	def close(self):
		pass
