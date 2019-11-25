from gym.envs.registration import register

register(
    id='ChestAndKeys-v0',
    entry_point='gym_ChestAndKeys.envs:Gridworld',
)
