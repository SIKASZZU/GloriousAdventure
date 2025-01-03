import pygame

from items import items_list
from functions import UniversalFunctions


class Interaction:
    def __init__(self, pupdate, paudio, tile_sounds, td, camera, 
                inv, essentials, map_data, fading_text, maze_addition, o_management, variables, CLOSED_DOOR_IDS, loot):
        self.player_update = pupdate
        self.player_audio = paudio
        self.tile_sounds = tile_sounds
        self.terrain_data = td
        self.camera = camera
        self.inv = inv
        self.essentials = essentials
        self.map_data = map_data
        self.fading_text = fading_text
        self.maze_addition = maze_addition
        self.object_management = o_management
        self.variables = variables
        self.CLOSED_DOOR_IDS = CLOSED_DOOR_IDS
        self.loot = loot

        self.keylock: int = 0
        self.first_time_collision = False  # et blitiks screenile, et spacebariga saab yles v6tta

    def colliderect(self, collision_object_rect, object_id, terrain_x, terrain_y):
        """ Player collision itemiga ja siis tekib interaction. Barreli, key yles v6tmine space bariga. """

        keys = pygame.key.get_pressed()  # Jälgib keyboard inputte

        if self.player_update.player_rect.colliderect(collision_object_rect):
            pick_up_items = {item[5] for item in self.variables.object_list}

            if self.first_time_collision == False and object_id in pick_up_items:
                self.first_time_collision = True
                self.variables.ui_elements.append(""" Press SPACE to pick up items. """)

            if keys[pygame.K_SPACE]:
                if object_id == 1001:  # panin selle if statementi, kuigi see ei muuda mdiagi. id 1001 ei ole m6jutatud removeobjectatposition functioonist.
                    self.loot.loot_update(player_pressed_pick_up=True)
                else:
                    self.object_management.remove_object_at_position( terrain_x, terrain_y, object_id)

            # find render when for item
            # FIXME: See on siin, sest miks? OK, variableid on olemas ja puha aga miks mitte collisionis.
            for item in items_list:
                if item.id == object_id:
                    render_when = item.render_when

            if render_when != None:
                point_of_render_after = collision_object_rect[1] + render_when
                if point_of_render_after <= self.player_update.player_rect[1]:
                    self.variables.render_after = True
                else:
                    self.variables.render_after = False

    def objects(self) -> None:
        """ Playeri interactionid objektidega. Ntks keyholderid, doors. """

        collision_object_rect = pygame.Rect(0, 0, 0, 0)

        for terrain_x, terrain_y, object_width, object_height, _, object_id in self.variables.object_list:
            terrain_x: int = terrain_x - self.variables.offset_x
            terrain_y: int = terrain_y - self.variables.offset_y

            collision_object_rect = pygame.Rect(terrain_x, terrain_y, object_width, object_height)
            self.colliderect(collision_object_rect, object_id, terrain_x, terrain_y)

            if not self.camera.click_window_x and not self.camera.click_window_y:
                continue

            # VAJALIK: imelik kood, laseb ainult ühe block click info läbi
            if terrain_x < self.camera.click_x < terrain_x + object_width and terrain_y < self.camera.click_y < terrain_y + object_height:

                terrain_grid_x = int(terrain_x // self.variables.block_size)
                terrain_grid_y = int(terrain_y // self.variables.block_size)

                if object_id == 981:  # Paneb key
                    if not 'Maze_Key' in self.inv.inventory or self.variables.current_equipped_item != 'Maze_Key':  # and self.variables.final_maze == True:
                        self.player_audio.error_audio()

                        text = "Shouldn't we put something here?"
                        if text in self.fading_text.shown_texts:
                            self.fading_text.shown_texts.remove(text)
                        self.variables.ui_elements.append(text)

                        # self.camera.reset_clicks()
                        return
                    else:
                        if self.variables.final_maze != True:
                            self.terrain_data[terrain_grid_y][terrain_grid_x] = 982  # Key slotti
                            self.object_management.remove_object_from_inv('Maze_Key')
                            self.variables.portal_frames += 1

                            self.tile_sounds.insert_key_audio()
                            # self.camera.reset_clicks()

                        # Kui clickid tühja keysloti peale ja key on invis
                        else:
                            self.terrain_data[terrain_grid_y][terrain_grid_x] = 982  # Key slotti
                            self.object_management.remove_object_from_inv('Maze_Key')

                            self.tile_sounds.insert_key_audio()
                            UniversalFunctions.gray_yellow(self, 'yellow')
                    # self.camera.reset_clicks()  # KUI OBJECT_ID'D EI LEITUD, clearib click x/y history ära.

                if object_id == 982:
                    if self.variables.final_maze != True:
                        self.terrain_data[terrain_grid_y][terrain_grid_x] = 981  # Key slotti
                        self.variables.portal_frames -= 1

                        self.tile_sounds.insert_key_audio()
                        # self.camera.reset_clicks()

                    # Kui portal on roheline, võtad key ära, portal läheb kollaseks ja 1 läheb halliks
                    if UniversalFunctions.count_occurrences_in_list_of_lists(self.terrain_data,
                                                                             555) and UniversalFunctions.count_occurrences_in_list_of_lists(
                            self.terrain_data, 982) <= 8:

                        self.variables.ui_elements.append(
                            "Yet, with every passing moment, the portal's brilliance wanes, "
                            "its ethereal glow dimming until it flickers and fades into darkness once more, "
                            "sealing away the mysteries of the sanctum."
                        )

                        self.object_management.add_object_from_inv('Maze_Key')
                        self.terrain_data[terrain_grid_y][terrain_grid_x] = 981  # Key slotist välja

                        self.tile_sounds.portal_close_audio()
                        self.tile_sounds.pop_key_audio()
                        UniversalFunctions.yellow_green(self, 'yellow')
                        x, y = UniversalFunctions.find_number_in_list_of_lists(self.terrain_data, 1000)
                        self.terrain_data[x][y] = 9882

                        self.variables.portal_list = []
                        self.variables.portal_frame_rect = None

                    else:  # Kui slotist võtad key ära
                        self.object_management.add_object_from_inv('Maze_Key')
                        self.terrain_data[terrain_grid_y][terrain_grid_x] = 981  # Key slotist välja

                        self.tile_sounds.pop_key_audio()
                        UniversalFunctions.gray_yellow(self, 'gray')

                if object_id in self.CLOSED_DOOR_IDS.value:  # Kinniste uste ID'd. Clickides saab avada ukse - uue maze
                    if self.essentials.day_night_text != 'Day':
                        self.player_audio.error_audio()

                        text = ("Can't open new maze during night.")
                        if text in self.fading_text.shown_texts:
                            self.fading_text.shown_texts.remove(text)
                        self.variables.ui_elements.append(text)

                        # self.camera.reset_clicks()
                        return

                    # For opening the door remove one key from inventory
                    else:
                        if not 'Maze_Key' in self.inv.inventory:
                            self.player_audio.error_audio()

                            text = ("No available Maze key in inventory.")
                            if text in self.fading_text.shown_texts:
                                self.fading_text.shown_texts.remove(text)
                            self.variables.ui_elements.append(text)

                            # self.camera.reset_clicks()
                            return

                        if self.keylock != 0:
                            continue

                        self.keylock += 1

                        # location on 1 ylesse, 2 alla, 3 vasakule, 4 paremale
                        locations = {
                            95: 1, 97: 2, 94: 3, 96: 4}
                        location = locations[object_id]

                        grid_x, grid_y = terrain_x // self.variables.block_size, terrain_y // self.variables.block_size

                        if self.variables.first_time:
                            for _ in range(2):

                                new_row = ['place' for _ in range(len(self.variables.map_list[0]))]
                                self.variables.map_list.insert(0, new_row)

                                for row in range(39):
                                    self.terrain_data.insert(0, [None] * len(self.terrain_data[0]))

                                for row in self.variables.map_list:
                                    row.insert(0, 'place')

                                for row in self.terrain_data:
                                    for row_len in range(39):
                                        row.insert(0, None)

                                # teleb playeri ja camera 6igesse kohta
                                self.variables.player_x += 39 * self.variables.block_size
                                self.variables.player_y += 39 * self.variables.block_size
                                self.camera.camera_rect.left = self.camera.camera_rect.left + 39 * self.variables.block_size
                                self.camera.camera_rect.top = self.camera.camera_rect.top + 39 * self.variables.block_size

                            self.variables.first_time = False
                            grid_x, grid_y = grid_x + 80, grid_y + 80

                        j = (grid_y // 39) * 39  # Y koordinaat
                        i = (grid_x // 39) * 39  # X kooridnaat

                        if location == 1 or location == 2:  # top and bottom
                            self.maze_addition.update_terrain(location, i, grid_x, object_id,
                                                                grid_y)  # Vaatab x coordinaati
                        else:  # left and right
                            self.maze_addition.update_terrain(location, j, grid_x, object_id,
                                                                grid_y)  # Vaatab y coordinaati
                        # self.camera.reset_clicks()

                # self.camera.reset_clicks()  # KUI OBJECT_ID'D EI LEITUD, clearib click x/y history ära.
        # self.camera.reset_clicks()
