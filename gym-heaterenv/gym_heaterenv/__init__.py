from gym.envs.registration import register

register(
	id='HeaterEnv-v0',
	entry_point='gym_heaterenv.envs:HeaterEnv',
)