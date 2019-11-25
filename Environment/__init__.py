from gym.envs.registration import register

register(
    id='CK-v0',
    entry_point='Environment.envs:ChestAndKeysEnv',
)