import matplotlib.pyplot as plt
import numpy as np

def plot_lattice(grid, mask):
    display = grid.copy().astype(float)
    display[~mask] = np.nan
    plt.imshow(display, cmap="tab20")
    plt.colorbar()
    plt.title("Grain Structure")
    plt.show()