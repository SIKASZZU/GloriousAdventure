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
        RenderPictures.terrain_in_view: list = []

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
                        self.row.append((col, row))  # 25.06.24, keerasin col ja row ymber, sest collision box listi refactorimisel l2ks midagi pekki.
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

                            elif terrain_value == 1000:  
                                image = ImageLoader.load_image('Final_Maze_Ground_2')  # MAZE GROUND BACKGROUNDI LISAMINE
                                RenderPictures.image_to_sequence(self,terrain_x, terrain_y, position,image, terrain_value)

                            elif terrain_value == 933 or terrain_value == 977:
                                # mu aju ytleb, et see elif lihtsalt 2ra kustutada, sest allpool on juba see, et laeb k6ik objekti id'de pealt sise
                                # aga kui seda elifi ei ole, siis 66sel uksed kinni ei l2he, idk miks

                                if EssentialsUpdate.day_night_text == 'Night':  
                                    self.terrain_data[position[1]][position[0]] = 977
                                    
                                    image = ImageLoader.load_image('Maze_End_Bottom')  # MAZE GROUND BACKGROUNDI LISAMINE
                                    RenderPictures.image_to_sequence(self,terrain_x, terrain_y, position,image, terrain_value)
                                else:  
                                    self.terrain_data[position[1]][position[0]] = 933
                                
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


    def object_render():
        for item in UniversalVariables.object_list:
            if item[4] is None:
                continue

            position = item[:2]  # x, y
            scaled_object_image = pygame.transform.scale(item[4], item[2:4])  # image, sizes
            UniversalVariables.screen.blit(scaled_object_image, position)


class ObjectCreation:

    def creating_lists(self):
        # print(f'\n UniversalVariables.collision_boxes len:{len(UniversalVariables.collision_boxes)} {UniversalVariables.collision_boxes}')
        # print(f'\n UniversalVariables.object_list len:{len(UniversalVariables.object_list)} {UniversalVariables.object_list}')

        UniversalVariables.collision_boxes = []
        UniversalVariables.object_list = []
        
        collision_items = []
        non_collision_items = []
        items_not_designed_for_list = [98, 989_98, 988]  # maze groundid vmdgi taolist

        for item in items_list:
            if item.get("Type") == "Object":
                object_id = item.get("ID")
                if object_id in items_not_designed_for_list:
                    continue
                else:
                    object_image_name = item.get("Name")
                    object_image      = ImageLoader.load_image(object_image_name)
                    breakability      = item.get('Breakable')
                    object_width      = item.get("Object_width")
                    object_height     = item.get("Object_height")
                    collision_box     = item.get("Collision_box")

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
                    if a_item[2] is None:  # if collision box is none or collision box item is clickable etc door, keyholder
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
            
            #if object_id not in UniversalVariables.no_terrain_background_items:
                
            for row in RenderPictures.terrain_in_view:
                for x, y in row:
                    if self.terrain_data[y][x] == object_id:  # object on leitud kuvatult terrainilt
                        terrain_x: int = x * UniversalVariables.block_size + UniversalVariables.offset_x
                        terrain_y: int = y * UniversalVariables.block_size + UniversalVariables.offset_y

                        new_object = (terrain_x, terrain_y, object_width, object_height, object_image, object_id)

                        if new_object not in UniversalVariables.object_list:
                            UniversalVariables.object_list.append(
                                (terrain_x, terrain_y, object_width, object_height, object_image, object_id)
                                )

if __name__ == '__main__':  ...