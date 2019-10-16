import Gridworld

class Agent:
	"""
	Defines an autonomous agent in a chest and keys environment
	"""
	def action(state):
		raise NotImplementedError
	
	def path_from_to(state, start, end):
		""" Returns the (path, total_length) of the optimal path from start to end in a state """
		def a_star(start, end, heuristic):
			

class HeuristicAgent(Agent):
	"""
	Defines an agent that takes the strategy recommended by 2 opt
	See this article on 2 opt: http://pedrohfsd.com/2017/08/09/2opt-part1.html
	"""
	def trajectory(state):
		""" Returns the trajectory yielded by 2-opt for a given state """
		raise NotImplementedError
