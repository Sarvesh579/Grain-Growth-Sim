import random
import math

def get_neighbors(y, x, h, w):
    neighbors = []
    directions = [
        (-1,0),(1,0),(0,-1),(0,1),   # cardinal
        (-1,-1),(-1,1),(1,-1),(1,1)  # diagonals
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

def monte_carlo_step(grid, orientations, mask, temperature, grains_compete=False):
    h, w = grid.shape
    y = random.randint(0,h-1)
    x = random.randint(0,w-1)

    if not mask[y,x]:
        return

    neighbors = get_neighbors(y,x,h,w)
    ny, nx = random.choice(neighbors)
    neighbor_gid = grid[ny,nx]
    if neighbor_gid == -1:
        return
    current_gid = grid[y,x]

    # EMPTY CELL → immediately adopt neighbor grain
    if grains_compete or current_gid == -1:
        grid[y,x] = neighbor_gid
        orientations[y,x] = orientations[ny,nx]
        return

    # normal grain boundary movement
    diff_neighbors = 0
    same_neighbors = 0

    for ny2,nx2 in neighbors:
        if grid[ny2,nx2] == current_gid:
            same_neighbors += 1
        else:
            diff_neighbors += 1

    current_theta = orientations[y, x]
    neighbor_theta = orientations[ny, nx]
    mis = misorientation(current_theta, neighbor_theta)
    dE = mis / 180

    if dE <= 0:
        grid[y,x] = neighbor_gid
        return
    prob = math.exp(-dE / temperature)
    if random.random() < prob:
        grid[y,x] = neighbor_gid