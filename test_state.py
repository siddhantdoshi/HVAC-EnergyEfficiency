import numpy as np


def state_to_index(state):
	error, delta_temp, acceleration = state

	print(f"State: {state}")
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

	# conjugate = 1000 * error + 100 * delta_temp + 10 * acceleration + 5011
	# index = ((conjugate // 100) * 6) + (conjugate % 10) + (conjugate % 100) + 1
	
	
	conjugate = 1000 * error + 100 * delta_temp + 10 * acceleration + 5011	
	print(conjugate)
	if conjugate > 0:
		index = ((conjugate // 100) * 9) + ((float(str(int(conjugate))[-2]) // 10) * 3) + (conjugate % 10)
	else:
		index = 0

	return index


for temp in np.arange(-5.0,5.1,0.1):
	for delta_temp in np.arange(-0.1,0.2,0.1):
		for accel in np.arange(-0.1, 0.2, 0.1):
			state = temp, delta_temp, accel
			index = state_to_index(state)
			print(index)
