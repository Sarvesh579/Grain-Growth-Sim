import random
import math
import config

def get_neighbors(y, x, h, w):
    neighbors = []
    directions = [
        (-1,0),(1,0),(0,-1),(0,1),
        (-1,-1),(-1,1),(1,-1),(1,1)
    ]
    for dy, dx in directions:
        ny = y + dy
        nx = x + dx
        if 0 <= ny < h and 0 <= nx < w:
            neighbors.append((ny,nx))
    return neighbors


def misorientation(theta1, theta2):
    diff = abs(theta1 - theta2)
    return min(diff, 360 - diff)


def monte_carlo_step(grid, orientations, mask, randomness, grains_compete=False):
    h, w = grid.shape
    y = random.randint(0, h-1)
    x = random.randint(0, w-1)
    if not mask[y, x]:
        return False
    neighbors = get_neighbors(y, x, h, w)
    ny, nx = random.choice(neighbors)
    neighbor_gid = grid[ny, nx]
    if neighbor_gid == -1:
        return False
    current_gid = grid[y, x]

    if not grains_compete:
        if current_gid == -1:
            grid[y, x] = neighbor_gid
            orientations[y, x] = orientations[ny, nx]
            return True
        return False

    current_theta = orientations[y, x]
    neighbor_theta = orientations[ny, nx]
    mis = misorientation(current_theta, neighbor_theta)

    pressure_term = config.PRESSURE * 0.01
    magnetic_term = config.MAG_FIELD * abs(neighbor_theta-current_theta)/360
    electric_term = config.ELEC_FIELD * random.random()*0.01
    dE = mis / 180
    dE += pressure_term + magnetic_term + electric_term

    if dE <= 0:
        was_empty = current_gid == -1
        grid[y, x] = neighbor_gid
        orientations[y, x] = neighbor_theta
        return was_empty

    prob = math.exp(-dE / randomness)

    if random.random() < prob:
        was_empty = current_gid == -1
        grid[y, x] = neighbor_gid
        orientations[y, x] = neighbor_theta
        return was_empty
    return False