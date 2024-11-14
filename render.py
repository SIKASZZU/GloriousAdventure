import pygame
import random

from camera import Camera
from items import object_items, world_items, ObjectItem, WorldItem, find_item_by_name, items_list
from images import ImageLoader
from variables import UniversalVariables, GameConfig
from tile_set import TileSet
from farmables import farming
from update import PlayerUpdate


class RenderPictures:
    render_range: int = 0
    terrain_in_view: dict = {}
    occupied_positions: dict = {}
    randomizer_x = round(random.uniform(0.1, 0.6), 1)
    randomizer_y = round(random.uniform(0.1, 0.6), 1)

    def image_to_sequence(self, terrain_x: int, terrain_y: int, position: tuple[int, int], image,
                          terrain_value) -> None:
        if image:
            occupied_positions_key = f"occupied_positions_{terrain_value}"

            if occupied_positions_key not in RenderPictures.__dict__:
                setattr(RenderPictures, occupied_positions_key, {})

            occupied_positions = getattr(RenderPictures, occupied_positions_key)

            if position not in occupied_positions:
                occupied_positions[position] = image
            else:
                scaled_saved_image = pygame.transform.scale(occupied_positions[position],
                                                            (UniversalVariables.block_size,
                                                             UniversalVariables.block_size))
                if terrain_value in [7, 107]:
                    UniversalVariables.blits_sequence_collision.append([scaled_saved_image, (terrain_x, terrain_y)])

                elif [scaled_saved_image, (terrain_x, terrain_y)] not in UniversalVariables.blits_sequence_collision:
                    UniversalVariables.blits_sequence_collision.append([scaled_saved_image, (terrain_x, terrain_y)])

    @staticmethod
    def get_render_ranges(player_grid_x, player_grid_y, camera_grid_col, camera_grid_row, terrain_type):
        # TODO: fix this

         # Determine the render range based on terrain type
        if terrain_type in GameConfig.RENDER_RANGE_SMALL.value:

            RenderPictures.render_range = 2
            base_row_range_0, base_row_range_1 = player_grid_y - RenderPictures.render_range - 1, player_grid_y + RenderPictures.render_range + 3
            base_col_range_0, base_col_range_1 = player_grid_x - RenderPictures.render_range - 2, player_grid_x + RenderPictures.render_range + 3

            if UniversalVariables.last_input in ['w', 'wa', 'wd']:
                row_range_0, row_range_1 = base_row_range_0, player_grid_y + 2
                col_range_0, col_range_1 = base_col_range_0, base_col_range_1
            elif UniversalVariables.last_input in ['s', 'sa', 'sd']:
                row_range_0, row_range_1 = player_grid_y, base_row_range_1
                col_range_0, col_range_1 = base_col_range_0, base_col_range_1
            elif UniversalVariables.last_input in ['a', 'wa', 'sa']:
                row_range_0, row_range_1 = base_row_range_0, base_row_range_1
                col_range_0, col_range_1 = base_col_range_0, player_grid_x + 2
            elif UniversalVariables.last_input in ['d', 'wd', 'sd']:
                row_range_0, row_range_1 = base_row_range_0, base_row_range_1
                col_range_0, col_range_1 = player_grid_x, base_col_range_1 + 1
            else:
                # Default to full range if no valid input
                row_range_0, row_range_1 = base_row_range_0, base_row_range_1
                col_range_0, col_range_1 = base_col_range_0, base_col_range_1

        else:

            RenderPictures.render_range = (
                                                      UniversalVariables.screen_x + UniversalVariables.screen_y) // UniversalVariables.block_size // 5
            row_range_0, row_range_1 = camera_grid_col - RenderPictures.render_range, camera_grid_col + RenderPictures.render_range + 3
            col_range_0, col_range_1 = camera_grid_row - RenderPictures.render_range - 3, camera_grid_row + RenderPictures.render_range + 6

        return row_range_0, row_range_1, col_range_0, col_range_1

    def find_terrain_in_view(self) -> None:
        RenderPictures.terrain_in_view.clear()

        camera_grid_row = int(
            (Camera.camera_rect.left + Camera.camera_rect.width / 2) // UniversalVariables.block_size) - 1
        camera_grid_col = int(
            (Camera.camera_rect.top + Camera.camera_rect.height / 2) // UniversalVariables.block_size) - 1

        player_grid_x = int(UniversalVariables.player_x // UniversalVariables.block_size)
        player_grid_y = int(UniversalVariables.player_y // UniversalVariables.block_size)

        try:
            # Determine the render range based on the player's position and terrain type
            terrain_type = self.terrain_data[player_grid_y][player_grid_x]
            row_range_0, row_range_1, col_range_0, col_range_1 = RenderPictures.get_render_ranges(player_grid_x,
                                                                                                  player_grid_y,
                                                                                                  camera_grid_col,
                                                                                                  camera_grid_row,
                                                                                                  terrain_type)

            for row in range(row_range_0, row_range_1):
                current_row = {}

                for col in range(col_range_0, col_range_1):
                    if not (0 <= row < len(self.terrain_data) and 0 <= col < len(self.terrain_data[row])):
                        continue

                    terrain_value = self.terrain_data[row][
                        col]  # see tekitab probleemi, et vaatab k6iki v22rtusi, isegi, kui object ei ole collision. Lisasin in_object_list variable, et counterida seda.

                    if terrain_value in GameConfig.GROUND_IMAGE.value and terrain_value != 1:
                        terrain_value = (1, terrain_value)

                    elif terrain_value in GameConfig.MAZE_GROUND_IMAGE.value and terrain_value != 98:
                        terrain_value = (98, terrain_value)

                    elif terrain_value in GameConfig.FARMLAND_IMAGE.value and terrain_value != 107:
                        terrain_value = (107, terrain_value)

                    else:
                        terrain_value = (terrain_value,)

                    current_row[(col, row)] = terrain_value

                RenderPictures.terrain_in_view.update(current_row)

        except IndexError:
            return

    def select_choice(self, image_name, surroundings):

        if image_name is 'Maze_Wall':
            return 'Maze_Wall_' + str(random.randint(0, 9))

        if image_name is 'Ground':
            return TileSet.determine_ground_image(self, surroundings)

        # if image_name == 'String':
        #     return TileSet.determine_string_image(self, surroundings)

        if image_name is 'Farmland':
            return TileSet.determine_farmland_image_name(self, surroundings)

        if image_name is 'Water':
            if random.random() < 0.6:
                return 'Water_0'
            else:
                return 'Water_' + str(random.randint(1, 3))

        if image_name is 'Maze_Ground':
            if random.random() < 0.65:
                return 'Maze_Ground_1'
            elif random.random() < 0.45:  # cracks
                return 'Maze_Ground_' + str(random.randint(1, 4))
            else:  # cracks + stones
                return 'Maze_Ground_' + str(random.randint(5, 9))

    # renderib k6ik objektide all, backgroundi,terraini, seinad
    def map_render(self):
        RenderPictures.find_terrain_in_view(self)

        many_choices = [0, 1, 107, 98, 99]  # objektid, millel on rohkem kui yks pilt. See list ei pruugi olla 6ige :D

        for grid_info in RenderPictures.terrain_in_view.items():

            surrounding_values = (None,)  # Valued mille järgi valib vajalikud tile-set'i pildid
            image_name = None  # reset
            grid, grid_ids = grid_info

            x, y = grid
            terrain_x = x * UniversalVariables.block_size + UniversalVariables.offset_x
            terrain_y = y * UniversalVariables.block_size + UniversalVariables.offset_y

            object_id = grid_ids[0]  # renderib esimese indexi, sest esimene index on alati alumine pilt ehk ground v6i maze wall

            if object_id == 0:  # neid itemeid ei ole item listis ehk see ei lahe allpool labi
                image_name = 'Water'

            elif object_id in GameConfig.GROUND_IMAGE.value:
                image_name = 'Ground'
                object_id = 1
                surrounding_values = (0,)

            elif object_id in GameConfig.MAZE_GROUND_IMAGE.value:
                image_name = 'Maze_Ground'
                object_id = 98

            elif object_id in GameConfig.FARMLAND_IMAGE.value:
                image_name, object_id, surrounding_values = farming(self, x, y, grid)  # See on farming failist

            ### FIXME: STRING, Tileset on broken ???
            if image_name == None:  image_name = next((item.name for item in items_list if object_id == item.id), None)
            if image_name:
                if object_id in many_choices:
                    surroundings = TileSet.check_surroundings(self, y, x, surrounding_values)
                    image_name = RenderPictures.select_choice(self, image_name,
                                                              surroundings)  # m6nel asjal on mitu varianti.

                # FIXME mdv, see see Tileset.determine ground image name returnib mingi surfaci kogu aeg...
                # insane hack
                if type(image_name) == pygame.surface.Surface:
                    RenderPictures.image_to_sequence(self, terrain_x, terrain_y, grid, image_name, object_id)
                    continue

                image = ImageLoader.load_image(image_name)
                RenderPictures.image_to_sequence(self, terrain_x, terrain_y, grid, image, object_id)

        UniversalVariables.buffer_collision.blits(UniversalVariables.blits_sequence_collision, doreturn=False)

    # See func renderib objecteid
    def object_render(self):
        if not UniversalVariables.render_after:
            PlayerUpdate.render_player(self)

        desired_order = GameConfig.OBJECT_RENDER_ORDER.value

        def sort_key(item):
            id = item[5]
            return desired_order.index(id) if id in desired_order else float('inf')

        # Filter and sort the objects
        sorted_objects = sorted(
            (item for item in UniversalVariables.object_list if item[4] is not None),
            key=sort_key
        )

        # Render the objects
        for item in sorted_objects:
            if item[
                5] in GameConfig.COLLISION_ITEMS.value:  # Skip need itemid, sest collisionis renderib kaa. SEe peab siin olema, et roosa ruut tekiks.
                continue
            position = item[:2]  # x, y
            image = item[4]

            scaled_object_image = pygame.transform.scale(image, item[2:4])  # image, sizes
            if [scaled_object_image, position] not in UniversalVariables.blits_sequence_objects:
                UniversalVariables.blits_sequence_objects.append([scaled_object_image, position])

        UniversalVariables.screen.blits(UniversalVariables.blits_sequence_objects, doreturn=False)
        if UniversalVariables.render_after:
            PlayerUpdate.render_player(self)

class ObjectCreation:
    random_offsets = {}

    def creating_lists(self):

        UniversalVariables.collision_boxes = []
        UniversalVariables.object_list = []

        collision_items = []
        non_collision_items = []
        items_not_designed_for_list = [11, 98, 99, 989_98, 988]  # maze groundid vmdgi taolist
        breakability = None

        for item_list in [object_items, world_items]:
            for item in item_list:
                object_id = item.id

                if object_id in items_not_designed_for_list:
                    continue

                object_image_name = item.name
                object_width = item.width
                object_height = item.height
                object_image = ImageLoader.load_image(object_image_name)
                breakability = item.breakable if isinstance(item, ObjectItem) else False

                a_item = (object_id, breakability, object_width, object_height, object_image)

                # item on juba yhe korra loopi l2bi teinud.
                if a_item in non_collision_items or a_item in collision_items:
                    pass

                else:
                    if a_item[0] in GameConfig.INTERACTABLE_ITEMS.value:
                        non_collision_items.append(a_item)

                    if a_item[0] in GameConfig.COLLISION_ITEMS.value:
                        collision_items.append(a_item)

        ObjectCreation.collision_box_list_creation(self, collision_items)
        ObjectCreation.object_list_creation(self, non_collision_items)

    def collision_box_list_creation(self, collision_items) -> None:
        """
            Teeb collision boxid objektidele, millel on vaja collisionit.
            Roheline ruut.
            See list on vajalik visioni tegemisel.
        """

        for item in collision_items:
            object_id, _, object_width, object_height, _, = item

            for grid, grid_ids in RenderPictures.terrain_in_view.items():

                x, y = grid
                object_id = grid_ids[
                    0]  # renderib esimese indexi, sest esimene index on alati alumine pilt ehk ground v6i maze wall
                if object_id in GameConfig.COLLISION_ITEMS.value:
                    terrain_x: int = x * UniversalVariables.block_size + UniversalVariables.offset_x
                    terrain_y: int = y * UniversalVariables.block_size + UniversalVariables.offset_y

                    new_object: tuple[int, ...] = (terrain_x, terrain_y, object_width, object_height, object_id)

                    if new_object not in UniversalVariables.collision_boxes:
                        UniversalVariables.collision_boxes.append(new_object)

    def object_list_creation(self, non_collision_items) -> None:
        for item in non_collision_items:
            object_id, _, object_width, object_height, object_image = item

            for grid, grid_ids in RenderPictures.terrain_in_view.items():
                x, y = grid
                if self.terrain_data[y][x] == object_id:  # Object is found on the rendered terrain
                    terrain_x: int = x * UniversalVariables.block_size + UniversalVariables.offset_x
                    terrain_y: int = y * UniversalVariables.block_size + UniversalVariables.offset_y

                    new_object = (terrain_x, terrain_y, object_width, object_height, object_image, object_id)

                    if new_object not in UniversalVariables.object_list:
                        # terrain_x, terrain_y, object_width, object_height, object_image, object_id
                        UniversalVariables.object_list.append(new_object)


if __name__ == '__main__':  ...