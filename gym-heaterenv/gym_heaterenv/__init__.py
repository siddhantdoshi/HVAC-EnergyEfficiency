from gym.envs.registration import register

register(
	id='HeaterEnv-v0',
	entry_point='gym_heaterenv.envs:HeaterEnv1',
)

register(
	id='HeaterEnv-v1',
	entry_point='gym_heaterenv.envs:HeaterEnv2',
)

register(
	id='HeaterEnv-v2',
	entry_point='gym_heaterenv.envs:HeaterEnv3',
)

register(
	id='HeaterEnv-v3',
	entry_point='gym_heaterenv.envs:HeaterEnv4',
)

register(
	id='HeaterEnv-v4',
	entry_point='gym_heaterenv.envs:HeaterEnv5',
)

register(
	id='HeaterEnv-v5',
	entry_point='gym_heaterenv.envs:HeaterEnv6',
)

register(
	id='HeaterEnvRelay-v0',
	entry_point='gym_heaterenv.envs:HeaterEnvRelay',
)