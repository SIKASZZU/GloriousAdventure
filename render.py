import pygame
import random
from images import ground_images, water_images, item_images
from objects import Object_Management # place_and_render_hitbox, place_and_render_object

class Render_Checker:
    #display_hit_box_decay: int = 0
    #index: int = 0

    def map_render(self) -> None:
        self.screen.fill('white')
        self.render_terrain_data: list = []

        # Renderiks kogu maailma ära ja siis muutub else statementis olevaks intager'iks
        if self.index < 10:
            self.render_range: int = 70  # Muudab renerimise suurust
            self.index += 1
        else: self.render_range: int = 8

        player_grid_row = int(self.player_x // self.block_size)
        player_grid_col = int(self.player_y // self.block_size)

        for i in range(player_grid_col - self.render_range, player_grid_col + self.render_range + 1):
            self.row: list[int, ...] = []
            for j in range(player_grid_row - self.render_range, player_grid_row + self.render_range + 1):
                terrain_x: int = j * self.block_size + self.offset_x
                terrain_y: int = i * self.block_size + self.offset_y

                try: self.row.append(self.terrain_data[i][j])
                except IndexError: pass

                # Kontrollib kas terrain block jääb faili self.terrain_data piiridesse
                if 0 <= i < len(self.terrain_data) and 0 <= j < len(self.terrain_data[i]):
                    terrain_value = self.terrain_data[i][j]

                    if terrain_value != 0 and (i, j) not in self.generated_ground_images:
                        ground_image_name = f"Ground_{random.randint(0, 19)}"
                        self.generated_ground_images[(i, j)] = pygame.transform.scale(ground_images.get(ground_image_name), (self.block_size, self.block_size))

                    if terrain_value == 0 and (i, j) not in self.generated_water_images:
                        generated_water_images = f"Water_{random.randint(0, 0)}"
                        self.generated_water_images[(i, j)] = pygame.transform.scale(water_images.get(generated_water_images), (self.block_size, self.block_size))

                    image = self.generated_ground_images.get((i, j)) if terrain_value != 0 else self.generated_water_images.get((i, j))
                    if image:
                        self.screen.blit(image, (terrain_x, terrain_y))
                else:
                    if (i, j) not in self.generated_water_images:
                        generated_water_images = f"Water_{random.randint(0, 0)}"
                        self.generated_water_images[(i, j)] = pygame.transform.scale(water_images.get(generated_water_images), (self.block_size, self.block_size))
                        
                    image = self.generated_water_images.get((i, j))
                    if image:
                        self.screen.blit(image, (terrain_x, terrain_y))
                        
            # Teeb chunki render range laiuselt - test_list = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
            self.render_terrain_data.append(self.row)

    def object_list_creation(self) -> None:
        """See func, object_list_creation, teeb ainult self.hit_boxes listi. Appendib sinna world objecktid."""

        player_grid_row = int(self.player_x // self.block_size)
        player_grid_col = int(self.player_y // self.block_size)

        # Et ei tekiks lõpmatus arv pilte ühe ja sama objecti kohta
        self.terrain_data_minerals: int = 0

        for i in range(player_grid_col - self.render_range, player_grid_col + self.render_range + 1):
            for j in range(player_grid_row - self.render_range, player_grid_row + self.render_range + 1):

                # Ei renderi asju mapist välja
                if 0 <= i < len(self.terrain_data) and 0 <= j < len(self.terrain_data[0]):

                    # Kui terrain data [i][j] on suurem kui 1 siis arvutab
                    # objecti asukoha ja hitboxi ning displayib pildi
                    if self.terrain_data[i][j] > 1:
                        terrain_x: int = j * self.block_size + self.offset_x
                        terrain_y: int = i * self.block_size + self.offset_y
                        object_id: int = self.terrain_data[i][j]

                        object_width: int = 0
                        object_height: int = 0
                        hit_box_width: int = 0
                        hit_box_height: int = 0
                        hit_box_offset_x: int = 0
                        hit_box_offset_y: int = 0

                        if object_id > 1: self.terrain_data_minerals += 1

                        if object_id == 2:
                            object_width = int(self.block_size * 1)
                            object_height = int(self.block_size * 0.8)
                            hit_box_width = int(object_width * 0.5)
                            hit_box_height = int(object_height * 0.5)
                            hit_box_offset_x = int(object_width * 0.3)
                            hit_box_offset_y = int(object_height * 0.25)

                        elif object_id == 4:
                            # Pane TOP-LEFT otsa järgi paika
                            # ja siis muuda - palju lihtsam
                            object_width = int(self.block_size * 2)
                            object_height = int(self.block_size * 2)
                            hit_box_width = int(object_width * 0.25)
                            hit_box_height = int(object_height * 0.65)

                            hit_box_offset_x = int(object_width * 0.4)
                            hit_box_offset_y = int(object_height * 0.2)

                        #self.hit_box_halfpoint: int = hit_box_height / 2
                        hit_box_x: int = terrain_x + hit_box_offset_x
                        hit_box_y: int = terrain_y + hit_box_offset_y

                        if self.display_hit_box_decay <= self.terrain_data_minerals:
                            new_object: tuple[int, ...] = (hit_box_x, hit_box_y, hit_box_width, hit_box_height, object_id, hit_box_offset_x, hit_box_offset_y)
                            
                            if new_object not in self.hit_boxes: self.hit_boxes.append(new_object)
                            self.display_hit_box_decay += 1