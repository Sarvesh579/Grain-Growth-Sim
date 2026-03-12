import random
import math


def get_neighbors(y, x, h, w):

    neighbors = []

    for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:

        ny = y + dy
        nx = x + dx

        if 0 <= ny < h and 0 <= nx < w:
            neighbors.append((ny,nx))

    return neighbors


def monte_carlo_step(grid, mask, temperature):

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
    if current_gid == -1:
        grid[y,x] = neighbor_gid
        return

    # normal grain boundary movement
    diff_neighbors = 0
    same_neighbors = 0

    for ny2,nx2 in neighbors:

        if grid[ny2,nx2] == current_gid:
            same_neighbors += 1
        else:
            diff_neighbors += 1

    dE = diff_neighbors - same_neighbors

    if dE <= 0:
        grid[y,x] = neighbor_gid
        return

    prob = math.exp(-dE / temperature)

    if random.random() < prob:
        grid[y,x] = neighbor_gid