import numpy as np

# This file mainly includes utilities for writing training data to files, and reading that data
# The intention here is to map states to actions, and build a supervised learner as a first test

class Direction:
	"""
	Defines the available actions for an agent in gridworld
	Some of this code is copied from 
	https://github.com/HumanCompatibleAI/learning_biases/blob/master/gridworld.py
	The next thing to do here is import the class from that file since it's better anyway
	"""
	NORTH = (0, -1)
	SOUTH = (0, 1)
	WEST = (-1, 0)
	EAST = (1, 0)
	STAY = (0, 0)
	INDEX_TO_DIRECTION = [NORTH, EAST, SOUTH, WEST, STAY]
	DIRECTION_TO_INDEX = {a:i for i, a in enumerate(INDEX_TO_DIRECTION)}
	
	@staticmethod
	def get_number_from_direction(direction):
		return Direction.DIRECTION_TO_INDEX[direction]

	@staticmethod
	def get_direction_from_number(number):
		return Direction.INDEX_TO_DIRECTION[number]
	
	def add(v1, v2):
		""" Add two vectors"""
		return (v1[0] + v2[0], v1[1] + v2[1])
	
	def multiply(v, scalar):
		""" Multiply a vector by a scalar"""
		return (v[0] * scalar, v[1] * scalar)
	
	@staticmethod
	def legal_directions(v, dimensions, jumpsize = 1):
		""" Returns the legal directions at a tile, given the coordinates of the box
		and how large of a jump the player is allowed to move in a direction """
		directions = []
		if v[0] - jumpsize >= 0:
			directions += [Direction.multiply(Direction.WEST, jumpsize)]
		if v[0] + jumpsize < dimensions[0]:
			directions += [Direction.multiply(Direction.EAST, jumpsize)]
		if v[1] - jumpsize >= 0:
			directions += [Direction.multiply(Direction.NORTH, jumpsize)]
		if v[1] + jumpsize < dimensions[1]:
			directions += [Direction.multiply(Direction.SOUTH, jumpsize)]
		return directions
	
	@staticmethod
	def free_directions(pos, grid):
		""" Returns the directions that you can move to for a given position on a grid 
		This is specific to gridworlds only"""
		
		potential = Direction.legal_directions(pos, (len(grid[0]), len(grid)))
		free = []
		for d in potential:
			adjacent = Direction.add(pos, d)
			if grid[adjacent[0]][adjacent[1]] != 1:
				free.append(d)
		return free

def path_from_to(state, start, end, grid):
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
				neighbors = [Direction.add(current, d) for d in Direction.free_directions(current, grid)]
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

def get_string_state_action(state, action):
	""" Retreives a string corresponding to the state of a gridworld along with
	an associated action """
	text = ""
	for line in state[0]:
		for char in line:
			text += str(char)
		text += "\n"
	text += str(state[1][0]) + "\n" + str(state[1][1]) + "\n"
	text += str(state[2]) + "\n"
	text += str(Agent.Direction.DIRECTION_TO_INDEX[action]) + "\n\n"
	return text

def write_state_action(state, action, filename):
	""" Appends a (state, action) string to a file """
	f = open(filename, "a+")
	f.write(get_string_state_action(state, action))
	f.close()

def get_samples_from(filename, grid_dimensions):
	""" Retrieves a list of sample (state, action_index) pairs from a .dat file """
	assert filename[-4:] == ".dat"
	
	f = open(filename, 'r+')
	lines = f.readlines()
	
	pairs = []
	block_length = grid_dimensions[1] + 5
	
	for i in range(0, len(lines), block_length):
		grid = [[]]
		for j in range(i, i + grid_dimensions[1]):
			index = (j - i) % grid_dimensions[1]
			for k in range(grid_dimensions[0]):
				grid[index].append(int(lines[j][k]))
			if j < i + grid_dimensions[1] - 1:
				grid.append([])
				
		agent_pos = (int(lines[i + grid_dimensions[1]].replace('\n', '')), \
							int(lines[i + grid_dimensions[1] + 1].replace('\n', '')))
							
		keys = int(lines[i + grid_dimensions[1] + 2].replace('\n', ''))
		
		action_index = int(lines[i + grid_dimensions[1] + 3].replace('\n', ''))
		grid = np.array(grid).tolist()
		pairs.append(((grid, agent_pos, keys), action_index))
		
	f.close()
	
	return pairs
