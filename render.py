import pygame
from map_generator import map_data_generator
import random
from images import ground_images, water_images, item_images
from objects import place_and_render_hitbox, place_and_render_object
import collisions


class Render_Checker:
    display_hit_box_decay: int = 0
    index: int = 0

    def map_render(self) -> None:
        self.screen.fill('white')
        self.render_terrain_data: list = []

        # Renderiks kogu maailma ära ja siis muutub else statementis olevaks intager'iks
        if self.index < 10:
            self.render_range: int = 70  # Muudab renerimise suurust
            self.index += 1
        else:
            self.render_range: int = 8

        player_grid_row = int(self.player_x // self.block_size)
        player_grid_col = int(self.player_y // self.block_size)

        for i in range(player_grid_col - self.render_range, player_grid_col + self.render_range + 1):
            self.row: list[int, ...] = []
            for j in range(player_grid_row - self.render_range, player_grid_row + self.render_range + 1):
                terrain_x: int = j * self.block_size + self.offset_x
                terrain_y: int = i * self.block_size + self.offset_y

                try:
                    self.row.append(self.terrain_data[i][j])
                except IndexError as e:
                    pass

                # Kontrollib kas terrain block jääb faili self.terrain_data piiridesse
                if 0 <= i < len(self.terrain_data) and 0 <= j < len(self.terrain_data[i]):

                    # Vaatab kas terrain data on 1
                    if self.terrain_data[i][j] != 0:
                        # Vaatab kas ground pilt on juba olemas
                        if (i, j) not in self.generated_ground_images:
                            ground_image_name: str = f"Ground_{random.randint(0, 19)}"
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
                            generated_water_images: str = f"Water_{random.randint(0, 0)}"
                            water_image = water_images.get(generated_water_images)
                            self.generated_water_images[(i, j)] = water_image

                        # Renderib water pidid kui need eksisteerivad
                        water_image = self.generated_water_images.get((i, j))
                        if water_image:
                            water_image = pygame.transform.scale(water_image, (self.block_size, self.block_size))
                            self.screen.blit(water_image, (terrain_x, terrain_y))

            # Teeb chunki render range laiuselt - test_list = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
            self.render_terrain_data.append(self.row)


    def object_render(self) -> None:
        player_grid_row: int = int(self.player_x // self.block_size)
        player_grid_col: int = int(self.player_y // self.block_size)

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

                        object_image = None
                        object_width: int = 0
                        object_height: int = 0
                        hit_box_width: int = 0
                        hit_box_height: int = 0
                        hit_box_offset_x: int = 0
                        hit_box_offset_y: int = 0

                        if object_id == 4: self.terrain_data_minerals += 1

                        if object_id == 2:
                            object_image = item_images.get("Rock")
                            object_width = int(self.block_size * 1)
                            object_height = int(self.block_size * 0.8)
                            hit_box_width = int(object_width * 0.5)
                            hit_box_height = int(object_height * 0.5)
                            hit_box_offset_x = int(object_width * 0.3)
                            hit_box_offset_y = int(object_height * 0.25)

                        elif object_id == 4:
                            object_image = item_images.get("Tree")
                            hit_box_color = 'green'

                            # Pane TOP-LEFT otsa järgi paika
                            # ja siis muuda - palju lihtsam
                            object_width = int(self.block_size * 2)
                            object_height = int(self.block_size * 2)
                            hit_box_width = int(object_width * 0.25)
                            hit_box_height = int(object_height * 0.65)

                            hit_box_offset_x = int(object_width * 0.4)
                            hit_box_offset_y = int(object_height * 0.2)

                        hit_box_x: int = terrain_x + hit_box_offset_x
                        hit_box_y: int = terrain_y + hit_box_offset_y

                        if object_id > 1:
                            if self.display_hit_box_decay <= self.terrain_data_minerals:
                                new_item: tuple[int, ...] = (hit_box_x, hit_box_y,
                                                             hit_box_width, hit_box_height,
                                                             object_id,
                                                             hit_box_offset_x, hit_box_offset_y)

                                if new_item not in self.hit_boxes:
                                    self.hit_boxes.append(new_item)

                                self.display_hit_box_decay += 1


                            place_and_render_object(self,
                                                    object_id, object_image,
                                                    terrain_x, terrain_y,
                                                    object_width, object_height
                                                    )

                            place_and_render_hitbox(self,
                                                    object_id,
                                                    hit_box_x, hit_box_y,
                                                    hit_box_width, hit_box_height
                                                    )
