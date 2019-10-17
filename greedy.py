import random
import common

def solve_greedy(distance_matrix, v, s):
    current = random.choice(tuple(v))
    path = [current]

    free_v = set(v)
    free_v.remove(current)
    free_s = set(s)

    acc = 1

    while free_v or len(s-free_s)<len(v):
        free = free_v if (acc == 0) else (free_v | free_s)
        next_node = min(free, key=lambda x: distance_matrix[current][x])
        if next_node in free_v:
            acc += 1
            free_v.remove(next_node)
        else:
            acc -= 1
            free_s.remove(next_node)
        path.append(next_node)
        current = next_node

    return path, common.path_distance(distance_matrix, path)

def best_of_greedy(distance_matrix, v, s, n):
    best_path, best_distance = solve_greedy(distance_matrix, v, s)
    for i in range(n-1):
        path, distance = solve_greedy(distance_matrix, v, s)
        if distance < best_distance:
            best_path, best_distance = path, distance
    return best_path, best_distance
    
