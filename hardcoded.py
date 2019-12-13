from Environment.envs.Gridworld import Direction, ChestsAndKeys, ChestsAndKeysSpecial
from Agent import GreedyAgent
import time
import Utilities
import random

total_reward = 0
for j in range(10000):
	global_env = ChestsAndKeys((10, 10), 2, 9, drawing = False)
	env = ChestsAndKeysSpecial(5, global_env.state(), drawing = False)
	model = GreedyAgent(env.state())
	for i in range(10):
		action = model.get_action(env.state())
		state, rewards = env.take_action(action)
		#env.draw()
		total_reward += rewards
	
print("Average reward: ", total_reward / 10000.0)
