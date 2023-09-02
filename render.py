import pygame
import random
from images import ground_images, item_images
from map_generator import map_data_generator
from objects import place_and_render_object


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


def render_grid(self):
    """Renderib (visuaalselt) gridi, mille sees asuv terrain ennast playeri jaoks renderib... Siin ei renderi, teeb ainult gridi"""
    x = 100
    left = self.player_x - x
    top = self.player_y - x
    width = 3 * x
    height = 3 * x

    render_rect = pygame.Rect(left,top,width,height)

    return render_rect  # Rect
