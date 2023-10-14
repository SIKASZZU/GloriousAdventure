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
                            
                            tile_to_cell = {
                                "Grass": 1,
                                "Rock": 2,
                                "Sand": 3,
                                "Tree": 4,
                                "Flower": 5,
                                "Mushroom": 6
                            }

                            for low, high, tile_value in color_ranges:
                                if low <= biome_val < high:
                                    if tile_value in tile_to_cell:
                                        cell_value = tile_to_cell[tile_value]
                                    else:
                                        cell_value = 0
                                    break

                            row.append(cell_value)

                        grid_pattern.append(row)
                    return grid_pattern


    def glade_creation():
        # Define the dimensions of the map
        width = 40
        height = 40

        # Initialize the map with 99s
        map_matrix = [[99 for _ in range(width)] for _ in range(height)]

        # Define the coordinates for the square of terrain (value 1)
        square_top_left_x = 1
        square_top_left_y = 1
        square_width = width - 2
        square_height = height - 2

        # Fill the square area with value 1
        for i in range(square_top_left_y, square_top_left_y + square_height):
            for j in range(square_top_left_x, square_top_left_x + square_width):
                map_matrix[i][j] = 1

        # Define the coordinates for the smaller water bond (value 0)
        water_bond_top_left_x = 5
        water_bond_top_left_y = 7
        water_bond_width = width // 2 - 7
        water_bond_height =  height // 2 - 5

        # Fill the smaller water bond area with value 0
        for i in range(water_bond_top_left_y, water_bond_top_left_y + water_bond_height):
            for j in range(water_bond_top_left_x, water_bond_top_left_x + water_bond_width):
                map_matrix[i][j] = 0

        # Define the coordinates for the farming area (value 7)
        farm_top_left_x = width - 4
        farm_top_left_y = 1
        farm_width = 3
        farm_height = height // 2 - 6

        # Fill the farming area with value 7
        for i in range(farm_top_left_y, farm_top_left_y + farm_height):
            for j in range(farm_top_left_x, farm_top_left_x + farm_width):
                map_matrix[i][j] = 7

        return map_matrix

