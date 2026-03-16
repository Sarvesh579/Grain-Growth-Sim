import numpy as np

def initialize_lattice(mask, num_seeds):
    h,w = mask.shape
    grid = -np.ones((h,w),dtype=int)
    orientations = np.zeros((h,w))

    valid_positions = np.argwhere(mask)
    seed_indices = np.random.choice(len(valid_positions),num_seeds,replace=False)
    seeds = valid_positions[seed_indices]

    seed_orientations = np.random.rand(num_seeds)*360

    for i,(y,x) in enumerate(seeds):
        grid[y,x]=i
        orientations[y,x]=seed_orientations[i]

    return grid,orientations