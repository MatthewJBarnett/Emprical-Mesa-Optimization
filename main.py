import Gridworld

world = Gridworld.ChestsAndKeys((9, 9), 10, 3, drawing = True)
line_in = ""
while line_in != "quit":
	world.draw()
	print()
	print("Enter 0 - 4 for (North, East, South, West, Stay) respectively")
	print("Or enter 'quit' to exit")
	line_in = input()
	if line_in in [str(i) for i in list(range(5))]:
		option = int(line_in)
		if option >= 0 and option <= 5:
			state, reward = world.take_action(Gridworld.Direction.INDEX_TO_DIRECTION[option])
			print()
			print("Agent got ", reward, " reward")
			print()

world.exit_drawing()

