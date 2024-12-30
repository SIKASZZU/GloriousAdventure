import pygame

from text import Fading_text
from items import items_list
from update import EssentialsUpdate
from objects import ObjectManagement
from variables import GameConfig
from variables import UniversalVariables
from mazecalculation import AddingMazeAtPosition
from camera import Camera
from audio import Tile_Sounds, Player_audio
from loot import Loot
from functions import UniversalFunctions


class Interaction:
    keylock: int = 0
    first_time_collision = False  # et blitiks screenile, et spacebariga saab yles v6tta

    def colliderect(self, collision_object_rect, object_id, terrain_x, terrain_y):
        """ Player collision itemiga ja siis tekib interaction. Barreli, key yles v6tmine space bariga. """

        keys = pygame.key.get_pressed()  # Jälgib keyboard inputte

        if self.player_rect.colliderect(collision_object_rect):
            pick_up_items = {item[5] for item in UniversalVariables.object_list}

            if Interaction.first_time_collision == False and object_id in pick_up_items:
                Interaction.first_time_collision = True
                UniversalVariables.ui_elements.append(""" Press SPACE to pick up items. """)

            if keys[pygame.K_SPACE]:
                if object_id == 1001:  # panin selle if statementi, kuigi see ei muuda mdiagi. id 1001 ei ole m6jutatud removeobjectatposition functioonist.
                    # Loot.loot_update(self, True)
                    ...
                else:
                    ObjectManagement.remove_object_at_position(self, terrain_x, terrain_y, object_id)

            # find render when for item
            # FIXME: See on siin, sest miks? OK, variableid on olemas ja puha aga miks mitte collisionis.
            for item in items_list:
                if item.id == object_id:
                    render_when = item.render_when

            if render_when != None:
                point_of_render_after = collision_object_rect[1] + render_when
                if point_of_render_after <= self.player_rect[1]:
                    UniversalVariables.render_after = True
                else:
                    UniversalVariables.render_after = False

    def objects(self) -> None:
        """ Playeri interactionid objektidega. Ntks keyholderid, doors. """

        collision_object_rect = pygame.Rect(0, 0, 0, 0)

        for terrain_x, terrain_y, object_width, object_height, _, object_id in UniversalVariables.object_list:
            terrain_x: int = terrain_x - UniversalVariables.offset_x
            terrain_y: int = terrain_y - UniversalVariables.offset_y

            collision_object_rect = pygame.Rect(terrain_x, terrain_y, object_width, object_height)
            Interaction.colliderect(self, collision_object_rect, object_id, terrain_x, terrain_y)

            if not self.camera.click_window_x and not self.camera.click_window_y:
                continue

            # VAJALIK: imelik kood, laseb ainult ühe block click info läbi
            if terrain_x < self.camera.click_x < terrain_x + object_width and terrain_y < self.camera.click_y < terrain_y + object_height:

                terrain_grid_x = int(terrain_x // UniversalVariables.block_size)
                terrain_grid_y = int(terrain_y // UniversalVariables.block_size)

                if object_id == 981:  # Paneb key
                    if not 'Maze_Key' in self.inv.inventory or UniversalVariables.current_equipped_item != 'Maze_Key':  # and UniversalVariables.final_maze == True:
                        Player_audio.error_audio(self)

                        text = "Shouldn't we put something here?"
                        if text in Fading_text.shown_texts:
                            Fading_text.shown_texts.remove(text)
                        UniversalVariables.ui_elements.append(text)

                        Camera.reset_clicks(self)
                        return
                    else:
                        if UniversalVariables.final_maze != True:
                            self.terrain_data[terrain_grid_y][terrain_grid_x] = 982  # Key slotti
                            ObjectManagement.remove_object_from_inv(self, 'Maze_Key')
                            UniversalVariables.portal_frames += 1

                            Tile_Sounds.insert_key_audio(self)
                            Camera.reset_clicks(self)

                        # Kui clickid tühja keysloti peale ja key on invis
                        else:
                            self.terrain_data[terrain_grid_y][terrain_grid_x] = 982  # Key slotti
                            ObjectManagement.remove_object_from_inv(self, 'Maze_Key')

                            Tile_Sounds.insert_key_audio(self)
                            UniversalFunctions.gray_yellow(self, 'yellow')
                    Camera.reset_clicks(self)  # KUI OBJECT_ID'D EI LEITUD, clearib click x/y history ära.

                if object_id == 982:
                    if UniversalVariables.final_maze != True:
                        self.terrain_data[terrain_grid_y][terrain_grid_x] = 981  # Key slotti
                        UniversalVariables.portal_frames -= 1

                        Tile_Sounds.insert_key_audio(self)
                        Camera.reset_clicks(self)

                    # Kui portal on roheline, võtad key ära, portal läheb kollaseks ja 1 läheb halliks
                    if UniversalFunctions.count_occurrences_in_list_of_lists(self.terrain_data,
                                                                             555) and UniversalFunctions.count_occurrences_in_list_of_lists(
                            self.terrain_data, 982) <= 8:

                        UniversalVariables.ui_elements.append(
                            "Yet, with every passing moment, the portal's brilliance wanes, "
                            "its ethereal glow dimming until it flickers and fades into darkness once more, "
                            "sealing away the mysteries of the sanctum."
                        )

                        ObjectManagement.add_object_from_inv(self, 'Maze_Key')
                        self.terrain_data[terrain_grid_y][terrain_grid_x] = 981  # Key slotist välja

                        Tile_Sounds.portal_close_audio(self)
                        Tile_Sounds.pop_key_audio(self)
                        UniversalFunctions.yellow_green(self, 'yellow')
                        x, y = UniversalFunctions.find_number_in_list_of_lists(self.terrain_data, 1000)
                        self.terrain_data[x][y] = 9882

                        UniversalVariables.portal_list = []
                        UniversalVariables.portal_frame_rect = None

                    else:  # Kui slotist võtad key ära
                        ObjectManagement.add_object_from_inv(self, 'Maze_Key')
                        self.terrain_data[terrain_grid_y][terrain_grid_x] = 981  # Key slotist välja

                        Tile_Sounds.pop_key_audio(self)
                        UniversalFunctions.gray_yellow(self, 'gray')

                if object_id in GameConfig.CLOSED_DOOR_IDS.value:  # Kinniste uste ID'd. Clickides saab avada ukse - uue maze
                    if self.essentials.day_night_text != 'Day':
                        Player_audio.error_audio(self)

                        text = ("Can't open new maze during night.")
                        if text in Fading_text.shown_texts:
                            Fading_text.shown_texts.remove(text)
                        UniversalVariables.ui_elements.append(text)

                        Camera.reset_clicks(self)
                        return

                    # For opening the door remove one key from inventory
                    else:
                        if not 'Maze_Key' in self.inv.inventory:
                            Player_audio.error_audio(self)

                            text = ("No available Maze key in inventory.")
                            if text in Fading_text.shown_texts:
                                Fading_text.shown_texts.remove(text)
                            UniversalVariables.ui_elements.append(text)

                            Camera.reset_clicks(self)
                            return

                        if Interaction.keylock != 0:
                            continue

                        Interaction.keylock += 1

                        # location on 1 ylesse, 2 alla, 3 vasakule, 4 paremale
                        locations = {
                            95: 1, 97: 2, 94: 3, 96: 4}
                        location = locations[object_id]

                        grid_x, grid_y = terrain_x // UniversalVariables.block_size, terrain_y // UniversalVariables.block_size

                        if UniversalVariables.first_time:
                            for _ in range(2):

                                new_row = ['place' for _ in range(len(UniversalVariables.map_list[0]))]
                                UniversalVariables.map_list.insert(0, new_row)

                                for row in range(39):
                                    self.terrain_data.insert(0, [None] * len(self.terrain_data[0]))

                                for row in UniversalVariables.map_list:
                                    row.insert(0, 'place')

                                for row in self.terrain_data:
                                    for row_len in range(39):
                                        row.insert(0, None)

                                # teleb playeri ja camera 6igesse kohta
                                UniversalVariables.player_x += 39 * UniversalVariables.block_size
                                UniversalVariables.player_y += 39 * UniversalVariables.block_size
                                self.camera.camera_rect.left = self.camera.camera_rect.left + 39 * UniversalVariables.block_size
                                self.camera.camera_rect.top = self.camera.camera_rect.top + 39 * UniversalVariables.block_size

                            UniversalVariables.first_time = False
                            grid_x, grid_y = grid_x + 80, grid_y + 80

                        j = (grid_y // 39) * 39  # Y koordinaat
                        i = (grid_x // 39) * 39  # X kooridnaat

                        if location == 1 or location == 2:  # top and bottom
                            AddingMazeAtPosition.update_terrain(self, location, i, grid_x, object_id,
                                                                grid_y)  # Vaatab x coordinaati
                        else:  # left and right
                            AddingMazeAtPosition.update_terrain(self, location, j, grid_x, object_id,
                                                                grid_y)  # Vaatab y coordinaati
                        Camera.reset_clicks(self)

                Camera.reset_clicks(self)  # KUI OBJECT_ID'D EI LEITUD, clearib click x/y history ära.
        Camera.reset_clicks(self)
