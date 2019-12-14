from Environment.envs.Gridworld import ChestsAndKeys, Direction
import numpy as np
import random

class Agent:
	"""
	Defines an autonomous agent in a chest and keys environment
	"""
	def __init__(self, grid):
		self.grid = grid
	
	def action(self, state):
		raise NotImplementedError
		
	def path_from_to(self, state, start, end):
		""" Returns the (path, total_length) of the optimal path from start to end in a state """
		grid = state[0]
		
		def reconstruct_path(came_from, current):
			""" Reconstructs the path from the current node in the graph. 
			This is a helper function for A* """
			path = [current]
			length = 0
			while current in came_from.keys():
				current = came_from[current]
				path.insert(0, current)
				length += 1
			return path, length
		
		import math
		def minimum_index(f, frontier):
			""" Helper function for returning the index of the node with the lowest f value in the frontier"""
			min_so_var = math.inf
			best_index = 0
			for i in range(len(frontier)):
				n = frontier[i]
				f_val = f[n[0]][n[1]]
				if f_val < min_so_var:
					min_so_far = f_val
					best_index = i
			return frontier[best_index]
		
		def a_star(start, end, heuristic):
			""" An implementation of A* specific to a gridworld environment. 
			This is based on the psuedocode provided by Wikipedia.
			See https://en.wikipedia.org/wiki/A*_search_algorithm """
			
			frontier = [start]
			came_from = {}
			g = [[math.inf for i in range(len(grid[0]))] for j in range(len(grid))]
			g[start[0]][start[1]] = 0
			
			explored = []
			f = [[math.inf for i in range(len(grid[0]))] for j in range(len(grid))]
			f[start[0]][start[1]] = heuristic(start)
			
			while len(frontier) > 0:
				current = minimum_index(f, frontier)
				if current == end:
					return reconstruct_path(came_from, current)
					
				frontier.remove(current)
				explored.append(current)
				neighbors = [Direction.add(current, d) for d in Direction.free_directions(current, self.grid)]
				for neighbor in neighbors:
					if neighbor in explored:
						continue
					tentative_g = g[current[0]][current[1]] + 1
					if tentative_g < g[neighbor[0]][neighbor[1]]:
						came_from[neighbor] = current
						g[neighbor[0]][neighbor[1]] = tentative_g
						f[neighbor[0]][neighbor[1]] = g[neighbor[0]][neighbor[1]] + heuristic(neighbor)
						if not neighbor in frontier:	
							frontier.append(neighbor)
							
			assert "A_star failed to yield a valid path for start: {} and end: {}".format(str(start), str(end))
		
		# Return A* function with a Manhattan distance heuristic
		return a_star(start, end, lambda pos: abs(pos[0] - end[0]) + abs(pos[1] - end[0]))
				
class NeuralNetAgent(Agent):
	def __init__(self, state, neural_network):
		super().__init__(state[0])
		self.model = neural_network
	
	def action(self, state):
		""" Takes an action using the models prediction of the best action """
		prediction = self.model.predict(ChestsAndKeys.embed(state))
		return np.random.choice(5, size = 1, p = prediction)[0]

class RandomAgent(Agent):
	"""
	Defines an agent that takes random legal actions
	"""
	def __init__(self, state):
		super().__init__(state[0])
	
	
	def get_action(self, state):
		""" Returns a random legal direction """
		return random.choice(Direction.free_directions(state[1], state[0]))
		
