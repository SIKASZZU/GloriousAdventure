import pygame
import random

from camera import Camera
from items import items_list
from images import ImageLoader
from update import EssentialsUpdate
from variables import UniversalVariables
from tile_set import TileSet

class RenderPictures:
    render_range: int = 0
    terrain_in_view: list = []
    occupied_positions: dict = {}
    randomizer_x = round(random.uniform(0.1, 0.6) , 1)
    randomizer_y = round(random.uniform(0.1, 0.6) , 1)

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
        #TODO: fix this
        
        # Determine the render range based on terrain type
        if terrain_type in UniversalVariables.render_range_small:
            
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
                            
            RenderPictures.render_range = (UniversalVariables.screen_x + UniversalVariables.screen_y) // UniversalVariables.block_size // 5
            row_range_0, row_range_1 = camera_grid_col - RenderPictures.render_range, camera_grid_col + RenderPictures.render_range + 3
            col_range_0, col_range_1 = camera_grid_row - RenderPictures.render_range - 3, camera_grid_row + RenderPictures.render_range + 6

        return row_range_0, row_range_1, col_range_0, col_range_1

    def map_render(self) -> None:
        UniversalVariables.screen.fill('black')
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
            row_range_0, row_range_1, col_range_0, col_range_1 = RenderPictures.get_render_ranges(player_grid_x, player_grid_y, camera_grid_col, camera_grid_row, terrain_type)

            for row in range(row_range_0, row_range_1):
                current_row = []

                for col in range(col_range_0, col_range_1):
                    if not (0 <= row < len(self.terrain_data) and 0 <= col < len(self.terrain_data[row])):
                        continue

                    current_row.append((col, row))
                    terrain_value = self.terrain_data[row][col]  # see tekitab probleemi, et vaatab k6iki v22rtusi, isegi, kui object ei ole collision. Lisasin in_object_list variable, et counterida seda.
                    terrain_x = col * UniversalVariables.block_size + UniversalVariables.offset_x
                    terrain_y = row * UniversalVariables.block_size + UniversalVariables.offset_y
                    position = (col, row)
                    if terrain_value in UniversalVariables.interactable_items:  # see peks olema mingi no background needed list .. et ei renderiks topelt object ja map renderis
                        continue

                    if terrain_value is None:
                        continue

                    image = None

                    ### FIXME: maze uksed ja blade maze flickerib

                    # SEE FUNCTION BLITIB AINULT BACKGROUNDI

                    # Kui terrain data on 0 - 10
                    # Teeb Water/Ground imaged v background imaged
                    if 0 <= terrain_value <= 10 or terrain_value >= 1004:
                        if terrain_value != 0:

                            surroundings = TileSet.check_surroundings(self, row, col, 0)
                            image_name = TileSet.determine_ground_image_name(self, surroundings)

                        else:
                            if random.random() < 0.6:
                                image_name = 'Water_0'
                            else:
                                image_name = 'Water_' + str(random.randint(1, 3))

                        if type(image_name) != str:
                            image = image_name

                        if image is None:
                            image = ImageLoader.load_image(image_name)

                        # Näiteks wheat ja key alla ei pane pilti siin vaid all pool, muidu tuleks topelt
                        if terrain_value in {7, 10}:
                            image = None

                        if image:
                            if position not in RenderPictures.occupied_positions:
                                scaled_image = pygame.transform.scale(image, (UniversalVariables.block_size, UniversalVariables.block_size))

                                if [scaled_image, (terrain_x, terrain_y)] not in UniversalVariables.blits_sequence_collision:
                                    UniversalVariables.blits_sequence_collision.append([scaled_image, (terrain_x, terrain_y)])
                                RenderPictures.occupied_positions[position] = scaled_image
                            else:
                                scaled_image = RenderPictures.occupied_positions[position]
                                if [scaled_image, (terrain_x, terrain_y)] not in UniversalVariables.blits_sequence_collision:
                                    UniversalVariables.blits_sequence_collision.append([scaled_image, (terrain_x, terrain_y)])

                    # SEE FUNCTION BLITIB AINULT BACKGROUNDI
                    elif terrain_value == 98:
                        if random.random() < 0.65:
                            image_name = 'Maze_Ground'
                        elif random.random() < 0.45:  # cracks
                            image_name = 'Maze_Ground_' + str(random.randint(1, 4))
                        else: # cracks + stones
                            image_name = 'Maze_Ground_' + str(random.randint(1, 9))


                        image = ImageLoader.load_image(image_name)
                        RenderPictures.image_to_sequence(self, terrain_x, terrain_y, position, image, terrain_value)

                    elif terrain_value == 99:
                        image_name = 'Maze_Wall_' + str(random.randint(0, 9))
                        image = ImageLoader.load_image(image_name)
                        RenderPictures.image_to_sequence(self, terrain_x, terrain_y, position, image, terrain_value)

                    elif terrain_value == 107:
                        image_name = TileSet.determine_farmland_image_name(self, row, col)
                        image = ImageLoader.load_image(image_name)
                        RenderPictures.image_to_sequence(self, terrain_x, terrain_y, position, image, terrain_value)

                    elif terrain_value in {933, 977}:
                        if EssentialsUpdate.day_night_text == 'Night':
                            self.terrain_data[row][col] = 977
                            image = ImageLoader.load_image('Maze_End_Bottom')
                        else:
                            self.terrain_data[row][col] = 933

                        RenderPictures.image_to_sequence(self, terrain_x, terrain_y, position, image, terrain_value)

                    elif terrain_value == 1000:
                        image = ImageLoader.load_image('Final_Maze_Ground_2')
                        RenderPictures.image_to_sequence(self, terrain_x, terrain_y, position, image, terrain_value)

                    elif terrain_value in {1001, 1002, 1003}:
                        image = ImageLoader.load_image('Maze_Ground')
                        RenderPictures.image_to_sequence(self, terrain_x, terrain_y, position, image, terrain_value)

                    else:
                        image_name = next((item['Name'] for item in items_list if terrain_value == item['ID']),None)
                        if image_name:
                            image = ImageLoader.load_image(image_name)
                            RenderPictures.image_to_sequence(self, terrain_x, terrain_y, position, image, terrain_value)

                    # SEE FUNCTION BLITIB AINULT BACKGROUNDI

                    # See on peale else: sest kui see oleks enne siis
                    # hakkavad flickerima ja tekivad topelt pildid teistele
                    if terrain_value in {7, 107}:
                        image_name = TileSet.determine_farmland_image_name(self, row, col)
                        image = ImageLoader.load_image(image_name)
                        RenderPictures.image_to_sequence(self, terrain_x, terrain_y, position, image, terrain_value)

                    elif terrain_value in {10, 11}:
                        image = ImageLoader.load_image('Maze_Ground_Keyhole')
                        RenderPictures.image_to_sequence(self, terrain_x, terrain_y, position, image, terrain_value)

                RenderPictures.terrain_in_view.append(current_row)

            UniversalVariables.screen.blits(UniversalVariables.blits_sequence_collision, doreturn=False)

        except IndexError:
            return

    # See func renderib objecteid
    #TODO: objeckte me hetkel blitimie, mitte blitsime, 
    def object_render():
        desired_order = UniversalVariables.object_render_order

        def sort_key(item):
            item_id = item[5]
            return desired_order.index(item_id) if item_id in desired_order else float('inf')

        # Filter and sort the objects
        sorted_objects = sorted(
            (item for item in UniversalVariables.object_list if item[4] is not None),
            key=sort_key
        )

        # Render the objects
        for item in sorted_objects:
            position = item[:2]  # x, y
            scaled_object_image = pygame.transform.scale(item[4], item[2:4])  # image, sizes
            if [scaled_object_image, position] not in UniversalVariables.blits_sequence_objects:
                UniversalVariables.blits_sequence_objects.append([scaled_object_image, position])
            
        UniversalVariables.screen.blits(UniversalVariables.blits_sequence_objects, doreturn=False)

