import Agent
import numpy as np

# This file mainly includes utilities for writing training data to files, and reading that data
# The intention here is to map states to actions, and build a supervised learner as a first test

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