class GreedyAgent(Agent):
	"""
	Defines an agent that goes to the nearest key if it doesn't have one, and goes to the nearest chest if it has a key.
	"""
	def __init__(self, state):
		super().__init__(state[0])
	
	def get_all_pos(self, state, tile_type):
		""" Returns all the positions where there is a tile_type """
		state_size = len(state[0])
		grid = state[0]
		poses = []
		for i in range(state_size):
			for j in range(state_size):
				if grid[i][j] == tile_type:
					poses.append((i, j))
		return poses
	
	def get_action(self, state):
		""" Returns the first step in a path to the next key or chest depending on whether has a key """
		self.grid = state[0]
		state_size = len(state[0])
		next_state = state[1]
		if state[2] <= 0:
			key_poses = self.get_all_pos(state, 3)
			if key_poses != None:
				all_paths = [self.path_from_to(state, state[1], pos) for pos in key_poses]
				all_paths = [x for x in all_paths if x != None]
				if len(all_paths) > 0:
					shortest_path = min(all_paths, key = lambda t: t[1])
					next_state = shortest_path[0][1]
		else:
			chest_poses = self.get_all_pos(state, 2)
			if chest_poses != None:
				all_paths = [self.path_from_to(state, state[1], pos) for pos in chest_poses]
				all_paths = [x for x in all_paths if x != None]
				if len(all_paths) > 0:
					shortest_path = min(all_paths, key = lambda t: t[1])
					next_state = shortest_path[0][1]
		return Direction.add(next_state, (-state[1][0], -state[1][1]))
	
	def get_nearest_key_action(self, state):
		""" Returns the first step in a path to the next key """
		self.grid = state[0]
		state_size = len(state[0])
		next_state = state[1]
		key_poses = self.get_all_pos(state, 3)
		if key_poses != None:
			all_paths = [self.path_from_to(state, state[1], pos) for pos in key_poses]
			all_paths = [x for x in all_paths if x != None]
			if len(all_paths) > 0:
				shortest_path = min(all_paths, key = lambda t: t[1])
				next_state = shortest_path[0][1]
		return Direction.add(next_state, (-state[1][0], -state[1][1]))
		
class HeuristicAgent(Agent):
	"""
	Defines an agent that takes the strategy recommended by a particular implementation 
	of simulated annealing on the graph version of the problem.
	See the imported document for more information. Credit goes to Louis Francini for writing the solver.
	"""
	def __init__(self, state):
		super().__init__(state[0])
	
	def make_adjacency_matrix(self, state):
		""" Creates an adjacency matrix representation of the Keys and Chest problem 
		Returns (a set of chests indices, a set of keys indices, list of nodes, matrix of distances beteween nodes)"""
		grid = state[0]
		chest_indices = set()
		key_indices = set()
		nodes = []
		current_index = 0
		for y in range(len(grid[0])):
			for x in range(len(grid)):
				# If the part of the grid has a value above a 1, then it is an item
				# See the ChestsAndKeys class variable tilenames for more information
				item = grid[x][y]
				if item > 1:
					nodes.append((x, y))
					if item == 2:
						chest_indices.add(current_index)
					else:
						key_indices.add(current_index)
					current_index += 1
		adjacency_matrix = [[0 for i in range(len(nodes))] for j in range(len(nodes))]
		for i in range(len(nodes)):
			for j in range(len(nodes)):
				start_node = nodes[i]
				end_node = nodes[j]
				adjacency_matrix[i][j] = self.path_from_to(state, start_node, end_node)[1]
			
		return (chest_indices, key_indices, nodes, adjacency_matrix)
		
	def trajectory(self, state):
		""" Returns the trajectory yielded by simulated annealing for solving the corresponding graph problem """
		import common
		from simulated_annealing import solve_annealer
		chest_indices, key_indices, nodes, adjacency_matrix = self.make_adjacency_matrix(state)
		# print(chest_indices, key_indices, nodes, adjacency_matrix)
		path, dist = solve_annealer(adjacency_matrix, key_indices, chest_indices)
		
		def create_trajectory(path):
			""" Returns a trajectory given a path on the grid """
			traj = []
			current_node = path[0]
			for node in path[1:]:
				traj.append(Direction.add(node, (-current_node[0], -current_node[1])))
				current_node = node
			return traj
		
		trajectory = []
		current_pos = state[1]
		for index in path:
			node = nodes[index]
			partial_traj = create_trajectory(self.path_from_to(state, current_pos, node)[0])
			trajectory.extend(partial_traj)
			current_pos = node
			
		return trajectory
	
	def get_action(self, state):
		""" Returns the first step in a trajectory called on the state """
		return self.trajectory(state)[0]
		
