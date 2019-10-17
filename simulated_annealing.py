from __future__ import print_function
import math
import random
import common
import greedy
import opt2
from simanneal import Annealer

class ShortestPathAnnealer(Annealer):

    def __init__(self, state, distance_matrix, v):
        self.distance_matrix = distance_matrix
        self.v = v
        super(ShortestPathAnnealer, self).__init__(state)

    def move(self):
        candidate = self.state[:]
        movement = random.choice(['swap', 'rev'])
        if movement == 'swap':
            a = random.randint(0, len(self.state) - 1)
            b = random.randint(0, len(self.state) - 1)
            candidate[a], candidate[b] = self.state[b], self.state[a]
        else:
            l = random.randint(2, len(self.state) - 1)
            i = random.randint(0, len(self.state) - l)
            candidate[i : (i+l)] = reversed(candidate[i : (i + l)])
        valid = common.path_valid(candidate[:len(self.v)*2], self.v)
        if valid:
            self.state = candidate

        return self.energy()

    def energy(self):
        return common.path_distance(self.distance_matrix, self.state[:len(self.v)*2])

def solve_annealer(distance_matrix, v, s):
    opt2_state, opt2_distance = opt2.solve_2opt(distance_matrix, v, s)
    for i in range(10):
        state, distance = opt2.solve_2opt(distance_matrix, v, s)
        if distance < opt2_distance:
            opt2_state, opt2_distance = state, distance
    init_state = opt2_state + list(s - set(opt2_state))

    annealer = ShortestPathAnnealer(init_state, distance_matrix, v)
    schedule = annealer.auto(minutes=0.001)
    # print(schedule)
    annealer.set_schedule(schedule)
    annealer.copy_strategy = "slice"
    state, e = annealer.anneal()

    if opt2_distance < e:
        state, e = opt2_state, opt2_distance

    return state[:len(v)*2], e
