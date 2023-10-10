import pygame
import random
from items import items_list
import items
from images import ground_images, water_images, item_images
from objects import Object_Management # place_and_render_hitbox, place_and_render_object


class Render_Checker:
    def map_render(self) -> None:
        self.screen.fill('white')
        self.render_terrain_data: list = []

        self.render_range: int = (self.screen_x + self.screen_y) // 200

        player_grid_row = int((self.player_x + self.player_hitbox_offset_x + self.player_width / 2) // self.block_size)
        player_grid_col = int((self.player_y + self.player_hitbox_offset_y + self.player_height / 2) // self.block_size)
        for i in range(player_grid_col - self.render_range, player_grid_col + self.render_range):
            self.row: list[tuple[int, int], ...] = []

            for j in range(player_grid_row - self.render_range, player_grid_row + self.render_range + 1):
                terrain_x: int = j * self.block_size + self.offset_x
                terrain_y: int = i * self.block_size + self.offset_y

                # Salvestab koordinaadid listi, et neid saaks hiljem kasutada object list renderis
                try: self.row.append((j, i)),
                except IndexError: pass

                # Kontrollib kas terrain block jääb faili self.terrain_data piiridesse
                if 0 <= i < len(self.terrain_data) and 0 <= j < len(self.terrain_data[i]):
                    terrain_value = self.terrain_data[i][j]

                    if terrain_value != 0 and (i, j) not in self.generated_ground_images:
                        ground_image_name = f"Ground_{random.randint(0, 19)}"
                        self.generated_ground_images[(i, j)] = pygame.transform.scale(ground_images.get(ground_image_name), (self.block_size, self.block_size))

                    ####### Siin on koodi kordus, water images.

                    if terrain_value == 0 and (i, j) not in self.generated_water_images:
                        generated_water_images = f"Water_{random.randint(0, 0)}"
                        self.generated_water_images[(i, j)] = pygame.transform.scale(water_images.get(generated_water_images), (self.block_size, self.block_size))

                    image = self.generated_ground_images.get((i, j)) if terrain_value != 0 else self.generated_water_images.get((i, j))
                    if image:
                        self.screen.blit(image, (terrain_x, terrain_y))

                ####### Siin on koodi kordus, water images.
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
        """Teeb objectidele hitboxid. Kasutab items.py items_list'i"""
        self.terrain_data_minerals: int = 0
        self.hit_boxes: list = []
        self.display_hit_box_decay: int = 0

        # Teeb listi mis hoiab itemi ID'd ja Collision_box'i
        object_collision_boxes = {}
        # object_collision_boxes = {
                                # 4: [0.85, 0.85, 0.35, 0.7],
                                # 2: [0.3, 0.25, 0.5, 0.4],
                                # 5: [0, 0, 0, 0],
                                # 6: [0, 0, 0, 0]
                                # }

        # Lisab listi ID, collision_box'i
        for item in items_list:
            if item.get("Type") == "Object":
                id = item.get("ID")
                collision_box = item.get("Collision_box", [0, 0, 0, 0])
                object_collision_boxes[id] = collision_box

        for row in self.render_terrain_data:
            for x, y in row:
                if 0 <= y < len(self.terrain_data) and 0 <= x < len(self.terrain_data[0]):

                    # Vaatab kas itemi ID on dict'is:    object_collision_boxes = {}
                    if self.terrain_data[y][x] in object_collision_boxes:
                        terrain_x: int = x * self.block_size
                        terrain_y: int = y * self.block_size
                        object_id: int = self.terrain_data[y][x]

                        # Võtab õige itemi collision_box'i
                        collision_box = object_collision_boxes.get(object_id, [0, 0, 0, 0])

                        # Arvutab hitboxi suuruse ja asukoha vastavalt camera / player / render offsetile
                        hit_box_offset_x_mlp, hit_box_offset_y_mlp, hit_box_width_mlp, hit_box_height_mlp = collision_box
                        hit_box_width = int(self.block_size * hit_box_width_mlp)
                        hit_box_height = int(self.block_size * hit_box_height_mlp)

                        hit_box_offset_x = int(self.block_size * hit_box_offset_x_mlp)
                        hit_box_offset_y = int(self.block_size * hit_box_offset_y_mlp)

                        hit_box_x: int = terrain_x + hit_box_offset_x
                        hit_box_y: int = terrain_y + hit_box_offset_y

                        if self.display_hit_box_decay <= self.terrain_data_minerals:
                            new_object: tuple[int, ...] = (
                            hit_box_x, hit_box_y, hit_box_width, hit_box_height, object_id, hit_box_offset_x,
                            hit_box_offset_y)

                            if new_object not in self.hit_boxes:
                                self.hit_boxes.append(new_object)
                                self.terrain_data_minerals += 1
                            self.display_hit_box_decay += 1

        self.hit_boxes = sorted(self.hit_boxes, key=lambda box: box[1])  # sorteerib listi ära, Y väärtus kõige viimane