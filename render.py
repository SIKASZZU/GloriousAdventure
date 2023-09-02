import pygame
from map_generator import map_data_generator


grid_pattern = map_data_generator() # world data, terraindata  # list

def render_data(self, collison_x, collison_y, object_id):
    for hit_box_x, hit_box_y, hit_box_width, hit_box_height, object_id,\
        hit_box_offset_x, hit_box_offset_y in self.hit_boxes:

        # Saame olemasoleva blocki TOP-LEFT koordinaadid
        terrain_x = hit_box_x - hit_box_offset_x
        terrain_y = hit_box_y - hit_box_offset_y
    
    # teha grid x ja y-ist
    if object_id == 2:
        block_size = self.block_size

    if object_id == 4:
        block_size = self.block_size * 2
        terrain_x = terrain_x - self.block_size / 2
        terrain_y = terrain_y - self.block_size


    single_grid = pygame.Rect(collison_x, collison_y, block_size, block_size)


    # gridpattern[] 