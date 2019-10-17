import common
import greedy

def swap_2opt(route, i, k):
	new_route = route[0:i]
	new_route.extend(reversed(route[i:k + 1]))
	new_route.extend(route[k+1:])
	return new_route

def solve_2opt(matrix, v, s, n=100):
	improvement = True
	best_route, best_distance = greedy.best_of_greedy(matrix, v, s, n)
	best_route += list(s - set(best_route))
	while improvement: 
		improvement = False
		for i in range(len(v)*2 - 1):
			for k in range(i+1, len(v)*2):
				new_route = swap_2opt(best_route, i, k)
				if common.path_valid(new_route[:len(v)*2], v):
					new_distance = common.path_distance(matrix, new_route[:len(v)*2])
					if new_distance < best_distance:
						# print(best_distance, new_distance)
						best_distance = new_distance
						best_route = new_route
						improvement = True
						break #improvement found, return to the top of the while loop
			if improvement:
				break
	return best_route[:len(v)*2], best_distance
