import pygame
import random
from items import items_list
from images import ground_images, water_images


class RenderPictures:
    render_range: int = 0
    render_terrain_data: list = []
    generated_ground_images: dict = {}
    generated_water_images: dict = {}
    
    # Muudab player hitboxi asukoha õigeks, punane kast, 09.10.2023 see oli update.py line 79
    player_hitbox_offset_x = 29
    player_hitbox_offset_y = 22
    
    def map_render(self) -> None:
        self.screen.fill('white')
        RenderPictures.render_terrain_data: list = []

        RenderPictures.render_range: int = (self.screen_x + self.screen_y) // 200

        player_grid_row = int((self.player_x + RenderPictures.player_hitbox_offset_x + self.player_width / 2) // self.block_size)
        player_grid_col = int((self.player_y + RenderPictures.player_hitbox_offset_y + self.player_height / 2) // self.block_size)
        for i in range(player_grid_col - RenderPictures.render_range, player_grid_col + RenderPictures.render_range):
            self.row: list[tuple[int, int], ...] = []

            for j in range(player_grid_row - RenderPictures.render_range, player_grid_row + RenderPictures.render_range + 1):
                terrain_x: int = j * self.block_size + self.offset_x
                terrain_y: int = i * self.block_size + self.offset_y

                # Salvestab koordinaadid listi, et neid saaks hiljem kasutada object list renderis
                try: self.row.append((j, i)),
                except IndexError: pass

                # Kontrollib kas terrain block jääb faili self.terrain_data piiridesse
                if 0 <= i < len(self.terrain_data) and 0 <= j < len(self.terrain_data[i]):
                    terrain_value = self.terrain_data[i][j]

                    if terrain_value != 0 and (i, j) not in RenderPictures.generated_ground_images:
                        ground_image_name = f"Ground_{random.randint(0, 19)}"
                        RenderPictures.generated_ground_images[(i, j)] = pygame.transform.scale(ground_images.get(ground_image_name), (self.block_size, self.block_size))

                    if terrain_value == 0 and (i, j) not in RenderPictures.generated_water_images:
                        generated_water_images = f"Water_{random.randint(0, 0)}"
                        RenderPictures.generated_water_images[(i, j)] = pygame.transform.scale(water_images.get(generated_water_images), (self.block_size, self.block_size))

                    image = RenderPictures.generated_ground_images.get((i, j)) if terrain_value != 0 else RenderPictures.generated_water_images.get((i, j))
                    if image:
                        self.screen.blit(image, (terrain_x, terrain_y))
                    
                    if terrain_value == 7 or terrain_value == 107:
                        wheat_bg_image = pygame.image.load("images/Wheat_background.png")
                        self.screen.blit(wheat_bg_image, (terrain_x, terrain_y))

                    if terrain_value == 99:
                        wall = pygame.Rect(terrain_x, terrain_y, self.block_size, self.block_size)
                        pygame.draw.rect(self.screen, 'black', wall)
    
            # Teeb chunki render range laiuselt - test_list = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
            RenderPictures.render_terrain_data.append(self.row)


class CreateCollisionBoxes:
    terrain_data_minerals: int = 0
    display_collision_box_decay: int = 0

    def object_list_creation(self) -> None:
        """ Teeb objectidele hitboxid. Kasutab items.py items_list'i. """
        
        CreateCollisionBoxes.terrain_data_minerals: int = 0
        self.collision_boxes: list = []
        CreateCollisionBoxes.display_collision_box_decay: int = 0

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

        for row in RenderPictures.render_terrain_data:
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
                        collision_box_offset_x_mlp, collision_box_offset_y_mlp, collision_box_width_mlp, collision_box_height_mlp = collision_box
                        collision_box_width = int(self.block_size * collision_box_width_mlp)
                        collision_box_height = int(self.block_size * collision_box_height_mlp)

                        collision_box_offset_x = int(self.block_size * collision_box_offset_x_mlp)
                        collision_box_offset_y = int(self.block_size * collision_box_offset_y_mlp)

                        collision_box_x: int = terrain_x + collision_box_offset_x
                        collision_box_y: int = terrain_y + collision_box_offset_y

                        if CreateCollisionBoxes.display_collision_box_decay <= CreateCollisionBoxes.terrain_data_minerals:
                            new_object: tuple[int, ...] = (
                            collision_box_x, collision_box_y, collision_box_width, collision_box_height, object_id, collision_box_offset_x,
                            collision_box_offset_y)

                            if new_object not in self.collision_boxes:
                                self.collision_boxes.append(new_object)
                                CreateCollisionBoxes.terrain_data_minerals += 1
                            CreateCollisionBoxes.display_collision_box_decay += 1
            
        # Create a dictionary to map each id to its sort order
        id_sort_order = {6: 1, # First to be rendered
                        5: 2, 
                        2: 3, 
                        4: 4,
                        7: 5}  # Last to be rendered

        # Sort the collision_boxes list based on the custom sort order
        self.collision_boxes = sorted(self.collision_boxes, key=lambda box: (id_sort_order.get(box[4], float('inf')), box[1]))