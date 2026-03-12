import numpy as np
from PIL import Image

def load_shape_mask(path, resize=None):
    img = Image.open(path).convert("L")
    if resize:
        img = img.resize(resize)
    arr = np.array(img)
    mask = arr > 128
    return mask