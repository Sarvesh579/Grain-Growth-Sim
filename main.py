import os
import shutil
from tqdm import tqdm
from image_loader import load_shape_mask
from lattice import initialize_lattice
from monte_carlo import monte_carlo_step
from visualizer import save_frame, animate_frames
from config import *
import config
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=config.NUM_SEEDS)
    parser.add_argument("--rand", type=float, default=config.RANDOMNESS)
    parser.add_argument("--mask", type=str, default=config.MASK_PATH)
    parser.add_argument("--fps", type=int, default=config.FPS)
    return parser.parse_args()

def clear_output():
    if os.path.exists(FRAME_FOLDER):
        shutil.rmtree(FRAME_FOLDER)
    os.makedirs(FRAME_FOLDER)

def reduce_frames_to_target(folder,target_frames):
    files=sorted([f for f in os.listdir(folder) if f.startswith("frame_")])
    total=len(files)
    if total<=target_frames:
        return
    step=total/target_frames
    keep=set(int(i*step) for i in range(target_frames))
    for idx,f in enumerate(files):
        if idx not in keep:
            os.remove(os.path.join(folder,f))

def main():
    clear_output()
    args = parse_args()
    NUM_SEEDS = args.seeds
    RANDOMNESS = args.rand
    MASK_PATH = args.mask
    FPS = args.fps
    mask=load_shape_mask(MASK_PATH, resize=(200,200))
    grid,orientations=initialize_lattice(mask, NUM_SEEDS)
    total_pix=int(mask.sum())
    filled_pix = NUM_SEEDS
    step=0
    frame_count=0
    print("Running Monte Carlo Simulation")
    pbar=tqdm(total=total_pix, unit="pixels")
    while True:
        new_fill=monte_carlo_step(grid, orientations, mask, RANDOMNESS, GRAINS_COMPETE)
        if new_fill:
            filled_pix+=1
        if step%FRAME_INTERVAL==0:
            save_frame(grid, mask, frame_count)
            frame_count+=1
            pbar.n=filled_pix
            pbar.set_postfix({"steps":step})
            pbar.refresh()
            if filled_pix>=total_pix:
                break
        step+=1
    pbar.close()
    print("Reducing frames...")
    reduce_frames_to_target(FRAME_FOLDER, TARGET_FRAMES)
    print("Simulation complete")
    animate_frames(FRAME_FOLDER, fps=FPS)

if __name__=="__main__":
    main()