class ObjectCreation:

    def creating_lists(self):
        # print(f'\n UniversalVariables.collision_boxes len:{len(UniversalVariables.collision_boxes)} {UniversalVariables.collision_boxes}')
        # print(f'\n UniversalVariables.object_list len:{len(UniversalVariables.object_list)} {UniversalVariables.object_list}')

        UniversalVariables.collision_boxes = []
        UniversalVariables.object_list = []

        collision_items = []
        non_collision_items = []
        items_not_designed_for_list = [11, 98, 989_98, 988]  # maze groundid vmdgi taolist

        for item in items_list:
            if item.get("Type") == "Object":
                object_id = item.get("ID")
                if object_id in items_not_designed_for_list:
                    continue
                else:
                    object_image_name = item.get("Name")
                    breakability      = item.get('Breakable')
                    object_width      = item.get("Object_width")
                    object_height     = item.get("Object_height")
                    collision_box     = item.get("Collision_box")
                    object_image      = ImageLoader.load_image(object_image_name)


                if breakability == None:  breakability = False

                a_item = (object_id, breakability, collision_box, object_width, object_height, object_image)

                if collision_box != None:
                    start_corner_x, start_corner_y, end_corner_x, end_corner_y = collision_box
                    a_item = (object_id, breakability, start_corner_x, start_corner_y, end_corner_x, end_corner_y, object_width, object_height, object_image)

                # otsib itemeite collision boxe, et filtreerida neid.
                # a_item = (object_id, breakability, start_corner_x, start_corner_y, end_corner_x, end_corner_y, object_width, object_height, object_image)
                if a_item in non_collision_items or a_item in collision_items:
                    pass
                else:
                    if a_item[2] is None:  # if collision box is none, ehk tegu on interactable objektiga
                        non_collision_items.append(a_item)
                    else:
                        collision_items.append(a_item)

                        # lisa see pede box topelt, et oleks click v6imalus ja rohelist boxi ka
                        if a_item[0] in UniversalVariables.interactable_items:
                            non_collision_items.append(a_item)


        ObjectCreation.collision_box_list_creation(self, collision_items)
        ObjectCreation.object_list_creation(self, non_collision_items)


    def collision_box_list_creation(self, collision_items) -> None:
        """
            Teeb collision boxid objektidele, millel on vaja collisionit. Roheline ruut.
            See list on vajalik visioni tegemisel.
        """
        start_corner_x = 0
        start_corner_y = 0
        end_corner_x   = 0
        end_corner_y   = 0
        object_id      = 0

        object_collision_boxes: dict = {}

        for item in collision_items:
            object_id, _, start_corner_x, start_corner_y, end_corner_x, end_corner_y, _, _, _ = item
            object_collision_boxes[object_id] = [start_corner_x, start_corner_y, end_corner_x, end_corner_y]

        for row in RenderPictures.terrain_in_view:
            for x, y in row:
                if self.terrain_data[y][x] in object_collision_boxes:
                    object_id = self.terrain_data[y][x]
                    terrain_x: int = x * UniversalVariables.block_size + UniversalVariables.offset_x
                    terrain_y: int = y * UniversalVariables.block_size + UniversalVariables.offset_y

                    _, _, end_corner_width, end_corner_height = object_collision_boxes.get(object_id, [0, 0, 0, 0])
                    collision_box_width = int(UniversalVariables.block_size * end_corner_width)
                    collision_box_height = int(UniversalVariables.block_size * end_corner_height)

                    new_object: tuple[int, ...] = (terrain_x, terrain_y, collision_box_width, collision_box_height, object_id)

                    if new_object not in UniversalVariables.collision_boxes:
                        UniversalVariables.collision_boxes.append(new_object)


    def object_list_creation(self, non_collision_items) -> None:
        for item in non_collision_items:

            # see vajalik, sest hetkel on selline UniversalVariables.interactable_items abomination
            if len(item) == 6:
                object_id, _, _, object_width, object_height, object_image = item
            elif len(item) == 9:
                object_id, _, _, _, _, _, object_width, object_height, object_image = item

            for row in RenderPictures.terrain_in_view:
                for x, y in row:
                    if self.terrain_data[y][x] == object_id:  # object on leitud kuvatult terrainilt
                        terrain_x: int = x * UniversalVariables.block_size + UniversalVariables.offset_x
                        terrain_y: int = y * UniversalVariables.block_size + UniversalVariables.offset_y

                        new_object = (terrain_x, terrain_y, object_width, object_height, object_image, object_id)
                        random_placement = [10, 1001, 1002, 1003]
                        
                        if new_object[5] in random_placement:
                            position = (terrain_x + UniversalVariables.block_size * RenderPictures.randomizer_x, terrain_y + UniversalVariables.block_size * RenderPictures.randomizer_y)
                            new_object = (position[0], position[1], object_width, object_height, object_image, object_id)

                        if new_object not in UniversalVariables.object_list:
                            # terrain_x, terrain_y, object_width, object_height, object_image, object_id
                            UniversalVariables.object_list.append(
                                (new_object[0], new_object[1], new_object[2], new_object[3], new_object[4], new_object[5])
                                )


if __name__ == '__main__':  ...