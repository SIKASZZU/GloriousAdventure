# Thanks, https://github.com/pvigier/perlin-numpy

import numpy as np
import matplotlib.pyplot as plt

from perlin_noise import PerlinNoise
from matplotlib.colors import LinearSegmentedColormap

def map_data_generator(seed=None):

    # Värvib maailma
    color_ranges = [
        (-float('inf'), -0.1, (0.0, 0.2, 0.8)),  # Ocean (Blue)
        (-0.1, 0, (0.95, 0.87, 0.57)),  # Beach (Sand)
        (0, 0.1, (0.29, 0.47, 0.18)),  # Plains (Green)
        (0.1, 0.15, (0.18, 0.32, 0.15)),  # Forest (Dark Green)
        (0.15, 0.2, (0.29, 0.47, 0.18)),  # Plains (Green)
        (0.2, float('inf'), (0.0, 0.2, 0.8)),  # Ocean (Blue)
    ]
    
    # Convert color values to LinearSegmentedColormap format
    colors = [color for _, _, color in color_ranges]
    cmap = LinearSegmentedColormap.from_list('custom_cmap', colors)

    terrain_noise = PerlinNoise(octaves=10)
    elevation_noise = PerlinNoise(octaves=1)
    temperature_noise = PerlinNoise(octaves=5)
    moisture_noise = PerlinNoise(octaves=10)

    xpix, ypix = 50, 50
    pic = np.zeros((xpix, ypix, 3), dtype=np.float32)  # Create an RGB array

    water_threshold = 0.45
    check_seed = seed
    # Kui vett on liiga palju siis loopib läbi ja otsib sobiva maailma
    while True:

        # Kui seedi ei ole ette antud
        if check_seed is None:
            seed = np.random.randint(0, 1000)
        # Initialize the grid pattern as a list of lists
        grid_pattern = []

        for y in range(ypix):
            row = []
            for x in range(xpix):
                terrain_noise = PerlinNoise(octaves=10, seed=seed)  # Map geni manipuleerimiseks
                elevation_noise = PerlinNoise(octaves=1, seed=seed)  # Map geni manipuleerimiseks
                temperature_noise = PerlinNoise(octaves=5, seed=seed)  # Map geni manipuleerimiseks
                moisture_noise = PerlinNoise(octaves=10, seed=seed)  # Map geni manipuleerimiseks

                pic = np.zeros((xpix, ypix, 3), dtype=np.float32)  # RGB array

                # Initialize the grid pattern as a list of lists
                grid_pattern = []

                for y in range(ypix):
                    row = []
                    for x in range(xpix):
                        terrain_val = terrain_noise([x / xpix, y / ypix])
                        elevation_val = elevation_noise([x / xpix, y / ypix])
                        temperature_val = temperature_noise([x / xpix, y / ypix])
                        moisture_val = moisture_noise([x / xpix, y / ypix])

                        biome_val = elevation_val * 0.5 + temperature_val * 0.25 + moisture_val * 0.25

                        cell_value = None

                        for low, high, color in color_ranges:
                            if low <= biome_val < high:
                                if color == (0.0, 0.2, 0.8):
                                    cell_value = 0
                                elif color == (0.95, 0.87, 0.57):
                                    cell_value = 0
                                elif color == (0.29, 0.47, 0.18):
                                    cell_value = 1
                                elif color == (0.18, 0.32, 0.15):
                                    cell_value = 4
                                break

                        row.append(cell_value)

                    grid_pattern.append(row)
                return grid_pattern
            
