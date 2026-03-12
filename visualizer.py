import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib import animation


def save_frame(grid, mask, step, folder="output"):

    os.makedirs(folder, exist_ok=True)

    display = grid.copy().astype(float)
    display[~mask] = np.nan

    fig, ax = plt.subplots(figsize=(6,6))

    im = ax.imshow(display, cmap="tab20")

    ax.set_title(f"Step {step}")
    ax.axis("off")

    fig.colorbar(im, ax=ax, label="Grain ID")

    filename = f"{folder}/frame_{step:05d}.png"
    plt.savefig(filename, bbox_inches="tight", pad_inches=0)
    plt.close()


def animate_frames(folder="output", fps=30):
    import os
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    files = sorted([
        f"{folder}/{f}" for f in os.listdir(folder)
        if f.startswith("frame_")
    ])

    fig, ax = plt.subplots()
    ax.axis("off")
    img = plt.imread(files[0])
    im = ax.imshow(img)
    def update(frame):
        img = plt.imread(files[frame])
        im.set_data(img)
        return [im]
    ani = FuncAnimation(
        fig,
        update,
        frames=len(files),
        interval=1000/fps,
        blit=True
    )
    plt.show()