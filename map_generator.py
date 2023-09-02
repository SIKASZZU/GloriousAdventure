import time
import pygame
import numpy as np
import matplotlib.pyplot as plt
import random

from images import ground_images, item_images
from objects import place_and_render_object, remove_object_at_position, add_object_to_inv
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
            
def map_render(self):
    self.screen.fill('blue')

    # Loop through terrain data and render water and land
    for i in range(len(self.terrain_data)):
        for j in range(len(self.terrain_data[i])):
            terrain_x = j * self.block_size + self.offset_x
            terrain_y = i * self.block_size + self.offset_y

            # Check if terrain_data value is 1 (land)
            if self.terrain_data[i][j] == 1:
                # Check if ground image is already generated and cached
                if (i, j) not in self.generated_ground_images:
                    ground_image_name = f"Ground_{random.randint(0, 19)}"
                    ground_image = ground_images.get(ground_image_name)
                    self.generated_ground_images[(i, j)] = ground_image

                # Render the ground image if it exists
                ground_image = self.generated_ground_images.get((i, j))
                if ground_image:
                    ground_image = pygame.transform.scale(ground_image, (self.block_size, self.block_size))
                    self.screen.blit(ground_image, (terrain_x, terrain_y))

def object_render(self):

    # Loopib läbi terrain data ja saab x ja y
    for i in range(len(self.terrain_data)):
        for j in range(len(self.terrain_data[i])):
            terrain_x = j * self.block_size + self.offset_x
            terrain_y = i * self.block_size + self.offset_y

            if self.terrain_data[i][j] == 2 or self.terrain_data[i][j] == 4:
                self.terrain_data_minerals += 1

            # Jätab muud blockid välja millele pole hit boxe vaja
            if self.terrain_data[i][j] != 0:

                # Peavad olema muidu järgnevates if statementides tulevad errorid
                object_id = self.terrain_data[i][j]
                obj_image = None
                obj_width = 0
                obj_height = 0
                hit_box_width = 0
                hit_box_height = 0
                hit_box_color = ''
                hit_box_offset_x = 0
                hit_box_offset_y = 0

                # Vaatab kas terrain data on kivi
                if object_id == 2:
                    obj_image = item_images.get("Rock")
                    hit_box_color = 'green'

                    obj_width = int(self.block_size * 1)
                    obj_height = int(self.block_size * 0.8)

                    # Pane TOP-LEFT otsa järgi paika
                    # ja siis muuda - palju lihtsam
                    hit_box_width = int(obj_width * 0.5)
                    hit_box_height = int(obj_height * 0.5)
                    hit_box_offset_x = int(obj_width * 0.3)
                    hit_box_offset_y = int(obj_height * 0.25)

                # Vaatab kas terrain data on puu
                elif object_id == 4:
                    obj_image = item_images.get("Tree")
                    hit_box_color = 'green'

                    # Pane TOP-LEFT otsa järgi paika
                    # ja siis muuda - palju lihtsam
                    obj_width = int(self.block_size * 2)
                    obj_height = int(self.block_size * 2)
                    hit_box_width = int(obj_width * 0.25)
                    hit_box_height = int(obj_height * 0.65)

                    hit_box_offset_x = int(obj_width * 0.4)
                    hit_box_offset_y = int(obj_height * 0.2)

                # Arvutab hit boxi positsiooni
                # Default hit box on terrain_x ja terrain_y
                hit_box_x = terrain_x + hit_box_offset_x
                hit_box_y = terrain_y + hit_box_offset_y

                if object_id != 0:
                    if object_id != 1:
                        if self.display_hit_box_decay <= self.terrain_data_minerals:
                            self.hit_boxes.append((hit_box_x, hit_box_y, hit_box_width, hit_box_height, object_id, hit_box_offset_x, hit_box_offset_y))
                            self.display_hit_box_decay += 1
                            
                        place_and_render_object(self, object_id, obj_image, terrain_x, terrain_y, obj_width, obj_height, hit_box_color, hit_box_x, hit_box_y, hit_box_width, hit_box_height)

    self.terrain_data_minerals = 0
