import random
import math
import matplotlib.pyplot as plt

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def generate_points(n_v, n_s):
    assert(n_s >= n_v)

    points = [(random.uniform(0, 100), random.uniform(0, 100))
        for _ in range(n_v + n_s)]

    v = set(range(n_v))
    s = set(range(n_v, n_v + n_s))

    return (points, v, s)

def generate_distance_matrix(points):
    return [[distance(p1, p2) for p2 in points] for p1 in points]

def path_distance(distance_matrix, path):
    """Calculates the length of the route."""
    d = 0
    for i in range(len(path) - 1):
        d += distance_matrix[path[i]][path[i+1]]
    return d

def path_valid(path, v):
    """Checks if a path is valid"""
    acc = 0
    for i in path:
        if i in v:
            acc += 1
        else:
            acc -= 1
        if acc < 0: return False
    return True

def plot(points, v, path):
    plt.plot([points[i][0] for i in path], [points[i][1] for i in path], '-')
    plt.scatter([p[0] for p in points], [p[1] for p in points], c=[('blue' if i in v else 'red') for i in range(len(points))])

