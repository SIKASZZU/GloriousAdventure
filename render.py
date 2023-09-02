import pygame
from map_generator import map_data_generator
import random
from images import ground_images, item_images
from objects import place_and_render_object, remove_object_at_position


class Collision_Checker:
    def __init__(self):
        self.grid_pattern = map_data_generator()  # world data, terraindata  # list
        self.generated_ground_images = {}
        self.display_hit_box_decay = 0
    def render_data(self, collison_x, collison_y, object_id):
        for hit_box_x, hit_box_y, hit_box_width, hit_box_height, object_id, \
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

    def render_grid(self):
        x = 125
        left = self.player_x - x
        top = self.player_y - x
        width = 3 * x
        height = 3 * x

        render_rect = pygame.Rect(left, top, width, height)
        return render_rect  # Rect

    def map_render(self):
        self.render_terrain_data = []
        self.screen.fill('blue')
        self.render_range = 9  # Muudab renerimise suurust

        player_grid_row = int(self.player_x // self.block_size)
        player_grid_col = int(self.player_y // self.block_size)

        for i in range(player_grid_col - self.render_range, player_grid_col + self.render_range + 1):
            row = []
            for j in range(player_grid_row - self.render_range, player_grid_row + self.render_range + 1):

                terrain_x = j * self.block_size + self.offset_x
                terrain_y = i * self.block_size + self.offset_y
                row.append(self.terrain_data[i][j])

                # Kontrollib kas terrain block jääb faili self.terrain_data piiridesse
                if 0 <= i < len(self.terrain_data) and 0 <= j < len(self.terrain_data[i]):
                    # Vaatab kas terrain data on 1
                    if self.terrain_data[i][j] == 1:

                        # Vaatab kas ground pilt on juba olemas
                        if (i, j) not in self.generated_ground_images:
                            ground_image_name = f"Ground_{random.randint(0, 19)}"
                            ground_image = ground_images.get(ground_image_name)
                            self.generated_ground_images[(i, j)] = ground_image

                        # Renderib ground pidid kui need eksisteerivad
                        ground_image = self.generated_ground_images.get((i, j))
                        if ground_image:
                            ground_image = pygame.transform.scale(ground_image, (self.block_size, self.block_size))
                            self.screen.blit(ground_image, (terrain_x, terrain_y))
            self.render_terrain_data.append(row)

    def object_render(self):
        # Loopib läbi terrain data ja saab x ja y

        for i in range(len(self.render_terrain_data)):
            for j in range(len(self.render_terrain_data)):

                terrain_x = j * self.block_size + self.offset_x
                terrain_y = i * self.block_size + self.offset_y
                if self.render_terrain_data[i][j] == 2 or self.render_terrain_data[i][j] == 4:
                    self.terrain_data_minerals += 1

                # Jätab muud blockid välja millele pole hit boxe vaja
                if self.render_terrain_data[i][j] != 0:

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
                    if object_id == 4:
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
                                self.hit_boxes.append((hit_box_x, hit_box_y, hit_box_width, hit_box_height, object_id,
                                                       hit_box_offset_x, hit_box_offset_y))
                                self.display_hit_box_decay += 1

                            place_and_render_object(self, object_id, obj_image, terrain_x, terrain_y, obj_width,
                                                    obj_height,
                                                    hit_box_color, hit_box_x, hit_box_y, hit_box_width, hit_box_height)

        self.terrain_data_minerals = 0
        self.display_hit_box_decay = 0
