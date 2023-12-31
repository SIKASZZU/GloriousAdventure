import pygame
import random

from items import items_list
from variables import UniversalVariables
from images import ImageLoader
from camera import Camera
import time


class RenderPictures:
    render_range: int = 0
    render_terrain_data: list = []
    occupied_positions: dict = {}
    generated_ground_images: dict = {}
    generated_water_images: dict = {}

    @staticmethod
    def map_render(self) -> None:
        UniversalVariables.screen.fill('white')
        RenderPictures.render_terrain_data: list = []

        RenderPictures.render_range: int = (UniversalVariables.screen_x + UniversalVariables.screen_y) // (
                UniversalVariables.block_size) // 6

        # TODO: See tuleb ära muuta !! - - - - Window size muutes läheb renderimine perse  -- - - - Size Ratio
        # Use the camera's position to determine the render range
        camera_grid_row = int((Camera.camera_rect.left + Camera.camera_rect.width / 2) // UniversalVariables.block_size) - 4
        camera_grid_col = int((Camera.camera_rect.top + Camera.camera_rect.height / 2) // UniversalVariables.block_size) - 1

        for i in range(camera_grid_col - RenderPictures.render_range, camera_grid_col + RenderPictures.render_range + 3):
            self.row: list[tuple[int, int], ...] = []

            for j in range(camera_grid_row - RenderPictures.render_range, camera_grid_row + RenderPictures.render_range + 9):
                terrain_x: int = j * UniversalVariables.block_size + UniversalVariables.offset_x
                terrain_y: int = i * UniversalVariables.block_size + UniversalVariables.offset_y

                # Salvestab koordinaadid listi, et neid saaks hiljem kasutada object list renderis
                try:
                    self.row.append((j, i)),
                except IndexError:
                    pass

                # Kontrollib kas terrain block jääb faili UniversalVariables.terrain_data piiridesse
                if 0 <= i < len(UniversalVariables.terrain_data) and 0 <= j < len(UniversalVariables.terrain_data[i]):
                    terrain_value = UniversalVariables.terrain_data[i][j]

                    image_name = "Ground_" + str(random.randint(0, 19)) if terrain_value != 0 else "Water_0"
                    image = ImageLoader.load_image(image_name)

                    # Loadib Wheat'i ja Farmland'i
                    if terrain_value == 7 or terrain_value == 107:
                        image = ImageLoader.load_image("Farmland")

                    # Visualiseerib pilte
                    if image:
                        if terrain_value == 98 or terrain_value == 99:
                            pass
                        else:
                            terrain_x = (j * UniversalVariables.block_size) + UniversalVariables.offset_x
                            terrain_y = (i * UniversalVariables.block_size) + UniversalVariables.offset_y
                            position = (i, j)  # Using grid indices directly for the position

                            if position not in RenderPictures.occupied_positions:

                                scaled_image = pygame.transform.scale\
                                        (
                                        image, (UniversalVariables.block_size, UniversalVariables.block_size)
                                    )

                                UniversalVariables.screen.blit(scaled_image,(terrain_x, terrain_y))
                                RenderPictures.occupied_positions[position] = scaled_image
                            else:
                                saved_image = RenderPictures.occupied_positions[position]
                                scaled_saved_image = pygame.transform.scale\
                                        (
                                        saved_image, (UniversalVariables.block_size, UniversalVariables.block_size)
                                    )

                                UniversalVariables.screen.blit(scaled_saved_image,(terrain_x, terrain_y))

            RenderPictures.render_terrain_data.append(self.row)


class CreateCollisionBoxes:
    terrain_data_minerals: int = 0
    display_collision_box_decay: int = 0

    def __init__(self):
        self.terrain_data_minerals = 0
        self.display_collision_box_decay = 0

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
                                    collision_box_x, collision_box_y, collision_box_width, collision_box_height,
                                    object_id, collision_box_offset_x,
                                    collision_box_offset_y)

                                if new_object not in UniversalVariables.collision_boxes:
                                    UniversalVariables.collision_boxes.append(new_object)
                                    CreateCollisionBoxes.terrain_data_minerals += 1
                                CreateCollisionBoxes.display_collision_box_decay += 1
                    except Exception as e:
                        print(
                            f'Error: {e}, render.py @ if UniversalVariables.terrain_data[y][x] in object_collision_boxes:')

        # Teatud järjekorras laeb objektid sisse, et kivid oleksid ikka puude all jne.
        id_sort_order = {6: 1,  # First to be rendered
                         5: 2,
                         2: 3,
                         4: 4,
                         7: 5}  # Last to be rendered

        # Sort the collision_boxes list based on the custom sort order
        UniversalVariables.collision_boxes = sorted(UniversalVariables.collision_boxes,
                                                    key=lambda box: (id_sort_order.get(box[4], float('inf')), box[1]))