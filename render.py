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
    terrain_in_view: dict = {}
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
        
        # # Determine the render range based on terrain type
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


    def find_terrain_in_view(self) -> None:
        RenderPictures.terrain_in_view.clear()
        UniversalVariables.screen.fill('black')

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
                current_row = {}

                for col in range(col_range_0, col_range_1):
                    if not (0 <= row < len(self.terrain_data) and 0 <= col < len(self.terrain_data[row])):
                        continue

                    terrain_value = self.terrain_data[row][col]  # see tekitab probleemi, et vaatab k6iki v22rtusi, isegi, kui object ei ole collision. Lisasin in_object_list variable, et counterida seda.
                    current_row[(col, row)] = terrain_value

                RenderPictures.terrain_in_view.update(current_row)

        except IndexError:
            return


    def select_choice(image_name):

        if image_name == 'Maze_Wall':  
            return 'Maze_Wall_' + str(random.randint(0, 9))
        
        # FIXME water ja groundi ei ole, sest item listis ei ole neid itemeid >:D idk.
        if image_name == 'Water':
            if random.random() < 0.6:
                return 'Water_0'
            else:
                return 'Water_' + str(random.randint(1, 3))
                
        if image_name == 'Maze_Ground':
            if random.random() < 0.65:
                return 'Maze_Ground_1'
            elif random.random() < 0.45:  # cracks
                return 'Maze_Ground_' + str(random.randint(1, 4))
            else: # cracks + stones
                return 'Maze_Ground_' + str(random.randint(5, 9))


    # renderib k6ik objektide all, backgroundi,terraini, seinad
    def map_render(self):
        RenderPictures.find_terrain_in_view(self)
        
        many_choices = [98,99,1,0]  # objektid, millel on rohkem kui yks pilt. See list ei pruugi olla 6ige :D
        
        for grid_info in RenderPictures.terrain_in_view.items():
            image_name = None  # reset
            grid, object_id = grid_info
            x,y = grid
            terrain_x = x * UniversalVariables.block_size + UniversalVariables.offset_x
            terrain_y = y * UniversalVariables.block_size + UniversalVariables.offset_y
            
            
            if object_id in UniversalVariables.interactable_items:  # see funk suudab objekte ka renderida, ehk ss see if statement removib objektid 2ra.
                continue
            
            if object_id in [1, 0]:  # neid itemeid ei ole item listis ehk see ei lahe allpool labi
                if object_id == 1:
                    image_name = 'Ground_'
                    
                else:
                    if random.random() < 0.6:  image_name = 'Water_0'
                    else: image_name = 'Water_' + str(random.randint(1, 3))
                        
            if image_name == None:  image_name = next((item['Name'] for item in items_list if object_id == item['ID']), None)
            if image_name:
                
                if object_id in many_choices: image_name = RenderPictures.select_choice(image_name)  # m6nel asjal on mitu varianti.
                image = ImageLoader.load_image(image_name)
                RenderPictures.image_to_sequence(self, terrain_x, terrain_y, grid, image, object_id)
                
        UniversalVariables.screen.blits(UniversalVariables.blits_sequence_collision, doreturn=False)


    # See func renderib objecteid
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
    random_offsets = {}
    
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

        for grid, object_id in RenderPictures.terrain_in_view.items():
            x,y = grid
            if object_id in object_collision_boxes:
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

            for grid, _  in RenderPictures.terrain_in_view.items():
                x,y = grid
                if self.terrain_data[y][x] == object_id:  # Object is found on the rendered terrain
                    terrain_x: int = x * UniversalVariables.block_size + UniversalVariables.offset_x
                    terrain_y: int = y * UniversalVariables.block_size + UniversalVariables.offset_y

                    if object_id in UniversalVariables.random_placement:
                        position_key = (x, y)  # save object grid. koordinaadiga oleks perses.

                        # Check if the random offset for this position already exists
                        if position_key not in ObjectCreation.random_offsets:
                            # Generate and store the random offsets
                            randomizer_x = round(random.uniform(0.1, 0.6), 1)
                            randomizer_y = round(random.uniform(0.1, 0.6), 1)
                            ObjectCreation.random_offsets[position_key] = (randomizer_x, randomizer_y)
                        else:
                            # Retrieve the stored random offsets
                            randomizer_x, randomizer_y = ObjectCreation.random_offsets[position_key]

                        # Apply the random offset to the object's position
                        position = (terrain_x + UniversalVariables.block_size * randomizer_x,
                                    terrain_y + UniversalVariables.block_size * randomizer_y)
                        new_object = (position[0], position[1], object_width, object_height, object_image, object_id)
                    else:
                        new_object = (terrain_x, terrain_y, object_width, object_height, object_image, object_id)

                    if new_object not in UniversalVariables.object_list:
                        # terrain_x, terrain_y, object_width, object_height, object_image, object_id
                        UniversalVariables.object_list.append(new_object)
if __name__ == '__main__':  ...