import pygame
import random

from items import items_list
from variables import UniversalVariables
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
        UniversalVariables.screen.fill('white')
        RenderPictures.render_terrain_data: list = []

        RenderPictures.render_range: int = (UniversalVariables.screen_x + UniversalVariables.screen_y) // 200

        player_grid_row = int((UniversalVariables.player_x + RenderPictures.player_hitbox_offset_x + UniversalVariables.player_width / 2) // UniversalVariables.block_size)
        player_grid_col = int((UniversalVariables.player_y + RenderPictures.player_hitbox_offset_y + UniversalVariables.player_height / 2) // UniversalVariables.block_size)
        for i in range(player_grid_col - RenderPictures.render_range, player_grid_col + RenderPictures.render_range):
            self.row: list[tuple[int, int], ...] = []

            for j in range(player_grid_row - RenderPictures.render_range, player_grid_row + RenderPictures.render_range + 1):
                terrain_x: int = j * UniversalVariables.block_size + UniversalVariables.offset_x
                terrain_y: int = i * UniversalVariables.block_size + UniversalVariables.offset_y

                # Salvestab koordinaadid listi, et neid saaks hiljem kasutada object list renderis
                try: self.row.append((j, i)),
                except IndexError: pass

                # Kontrollib kas terrain block jääb faili UniversalVariables.terrain_data piiridesse
                if 0 <= i < len(UniversalVariables.terrain_data) and 0 <= j < len(UniversalVariables.terrain_data[i]):
                    terrain_value = UniversalVariables.terrain_data[i][j]

                    if terrain_value != 0 and (i, j) not in RenderPictures.generated_ground_images:
                        ground_image_name = f"Ground_{random.randint(0, 19)}"
                        RenderPictures.generated_ground_images[(i, j)] = pygame.transform.scale(ground_images.get(ground_image_name), (UniversalVariables.block_size, UniversalVariables.block_size))

                    if terrain_value == 0 and (i, j) not in RenderPictures.generated_water_images:
                        generated_water_images = f"Water_{random.randint(0, 0)}"
                        RenderPictures.generated_water_images[(i, j)] = pygame.transform.scale(water_images.get(generated_water_images), (UniversalVariables.block_size, UniversalVariables.block_size))

                    image = RenderPictures.generated_ground_images.get((i, j)) if terrain_value != 0 else RenderPictures.generated_water_images.get((i, j))
                    if image:
                        UniversalVariables.screen.blit(image, (terrain_x, terrain_y))
                    
                    if terrain_value == 7 or terrain_value == 107:  # Wheat ja Wheati background
                        wheat_bg_image = pygame.image.load("images/Wheat_background.png")
                        UniversalVariables.screen.blit(wheat_bg_image, (terrain_x, terrain_y))

                    if terrain_value == 99:  # mazei sein
                        wall = pygame.Rect(terrain_x, terrain_y, UniversalVariables.block_size, UniversalVariables.block_size)
                        pygame.draw.rect(UniversalVariables.screen, '#212529', wall)
                        #pygame.draw.rect(UniversalVariables.screen, '#343a40', wall)
                    
                    if terrain_value == 98:  # mazei p6rand 
                        floor = pygame.Rect(terrain_x, terrain_y, UniversalVariables.block_size, UniversalVariables.block_size)
                        pygame.draw.rect(UniversalVariables.screen, '#6c757d', floor)
    
            # Teeb chunki render range laiuselt - test_list = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
            RenderPictures.render_terrain_data.append(self.row)


class CreateCollisionBoxes:
    terrain_data_minerals: int = 0
    display_collision_box_decay: int = 0

    def object_list_creation(self) -> None:
        """ Teeb objectidele hitboxid. Kasutab items.py items_list'i. """
        
        CreateCollisionBoxes.terrain_data_minerals: int = 0
        UniversalVariables.collision_boxes: list = []
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
                if 0 <= y < len(UniversalVariables.terrain_data) and 0 <= x < len(UniversalVariables.terrain_data[0]):
                    try:
                        # Vaatab kas itemi ID on dict'is:    object_collision_boxes = {}
                        if UniversalVariables.terrain_data[y][x] in object_collision_boxes:
                            terrain_x: int = x * UniversalVariables.block_size
                            terrain_y: int = y * UniversalVariables.block_size
                            object_id: int = UniversalVariables.terrain_data[y][x]

                            # Võtab õige itemi collision_box'i
                            collision_box = object_collision_boxes.get(object_id, [0, 0, 0, 0])

                            # Arvutab hitboxi suuruse ja asukoha vastavalt camera / player / render offsetile
                            collision_box_offset_x_mlp, collision_box_offset_y_mlp, collision_box_width_mlp, collision_box_height_mlp = collision_box
                            collision_box_width = int(UniversalVariables.block_size * collision_box_width_mlp)
                            collision_box_height = int(UniversalVariables.block_size * collision_box_height_mlp)

                            collision_box_offset_x = int(UniversalVariables.block_size * collision_box_offset_x_mlp)
                            collision_box_offset_y = int(UniversalVariables.block_size * collision_box_offset_y_mlp)

                            collision_box_x: int = terrain_x + collision_box_offset_x
                            collision_box_y: int = terrain_y + collision_box_offset_y

                            if CreateCollisionBoxes.display_collision_box_decay <= CreateCollisionBoxes.terrain_data_minerals:
                                new_object: tuple[int, ...] = (
                                collision_box_x, collision_box_y, collision_box_width, collision_box_height, object_id, collision_box_offset_x,
                                collision_box_offset_y)

                                if new_object not in UniversalVariables.collision_boxes:
                                    UniversalVariables.collision_boxes.append(new_object)
                                    CreateCollisionBoxes.terrain_data_minerals += 1
                                CreateCollisionBoxes.display_collision_box_decay += 1
                    except Exception as e: print(f'Error: {e}, render.py @ if UniversalVariables.terrain_data[y][x] in object_collision_boxes:')
        # Create a dictionary to map each id to its sort order
        id_sort_order = {6: 1, # First to be rendered
                        5: 2, 
                        2: 3, 
                        4: 4,
                        7: 5}  # Last to be rendered

        # Sort the collision_boxes list based on the custom sort order
        UniversalVariables.collision_boxes = sorted(UniversalVariables.collision_boxes, key=lambda box: (id_sort_order.get(box[4], float('inf')), box[1]))