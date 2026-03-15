import os
import shutil
import numpy as np
import math
from tqdm import tqdm
from image_loader import load_shape_mask
from lattice import initialize_lattice
from monte_carlo import monte_carlo_step
from visualizer import save_frame, animate_frames

MASK_PATH = "input_shapes/shape.png"
NUM_SEEDS = 50
TEMPERATURE = 0.5
FRAME_INTERVAL = 3000
FPS = 24
DURATION = 5
TARGET_FRAMES = 1200
GRAINS_COMPETE = True

def clear_output():
    folder = "output"
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

def is_shape_filled(grid, mask, total_white):
    filled_pixels = ((grid != -1) & mask).sum()
    return filled_pixels >= total_white

def reduce_frames_to_target(folder, target_frames):
    files = sorted([
        f for f in os.listdir(folder)
        if f.startswith("frame_")
    ])
    total = len(files)
    if total <= target_frames:
        return
    step = total / target_frames
    keep_indices = set(int(i * step) for i in range(target_frames))
    for idx, f in enumerate(files):
        if idx not in keep_indices:
            os.remove(os.path.join(folder, f))

def main():
    clear_output()
    mask = load_shape_mask(MASK_PATH, resize=(200,200))
    grid, orientations = initialize_lattice(mask, NUM_SEEDS)
    total_pixels = mask.sum()
    i = 0
    frame_count = 0
    print("Running Monte Carlo Simulation")
    pbar = tqdm(unit="steps")
    while True:
        monte_carlo_step(grid, orientations, mask, TEMPERATURE, GRAINS_COMPETE)
        if i % FRAME_INTERVAL == 0:
            save_frame(grid, mask, frame_count)
            frame_count += 1
            if is_shape_filled(grid, mask, total_pixels):
                break
        i += 1
        pbar.update(1)
    pbar.close()
    print("Simulation complete")
    animate_frames(fps=FPS)


if __name__ == "__main__":
    main()