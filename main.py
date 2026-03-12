import numpy as np
from tqdm import tqdm
from image_loader import load_shape_mask
from lattice import initialize_lattice
from monte_carlo import monte_carlo_step
from visualizer import plot_lattice


MASK_PATH = "input_shapes/shape.png"
NUM_SEEDS = 50
TEMPERATURE = 0.1
ITERATIONS = 200000

def main():
    mask = load_shape_mask(MASK_PATH, resize=(200,200))
    grid, orientations = initialize_lattice(mask, NUM_SEEDS)
    print("Running Monte Carlo Simulation")
    for _ in tqdm(range(ITERATIONS)):
        monte_carlo_step(grid, mask, TEMPERATURE)
    plot_lattice(grid, mask)


if __name__ == "__main__":
    main()