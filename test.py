import common
from simulated_annealing import solve_annealer

points, v, s = common.generate_points(5, 5)
matrix = common.generate_distance_matrix(points)

path, dist = solve_annealer(matrix, v, s)
print(path, dist)
