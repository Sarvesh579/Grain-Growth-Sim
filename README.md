# Stochastic Monte Carlo Grain Growth Simulation

Python simulation of crystal grain growth inside arbitrary 2D shapes using a Monte Carlo lattice model.

## Features
- Load a black/white image mask as the material shape
- Initialize random grain seeds
- Simulate stochastic grain boundary evolution
- Visualize grain growth as an animation

## Tech Stack
Python, NumPy, Matplotlib, Pillow

## Installation

```bash
pip install numpy matplotlib pillow tqdm
````

## Run

```bash
python main.py
```

Place your shape image inside:
```
input_shapes/shape.png
```
### Note:
White = material region
Black = outside region.

