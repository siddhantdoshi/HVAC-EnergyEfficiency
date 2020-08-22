import gym
from gym import error, spaces, utils
from gym.utils import seeding

import math
import random
import numpy as np


class HeaterEnv10(gym.Env):
	meta_data = {'render.modes': ['human']}

	def __init__(self):

		self.mass = 0.05
		self.specific_heat_capacity = 4180.0

		self.room_temp = 23.5
		self.init_temp = 25.0
		self.set_point = 30.0
		self.multiplier = 0.03

		self.total_energy = 0.0
		self.total_energy_absorbed = 0.0

		self.max_voltage = 10.72
		self.resistance = 4.0

		self.max_error = 5.0
		self.max_velocity = 0.1
		self.max_acceleration = 0.2

		self.prev_velocity = 0.0

		self.time_step = 1.0

		self.state = (self.init_temp - self.set_point, 0.0)

		self.error_history = []
		self.velocity_history = []
		self.acceleration_history = []

		threshold = np.array([self.max_error, self.max_velocity, self.max_acceleration])

		self.observation_space = spaces.Box(-threshold, threshold, dtype=np.float32)
		self.action_space = spaces.Discrete(255)

	def set_multiplier(self, multiplier):
		self.multiplier = multiplier

	def step(self, action):

		# print(f"Performing action: {action}")

		episode_done = False

		error, delta_temp, acceleration = self.state

		voltage = ((self.max_voltage) / 255) * action

		energy_supplied = ((voltage ** 2) * self.time_step) / self.resistance

		# energy_dissipated = -0.9

		x = (self.set_point + error) - self.init_temp
		# energy_dissipated = (8E-12 * (x ** 3) - 3E-08 * (x ** 2) + 3E-05 * x - 0.02) * (self.mass * self.specific_heat_capacity)

		energy_dissipated = -0.64 - 0.18 * x

		# energy disipated is negative as per above equation, change it to positive

		# print("---- Step ----")
		# print(f"State: {self.state}")
		# print(f"Action: {action}")
		# print(f"Energy Dissipated: {energy_dissipated}")
		# print(f"Energy supplied: {energy_supplied}")

		self.total_energy += energy_supplied + energy_dissipated

		# print(f"Total energy : {self.total_energy}")

		delta_temp_calculated = (self.multiplier * (self.total_energy - self.total_energy_absorbed)) / (self.mass * self.specific_heat_capacity)
		delta_temp = np.random.normal(loc=delta_temp_calculated, scale=0.015)

		error += delta_temp
		acceleration = delta_temp - self.prev_velocity
		self.prev_velocity = delta_temp

		# print(f"Error: {error}")
		# print(f"Velocity: {delta_temp}")
		# print(f"Acceleration: {acceleration}\n")

		self.total_energy_absorbed = (self.max_error + error) * self.mass * self.specific_heat_capacity
		# print(f"Total energy absorbed: {self.total_energy_absorbed}")

		self.state = (error, delta_temp, acceleration)

		self.error_history.append(error)
		self.velocity_history.append(delta_temp)
		self.acceleration_history.append(acceleration)

		if error >= 3.0:
			episode_done = True

		if len(self.error_history) > 100:
			last_hundred_errors = self.error_history[-100:]
			avg_error = sum(last_hundred_errors) / 100.0
			max_error = max(last_hundred_errors)
			min_error = min(last_hundred_errors)

			# print(f"avg_error: {avg_error}")
			# print(f"max_error: {max_error}")
			# print(f"min_error: {min_error}")

			if abs(avg_error) <= 0.1 and max_error <= 0.2 and min_error >= -0.2:
				episode_done = True

		reward = self.reward(error, delta_temp, acceleration)

		return np.array(self.state), reward, episode_done, {}

	def reward(self, error, velocity, acceleration):

		last_ten_errors = self.error_history[-10:]
		avg_error = sum(last_ten_errors) / len(last_ten_errors)

		last_ten_velocities = self.velocity_history[-10:]
		avg_velocity = sum(last_ten_velocities) / len(last_ten_velocities)

		last_ten_accel = self.acceleration_history[-10:]
		avg_accel = sum(last_ten_accel) / len(last_ten_accel)

		# if error > 0:
		# 	return -10 * error * avg_velocity - 5 * error * avg_accel

		if error > 0:
			return -1000 * error * avg_velocity

		if error > -1:
			# if velocity < 0:
			# 	return 1.0
			
			# else:
			# 	return -100 * acceleration - 10 * velocity

			return -10 * avg_accel - 100 * avg_velocity
			# return 1.0 / ((error + 1) * avg_velocity) + 2.0 / ((error + 1) * avg_accel)

		if error > -2.5:
			return -20 * error * avg_velocity - 5 * abs(avg_accel)

		else:
			return -2 * error * (5 * avg_velocity - 2 * avg_accel)

	def old_reward2(self, error, velocity):

		last_ten_errors = self.error_history[-10:]
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

	def old_reward1(self, error, velocity):
		last_ten_errors = self.error_history[-10:]
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

	def reset(self, init_temp = 25.0):
		self.total_energy_absorbed = 0.0
		self.total_energy = 0.0

		self.error_history = []
		self.velocity_history = []

		self.init_temp = init_temp

		self.state = (self.init_temp - self.set_point, 0.0, 0.0)

		return np.array(self.state)

	def render(self, mode='human', close=False):
		pass

	def close(self):
		pass
