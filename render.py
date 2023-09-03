import pygame
from map_generator import map_data_generator
import random
from images import ground_images, water_images, item_images
from objects import place_and_render_object, remove_object_at_position


class Rendering:
    def __init__(self):
        self.grid_pattern = map_data_generator()  # world data, terraindata  # list
        self.display_hit_box_decay = 0

        # Tee dict et tile pilti maailma lisada
        self.generated_ground_images = {}
        self.generated_water_images = {}


    def render_grid(self):
        x = 125
        left = self.player_x - x
        top = self.player_y - x
        width = 3 * x
        height = 3 * x

        render_rect = pygame.Rect(left, top, width, height)
        return render_rect  # Rect

    def map_render(self):
        self.screen.fill('white')
        self.render_range = 9  # Muudab renerimise suurust

        player_grid_row = int(self.player_x // self.block_size)
        player_grid_col = int(self.player_y // self.block_size)

        for i in range(player_grid_col - self.render_range, player_grid_col + self.render_range + 1):
            for j in range(player_grid_row - self.render_range, player_grid_row + self.render_range + 1):
                terrain_x = j * self.block_size + self.offset_x
                terrain_y = i * self.block_size + self.offset_y

                # Kontrollib kas terrain block jääb faili self.terrain_data piiridesse
                if 0 <= i < len(self.terrain_data) and 0 <= j < len(self.terrain_data[i]):

                    # Vaatab kas terrain data on 1
                    if self.terrain_data[i][j] != 0:
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

                    if self.terrain_data[i][j] == 0:
                        # Vaatab kas water pilt on juba olemas
                        if (i, j) not in self.generated_water_images:
                            generated_water_images = f"Water_{random.randint(0, 0)}"
                            water_image = water_images.get(generated_water_images)
                            self.generated_water_images[(i, j)] = water_image

                        # Renderib water pidid kui need eksisteerivad
                        water_image = self.generated_water_images.get((i, j))
                        if water_image:
                            water_image = pygame.transform.scale(water_image, (self.block_size, self.block_size))
                            self.screen.blit(water_image, (terrain_x, terrain_y))


    def object_render(self):
        # Loopib läbi terrain data ja saab x ja y
        for i in range(len(self.terrain_data)):
            for j in range(len(self.terrain_data[i])):
                terrain_x = j * self.block_size + self.offset_x
                terrain_y = i * self.block_size + self.offset_y

                if self.terrain_data[i][j] == 2 or self.terrain_data[i][j] == 4: self.terrain_data_minerals += 1

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
                    hit_box_color = 'green'

                    # Vaatab kas terrain data on kivi
                    if object_id == 2:
                        obj_image = item_images.get("Rock")

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

                    if object_id != 0 or 1:
                        if self.display_hit_box_decay <= self.terrain_data_minerals:
                            self.hit_boxes.append((hit_box_x, hit_box_y, hit_box_width, hit_box_height, object_id, hit_box_offset_x, hit_box_offset_y))
                            self.display_hit_box_decay += 1

                        place_and_render_object(self, object_id, obj_image, terrain_x, terrain_y, obj_width, obj_height, hit_box_color, hit_box_x, hit_box_y, hit_box_width, hit_box_height)
        self.terrain_data_minerals = 0
