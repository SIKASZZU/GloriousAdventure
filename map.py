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
        map_width = 40
        map_height = 40
    
        # Initialize the map with default value 99
        glade_map = [[99 for _ in range(map_width)] for _ in range(map_height)]
    
        # Define different terrain areas
        terrain_value = 1
        water_value = 0
        farming_value = 7
        forest_value = 4
    
        # Create a function to fill an area with a specific value
        def fill_area(top_left_x, top_left_y, width, height, value):
            for i in range(top_left_y, top_left_y + height):
                for j in range(top_left_x, top_left_x + width):
                    glade_map[i][j] = value
    
        # Fill the terrain area
        terrain_top_left_x = 1
        terrain_top_left_y = 1
        terrain_width = map_width - 2
        terrain_height = map_height - 2
        fill_area(terrain_top_left_x, terrain_top_left_y, terrain_width, terrain_height, terrain_value)
    
        # Fill the water area
        water_top_left_x = 5
        water_top_left_y = 7
        water_width = map_width // 2 - 7
        water_height = map_height // 2 - 5
        fill_area(water_top_left_x, water_top_left_y, water_width, water_height, water_value)
    
        # Fill the farming area
        farming_top_left_x = map_width - 4
        farming_top_left_y = 1
        farming_width = 3
        farming_height = map_height // 2 - 6
        fill_area(farming_top_left_x, farming_top_left_y, farming_width, farming_height, farming_value)
    
        # Fill the forest areas
        forest_areas = [
            (35, 17, 3, 21),
            (17, 32, 18, 6)
        ]
    
        for top_left_x, top_left_y, width, height in forest_areas:
            fill_area(top_left_x, top_left_y, width, height, forest_value)
    
        return glade_map

