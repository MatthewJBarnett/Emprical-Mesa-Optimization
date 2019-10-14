import Gridworld

class Agent:
	"""
	Defines an autonomous agent in a chest and keys environment
	"""
	def action(state):
		raise NotImplementedError

class GreedyAgent(Agent):
	"""
	Defines an agent that pursues the optimal strategy for receiving the soonest possible next reward
	"""
	
