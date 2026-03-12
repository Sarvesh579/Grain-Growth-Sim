import os
import shutil
import numpy as np
from tqdm import tqdm

from image_loader import load_shape_mask
from lattice import initialize_lattice
from monte_carlo import monte_carlo_step
from visualizer import save_frame, animate_frames

MASK_PATH = "input_shapes/shape.png"
NUM_SEEDS = 50
TEMPERATURE = 0.5
ITERATIONS = 200000
FRAME_INTERVAL = 3000
TARGET_FRAMES = 1200
FPS = 24


def clear_output():
    folder = "output"
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

def is_filled(grid, mask):
    return not ((grid == -1) & mask).any()

def main():
    clear_output()
    mask = load_shape_mask(MASK_PATH, resize=(200,200))
    grid, orientations = initialize_lattice(mask, NUM_SEEDS)
    white_pixels = mask.sum()
    ITERATIONS = int(white_pixels * 20)
    FRAME_INTERVAL = max(1, ITERATIONS // TARGET_FRAMES)
    print(f"Estimated iterations: {ITERATIONS}")
    frame_count = 0
    print("Running Monte Carlo Simulation")

    for i in tqdm(range(ITERATIONS)):
        monte_carlo_step(grid, mask, TEMPERATURE)
        if i % FRAME_INTERVAL == 0:
            save_frame(grid, mask, i)

    print("Simulation complete")
    animate_frames(fps=FPS)


if __name__ == "__main__":
    main()