import Gridworld
import Agent
import time
import Utilities

# This generates training data right now
# Later I'll make a specialized function for it
'''
for i in range(12000):
	print(i)
	world = Gridworld.ChestsAndKeys((5, 5), 4, 2, drawing = False)
	agent = Agent.HeuristicAgent(world.state())
	trajectory = agent.trajectory(world.state())
	state = world.state()
	for action in trajectory:
		Utilities.write_state_action(state, action, "training.dat")
		state, reward = world.take_action(action)
		if world.item_count(3) < 1:
			break
'''
# This is a demo for reading in the training data and outputting the first points
# I'll need to figure out how to embed the training data (that's the next step of the project)	
'''
for i in range(10):
	print(Utilities.get_samples_from("training.dat", (5, 5))[i])
'''
