import pygame
import random

from camera import Camera
from items import items_list
from images import ImageLoader
from update import EssentialsUpdate
from variables import UniversalVariables

class RenderPictures:
    render_range: int = 0
    terrain_in_view: list = []
    occupied_positions: dict = {}
    generated_ground_images: dict = {}
    generated_water_images: dict = {}

    def render(self):
        RenderPictures.map_render(self)
        RenderPictures.object_render(self)


    def image_to_sequence(self, terrain_x: int, terrain_y: int, position: tuple[int, int], image,
                          terrain_value) -> None:
        """
        Teisendab pildi jadaks, kui esemel on mitu erinevat pilti, ja jaotab need positsioonide vahel laiali.

        Args:
            terrain_x (int): Grid X * block size + offset.
            terrain_y (int): Grid Y * block size + offset.
            position (tuple[int, int]): (Grid X, Grid Y).
            image: Pilt, mida töödeldakse.
            terrain_value: Väärtus, mis määrab maastiku tüübi.

        Returns:
            None
        """

        if image:
            current_entry = [image, (terrain_x, terrain_y)]

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

                if [scaled_saved_image, (terrain_x, terrain_y)] not in UniversalVariables.blits_sequence:
                    UniversalVariables.blits_sequence.append([scaled_saved_image, (terrain_x, terrain_y)])


    def map_render(self) -> None:
        #  NOTE:
        #    COL == J == X
        #    ROW == I == Y
        #    M6tle koordinaatteljestikule. Kui X muutub, muutub column. Kui muutub Y, siis muutub row.

        UniversalVariables.screen.fill('white')
        RenderPictures.render_terrain_data: list = []

        # Use the camera's position to determine the render range
        camera_grid_row = int((Camera.camera_rect.left + Camera.camera_rect.width / 2) // UniversalVariables.block_size) - 1
        camera_grid_col = int((Camera.camera_rect.top + Camera.camera_rect.height / 2) // UniversalVariables.block_size) - 1

        player_grid_x = int(UniversalVariables.player_x // UniversalVariables.block_size)
        player_grid_y = int(UniversalVariables.player_y // UniversalVariables.block_size)

        try:
            if self.terrain_data[player_grid_y][player_grid_x] in UniversalVariables.render_range_small:
                RenderPictures.render_range = 2
                row_range_0, row_range_1 = player_grid_y - RenderPictures.render_range - 2, player_grid_y + RenderPictures.render_range + 4
                col_range_0, col_range_1 = player_grid_x - RenderPictures.render_range - 3, player_grid_x + RenderPictures.render_range + 4
            else:
                RenderPictures.render_range: int = (UniversalVariables.screen_x + UniversalVariables.screen_y) // (UniversalVariables.block_size) // 5
                row_range_0, row_range_1 = camera_grid_col - RenderPictures.render_range, camera_grid_col + RenderPictures.render_range + 3
                col_range_0, col_range_1 = camera_grid_row - RenderPictures.render_range - 3, camera_grid_row + RenderPictures.render_range + 6

            for row in range(row_range_0, row_range_1):
                self.row: list[tuple[int, int], ...] = []

                for col in range(col_range_0, col_range_1):
                    # Kontrollib kas terrain block jääb faili terrain_data piiridesse
                    if 0 <= row < len(self.terrain_data) and 0 <= col < len(self.terrain_data[row]):
                        self.row.append((col, row))  # Salvestab koordinaadid listi, et neid saaks hiljem kasutada object list renderis
                        terrain_value = self.terrain_data[row][col]
                        terrain_x: int = col * UniversalVariables.block_size + UniversalVariables.offset_x
                        terrain_y: int = row * UniversalVariables.block_size + UniversalVariables.offset_y
                        position = (col, row)  # Using grid indices directly for the position
                        
                        if terrain_value == None: pass
                        else:
                            image = None
                            
                            # BACKGROUNDI LISAMINE KUHU VAJA
                            if 0 <= terrain_value <= 10:
                                if terrain_value == 7:  
                                    image = ImageLoader.load_image('Farmland')
                                    RenderPictures.image_to_sequence(self,terrain_x, terrain_y, position,image, terrain_value)
                                elif terrain_value == 10:  
                                    image = ImageLoader.load_image('Maze_Ground_Keyhole')
                                    RenderPictures.image_to_sequence(self,terrain_x, terrain_y, position,image, terrain_value)
                                else:
                                    image_name = 'Ground_' + str(random.randint(0, 19)) if terrain_value != 0 else 'Water_0'
                                    image = ImageLoader.load_image(image_name)

                                    # Ground pildile eraldi render, et see asi ei muutuks objekti eemaldamisel
                                    if position not in RenderPictures.occupied_positions:

                                        scaled_image = pygame.transform.scale(image, (UniversalVariables.block_size, UniversalVariables.block_size))
                                        if [scaled_image,(terrain_x, terrain_y)] not in UniversalVariables.blits_sequence:
                                            UniversalVariables.blits_sequence.append([scaled_image,(terrain_x, terrain_y)])

                                        RenderPictures.occupied_positions[position] = scaled_image
                                    else:
                                        scaled_image = RenderPictures.occupied_positions[position]
                                        scaled_saved_image = pygame.transform.scale(scaled_image, (UniversalVariables.block_size, UniversalVariables.block_size))

                                        if [scaled_image,(terrain_x, terrain_y)] not in UniversalVariables.blits_sequence:
                                            UniversalVariables.blits_sequence.append([scaled_saved_image,(terrain_x, terrain_y)])


                            elif terrain_value in UniversalVariables.door_ids:  
                                image = ImageLoader.load_image('Maze_Ground')  # MAZE GROUND BACKGROUNDI LISAMINE
                                RenderPictures.image_to_sequence(self,terrain_x, terrain_y, position,image, terrain_value)
                            
                            elif terrain_value == 1000:  
                                image = ImageLoader.load_image('Final_Maze_Ground_2')  # MAZE GROUND BACKGROUNDI LISAMINE
                                RenderPictures.image_to_sequence(self,terrain_x, terrain_y, position,image, terrain_value)

                            elif terrain_value == 933 or terrain_value == 977:
                                if EssentialsUpdate.day_night_text == 'Night': self.terrain_data[position[1]][position[0]] = 977
                                else: self.terrain_data[position[1]][position[0]] = 933
                                
                                # 933, 977 pole door_ids listis, sest mudu broken door/night open/close thing.
                                image = ImageLoader.load_image('Maze_Ground')  # MAZE GROUND BACKGROUNDI LISAMINE
                                RenderPictures.image_to_sequence(self,terrain_x, terrain_y, position,image, terrain_value)

                            # Spawnib maze ground, wall ja vist veel asju, mdea.
                            else:
                                for item in items_list:
                                    if terrain_value == item.get('ID'):
                                        image_name = item.get('Name')
                                     
                                # special case, sest walle on meil 9 erinevat tykki.
                                if image_name.startswith('Maze_Wall'): image_name = 'Maze_Wall_' + str(random.randint(0,9))
                    
                                image = ImageLoader.load_image(image_name)
                                RenderPictures.image_to_sequence(self, terrain_x, terrain_y, position,image, terrain_value)            

                RenderPictures.terrain_in_view.append(self.row)
            UniversalVariables.screen.blits(UniversalVariables.blits_sequence, doreturn=False)

        except IndexError:
            return


    def object_render(self):
        # render the bitch
        for item in UniversalVariables.object_list:
            position: tuple = (item[1], item[2])
            scaled_object_image = pygame.transform.scale(item[5], (item[3], item[4]))
            UniversalVariables.screen.blit(scaled_object_image, position)


class ObjectCreation:

    def creating_lists(self):
        UniversalVariables.collision_boxes = []
        UniversalVariables.object_list = []
        
        
        collision_item = []
        non_collision_item = []
        objects_in_view = set()

        # Lisab listi ID, collision_box'i
        for in_view_grid in RenderPictures.terrain_in_view:
            for x, y in in_view_grid:
                objects_in_view.add(self.terrain_data[y][x])

        for item in items_list:
            if item.get("Type") == "Object":
                object_id = item.get("ID")
                if object_id in objects_in_view:
                    #print(object_id)

                    object_image_name = item.get("Name")
                    object_image      = ImageLoader.load_image(object_image_name)
                    breakability      = item.get('Breakable')
                    object_width      =  item.get("Object_width")
                    object_height     = item.get("Object_height")
                    collision_box     = item.get("Collision_box")


                    if breakability == None:  breakability = False
                    
                    a_item = (object_id, breakability, collision_box, object_width, object_height, object_image)
                    if object_image:
                            
                        if collision_box != None:  
                            start_corner_x, start_corner_y, end_corner_x, end_corner_y = collision_box
                            a_item = (object_id, breakability, start_corner_x, start_corner_y, end_corner_x, end_corner_y, object_width, object_height, object_image)

                        # otsib itemeite collision boxe, et filtreerida neid.
                        if a_item[2] is None:  non_collision_item.append(a_item)
                        else:                  collision_item.append(a_item)
        
        ObjectCreation.collision_box_list_creation(self, collision_item)
        ObjectCreation.object_list_creation(self, non_collision_item)


    def collision_box_list_creation(self, collision_item) -> None:
        """ 
            Teeb collision boxid objektidele, millel on vaja collisionit. Roheline ruut. 
            See list on vajalik visioni tegemisel.
        """
        start_corner_x = 0
        start_corner_y = 0
        end_corner_x   = 0
        end_corner_y   = 0
        object_id      = 0

        for item in collision_item:
            object_id, breakability, start_corner_x, start_corner_y, \
                end_corner_x, end_corner_y, object_width, object_height, object_image = item 
        
        object_collision_boxes: dict = {}

        object_collision_boxes[object_id] = [start_corner_x, start_corner_y, end_corner_x, end_corner_y]

        for row in RenderPictures.terrain_in_view:
            for x, y in row:
                if self.terrain_data[y][x] in object_collision_boxes:
                    terrain_x: int = x * UniversalVariables.block_size + UniversalVariables.offset_x
                    terrain_y: int = y * UniversalVariables.block_size + UniversalVariables.offset_y

                    _, _, end_corner_width, end_corner_height = object_collision_boxes.get(object_id, [0, 0, 0, 0])
                    collision_box_width = int(UniversalVariables.block_size * end_corner_width)
                    collision_box_height = int(UniversalVariables.block_size * end_corner_height)

                    new_object: tuple[int, ...] = (terrain_x, terrain_y, collision_box_width, collision_box_height, object_id)
                    if new_object not in UniversalVariables.collision_boxes:
                        UniversalVariables.collision_boxes.append(new_object)


    def object_list_creation(self, non_collision_item) -> None:
        for item in non_collision_item:
            object_id, breakability, collision_box, object_width, object_height, object_image = item 
        
            if breakability == True:

                for row in RenderPictures.terrain_in_view:
                    for x, y in row:
                        if self.terrain_data[y][x] == object_id:  # object on leitud kuvatult terrainilt
                            terrain_x: int = x * UniversalVariables.block_size + UniversalVariables.offset_x
                            terrain_y: int = y * UniversalVariables.block_size + UniversalVariables.offset_y

                            new_object = (object_id, terrain_x, terrain_y, object_width, object_height, object_image)

                            if new_object not in UniversalVariables.object_list:
                                UniversalVariables.object_list.append(
                                    (object_id, terrain_x, terrain_y, object_width, object_height, object_image)
                                    )
                            break

                # id_sort_order = {6:1, 5:2, 2:3, 4:4, 7:5, 988:6, 9882:7, 1000:8}   # 6 = First to be rendered, 1000 = Last to be rendered
                # 
                # # Sort the collision_boxes list based on the custom sort order
                # UniversalVariables.collision_boxes = sorted(UniversalVariables.collision_boxes, key=lambda box: (id_sort_order.get(box[4], float('inf')), box[1]))


if __name__ == '__main__':  ...