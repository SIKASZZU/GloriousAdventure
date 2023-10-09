import numpy as np
from perlin_noise import PerlinNoise

class Map_information:

    def map_data_generator(seed=None) -> None:

        color_ranges: list[tuple()] = [
            (-float('inf'), -0.15, ("Water")),

            (-0.15, -0.05, ("Sand")),
            (-0.05, -0.04, ("Flower")),
            (-0.03, -0.02, ("Rock")),
            (-0.01, 0, ("Mushroom")),
            (0, 0.01, ("Tree")),
            (0.01, 0.2, ("Grass")),

            (0.2, float('inf'), ("Water")),
        ]

        # Muuda neid, et muuta mapi suurust
        max_x: int = 50
        max_y: int = 50

        while True:
            for y in range(max_y):
                row = []
                for x in range(max_x):
                    terrain_noise = PerlinNoise(octaves=5, seed=seed)
                    elevation_noise = PerlinNoise(octaves=1, seed=seed)
                    temperature_noise = PerlinNoise(octaves=5, seed=seed)
                    moisture_noise = PerlinNoise(octaves=10, seed=seed)

                    # Teeb listi, et salvestada maailma objectid, mineralid, jne
                    grid_pattern = []

                    for y in range(max_y):
                        row = []
                        for x in range(max_x):
                            terrain_val = terrain_noise([x / max_x, y / max_y])
                            elevation_val = elevation_noise([x / max_x, y / max_y])
                            temperature_val = temperature_noise([x / max_x, y / max_y])
                            moisture_val = moisture_noise([x / max_x, y / max_y])

                            biome_val = terrain_val * 0.2 + elevation_val * 0.5 + temperature_val * 0.25 + moisture_val * 0.25

                            cell_value = None

                            for low, high, tile_value in color_ranges:
                                if low <= biome_val < high:
                                    if tile_value == ("Grass"):
                                        cell_value = 1
                                    elif tile_value == ("Rock"):
                                        cell_value = 2
                                    elif tile_value == ("Sand"):
                                        cell_value = 3
                                    elif tile_value == ("Tree"):
                                        cell_value = 4
                                    elif tile_value == ("Flower"):
                                        cell_value = 5
                                    elif tile_value == ("Mushroom"):
                                        cell_value = 6
                                    else:
                                        cell_value = 0
                                    break

                            row.append(cell_value)

                        grid_pattern.append(row)
                    return grid_pattern