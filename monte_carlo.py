import numpy as np
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

def local_energy(grid, y, x):
    h, w = grid.shape
    gid = grid[y,x]
    e = 0
    for ny,nx in get_neighbors(y,x,h,w):
        if grid[ny,nx] != gid:
            e += 1
    return e


def monte_carlo_step(grid, mask, temperature):
    h, w = grid.shape
    y = random.randint(0,h-1)
    x = random.randint(0,w-1)

    if not mask[y,x]:
        return

    neighbors = get_neighbors(y,x,h,w)
    ny, nx = random.choice(neighbors)
    old_energy = local_energy(grid,y,x)
    new_gid = grid[ny,nx]
    old_gid = grid[y,x]
    grid[y,x] = new_gid
    new_energy = local_energy(grid,y,x)
    dE = new_energy - old_energy

    if dE <= 0:
        return

    prob = math.exp(-dE / temperature)
    if random.random() > prob:
        grid[y,x] = old_gid