import numpy as np

def initialize_lattice(mask, num_seeds):
    h, w = mask.shape

    grain_ids = -np.ones((h, w), dtype=int)
    orientations = np.zeros((h, w))

    valid_positions = np.argwhere(mask)

    seed_positions = valid_positions[
        np.random.choice(len(valid_positions), num_seeds, replace=False)
    ]

    for i, (y, x) in enumerate(seed_positions):
        grain_ids[y, x] = i
        orientations[y, x] = np.random.rand() * 360

    return grain_ids, orientations