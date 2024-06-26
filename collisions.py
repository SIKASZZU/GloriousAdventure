import pygame

from items import items_list
from inventory import Inventory
from render import RenderPictures
from update import EssentialsUpdate
from objects import ObjectManagement
from variables import UniversalVariables
from HUD import HUD_class
from mazecalculation import AddingMazeAtPosition
from camera import Camera
from audio import Tile_Sounds, Player_audio  # insert_key_audio, pop_key_audio, portal_open_audio


def find_number_in_list_of_lists(list_of_lists, number):
    for row_index, sublist in enumerate(list_of_lists):
        for col_index, element in enumerate(sublist):
            if element == number:
                return row_index, col_index  # Number found, return its coordinates
    return None  # Number not found, return None


def count_occurrences_in_list_of_lists(list_of_lists, number):
    count = 0
    for sublist in list_of_lists:
        for element in sublist:
            if element == number:
                count += 1
    return count


def reset_clicks(self):
    if self.click_window_x and self.click_window_y:
       # self.click_position: tuple[int, int] = ()  # ei pea resettima self.click_positioni, vist ikka peab
        self.click_window_x = None
        self.click_window_y = None


def gray_yellow(self, color):
    if color == 'gray':
        x, y = find_number_in_list_of_lists(self.terrain_data, 550)
        self.terrain_data[x][y] = 500
        reset_clicks(self)

    if color == 'yellow':
        x, y = find_number_in_list_of_lists(self.terrain_data, 500)
        self.terrain_data[x][y] = 550
        reset_clicks(self)


def yellow_green(self, color):
    if color == 'yellow':
        for i in range(8):
            x, y = find_number_in_list_of_lists(self.terrain_data, 555)
            self.terrain_data[x][y] = 550
            reset_clicks(self)

        gray_yellow(self, 'gray')


    elif color == 'green':
        for i in range(8):
            x, y = find_number_in_list_of_lists(self.terrain_data, 550)

            self.terrain_data[x][y] = 555
            reset_clicks(self)


class Collisions:
    render_after = bool  # Vajalik teadmiseks kas player renderida enne v6i p2rast objekte
    keylock: int = 0
    object_dict = {}
    first_time_collision = False  # et blitiks screenile, et spacebariga saab yles v6tta

    def change_map_data(self) -> None:
        keys = pygame.key.get_pressed()  # Jälgib keyboard inputte
        collision_object_rect = pygame.Rect(0,0,0,0)

        for terrain_x, terrain_y, object_width, object_height, _, object_id in UniversalVariables.object_list:
            terrain_x: int = terrain_x - UniversalVariables.offset_x
            terrain_y: int = terrain_y - UniversalVariables.offset_y

            for item in items_list:
               if item.get("ID") == object_id:
                    render_when = item.get("Render_when")

            collision_object_rect = pygame.Rect(terrain_x, terrain_y, object_width, object_height)
            if self.player_rect.colliderect(collision_object_rect):
                pick_up_items = {item[5] for item in UniversalVariables.object_list}

                if Collisions.first_time_collision == False and object_id in pick_up_items:
                    Collisions.first_time_collision = True
                    UniversalVariables.ui_elements.append(""" Press SPACE to pick up items. """)

                if keys[pygame.K_SPACE]:  ObjectManagement.remove_object_at_position(self, terrain_x, terrain_y, object_id)

                if object_id == 99 or object_id == 98:  Collisions.render_after = True

                else:
                    point_of_render_after = collision_object_rect[1] + render_when
                    if point_of_render_after <= self.player_rect[1]:  Collisions.render_after = True
                    else:  Collisions.render_after = False

            if self.click_window_x and self.click_window_y:
                try:
                    if terrain_x < Camera.click_x < terrain_x + object_width and terrain_y < Camera.click_y < terrain_y + object_height:  # VAJALIK: imelik kood, laseb ainult ühe block click info läbi
                        
                        terrain_grid_x = int(terrain_x // UniversalVariables.block_size)
                        terrain_grid_y = int(terrain_y // UniversalVariables.block_size)

                        if object_id == 981:  # Paneb key
                            if not 'Maze_Key' in Inventory.inventory:  # and UniversalVariables.final_maze == True:
                                Player_audio.error_audio(self)

                                text = "Shouldn't we put something here?"
                                if text in self.shown_texts:
                                    self.shown_texts.remove(text)
                                UniversalVariables.ui_elements.append(text)

                                reset_clicks(self)
                                return
                            else:
                                UniversalVariables.ui_elements.append(
                                    "In the labyrinth's depths, scattered keyholders await, "
                                    "each craving its matching key."
                                )
                                if UniversalVariables.final_maze != True:
                                    self.terrain_data[terrain_grid_y][terrain_grid_x] = 982  # Key slotti
                                    ObjectManagement.remove_object_from_inv('Maze_Key')
                                    UniversalVariables.portal_frames += 1

                                    Tile_Sounds.insert_key_audio(self)
                                    reset_clicks(self)

                                # Kui clickid tühja keysloti peale ja key on invis
                                else:
                                    self.terrain_data[terrain_grid_y][terrain_grid_x] = 982  # Key slotti
                                    ObjectManagement.remove_object_from_inv('Maze_Key')

                                    Tile_Sounds.insert_key_audio(self)
                                    gray_yellow(self, 'yellow')
                            reset_clicks(self)  # KUI OBJECT_ID'D EI LEITUD, clearib click x/y history ära.

                        if object_id == 982:
                            if UniversalVariables.final_maze != True:
                                self.terrain_data[terrain_grid_y][terrain_grid_x] = 981  # Key slotti
                                UniversalVariables.portal_frames -= 1

                                Tile_Sounds.insert_key_audio(self)
                                reset_clicks(self)

                            # Kui portal on roheline, võtad key ära, portal läheb kollaseks ja 1 läheb halliks
                            if count_occurrences_in_list_of_lists(self.terrain_data, 555) and count_occurrences_in_list_of_lists(self.terrain_data, 982) <= 8:

                                UniversalVariables.ui_elements.append(
                                    "Yet, with every passing moment, the portal's brilliance wanes, "
                                    "its ethereal glow dimming until it flickers and fades into darkness once more, "
                                    "sealing away the mysteries of the sanctum."
                                )

                                ObjectManagement.add_object_from_inv('Maze_Key')
                                self.terrain_data[terrain_grid_y][terrain_grid_x] = 981  # Key slotist välja

                                Tile_Sounds.portal_close_audio(self)
                                Tile_Sounds.pop_key_audio(self)
                                yellow_green(self, 'yellow')
                                x, y = find_number_in_list_of_lists(self.terrain_data, 1000)
                                self.terrain_data[x][y] = 988

                                UniversalVariables.portal_list = []
                                UniversalVariables.portal_frame_rect = None

                            else:  # Kui slotist võtad key ära
                                ObjectManagement.add_object_from_inv('Maze_Key')
                                self.terrain_data[terrain_grid_y][terrain_grid_x] = 981  # Key slotist välja

                                Tile_Sounds.pop_key_audio(self)
                                gray_yellow(self, 'gray')

                        if object_id in [94, 95, 96, 97]:  # Kinniste uste ID'd. Clickides saab avada ukse - uue maze
                            if EssentialsUpdate.day_night_text != 'Day':
                                Player_audio.error_audio(self)

                                text = ("Can't open new maze during night.")
                                if text in self.shown_texts:
                                    self.shown_texts.remove(text)
                                UniversalVariables.ui_elements.append(text)

                                reset_clicks(self)
                                return

                            # For opening the door remove one key from inventory
                            else:
                                if not 'Maze_Key' in Inventory.inventory:
                                    Player_audio.error_audio(self)

                                    text =  ("No available Maze key in inventory.")
                                    if text in self.shown_texts:
                                        self.shown_texts.remove(text)
                                    UniversalVariables.ui_elements.append(text)

                                    reset_clicks(self)
                                    return

                                else:
                                    if UniversalVariables.maze_counter >= 3:
                                        UniversalVariables.final_maze = True

                                    if Collisions.keylock == 0:
                                        Collisions.keylock += 1

                                        # Sellega saab suuna kätte, '94: 3' - vasakule
                                        locations = {95: 1, 97: 2, 94: 3,
                                                        96: 4}  # location on 1 ylesse, 2 alla, 3 vasakule, 4 paremale
                                        location = locations[object_id]

                                        grid_x, grid_y = terrain_x // UniversalVariables.block_size, terrain_y // UniversalVariables.block_size

                                        j = (grid_y // 39) * 39  # Y koordinaat
                                        i = (grid_x // 39) * 39  # X kooridnaat

                                        if location == 1 or location == 2:
                                            AddingMazeAtPosition.update_terrain(self, location, i, grid_x, object_id,
                                                                                grid_y)  # Vaatab x coordinaati
                                        else:  # 3, 4
                                            AddingMazeAtPosition.update_terrain(self, location, j, grid_x, object_id,
                                                                                grid_y)  # Vaatab y coordinaati
                                        reset_clicks(self)

                        if UniversalVariables.final_maze == True:
                            if UniversalVariables.portal_frames > 0:
                                _ = UniversalVariables.portal_frames
                                for i in range(_):
                                    gray_yellow(self, 'yellow')
                                    UniversalVariables.portal_frames -= 1

                                    if i == 7:
                                        UniversalVariables.portal_frames = 0
                                        break

                            # Teeb portali valmis
                            if count_occurrences_in_list_of_lists(self.terrain_data, 982) >= 8:

                                if count_occurrences_in_list_of_lists(self.terrain_data, 555):
                                    return

                                else:
                                    text = (
                                            "As the final key slides into place, the portal shimmers open, "
                                            "revealing its arcane depths. A resounding hum fills the air, "
                                            "echoing through the labyrinth as the portal's magic pulses with newfound life."
                                        )
                                    if text not in self.shown_texts:
                                        UniversalVariables.ui_elements.append(text)

                                    UniversalVariables.portal_list = []
                                    Tile_Sounds.portal_open_audio(self)
                                    yellow_green(self, 'green')
                                    x, y = find_number_in_list_of_lists(self.terrain_data, 555)
                                    self.terrain_data[x+1][y] = 1000
                                    portal_y, portal_x =\
                                        ((x+1) * UniversalVariables.block_size) + UniversalVariables.block_size / 2,\
                                        (y * UniversalVariables.block_size) + UniversalVariables.block_size / 2

                                    UniversalVariables.portal_list.append((portal_x, portal_y))
                        
                        reset_clicks(self)  # KUI OBJECT_ID'D EI LEITUD, clearib click x/y history ära.
                except TypeError:
                    pass

        reset_clicks(self)  # KUI OBJECT_ID'D EI LEITUD, clearib click x/y history ära.


    def player_hit_collision(self, collision_box) -> None:
        keys = pygame.key.get_pressed()  # Jälgib keyboard inputte

        # Kui player jookseb siis ta ei lähe läbi objektide
        if keys[pygame.K_LSHIFT] and self.player.stamina.current_stamina != 0:  collision_move = 10
        else:  collision_move = 4

        # Arvutab, kui palju objekti hitbox on suurem (või väiksem) kui mängija hitbox
        dx = (self.player_rect.centerx - collision_box.centerx) / (UniversalVariables.player_width / 2 + collision_box[2] / 2)
        dy = (self.player_rect.centery - collision_box.centery) / (UniversalVariables.player_height / 2 + collision_box[3] / 2)
        
        if abs(dx) > abs(dy):
            if dx > 0:  UniversalVariables.player_x += collision_move  # Liigutab mängijat paremale
            else:  UniversalVariables.player_x -= collision_move  # Liigutab mängijat vasakule

        else:
            if dy > 0:  UniversalVariables.player_y += collision_move  # Liigutab mängijat alla
            else:  UniversalVariables.player_y -= collision_move  # Liigutab mängijat ülesse


    def collison_terrain_types(self) -> None:
        keys = pygame.key.get_pressed()

        player_grid_row = int(UniversalVariables.player_x // UniversalVariables.block_size)
        player_grid_col = int(UniversalVariables.player_y // UniversalVariables.block_size)

        # Vaatab terraini mida ta renerib ja selle järgi kontrollib collisoneid
        for row in range(player_grid_col - RenderPictures.render_range, player_grid_col + RenderPictures.render_range + 1):
            for col in range(player_grid_row - RenderPictures.render_range, player_grid_row + RenderPictures.render_range + 1):

                terrain_rect = pygame.Rect(col * UniversalVariables.block_size, row * UniversalVariables.block_size,
                                           UniversalVariables.block_size, UniversalVariables.block_size)
                
                # Vaatab terrain recti ja playeri collisoneid
                if self.player_rect.colliderect(terrain_rect):
                    ### FIXME: Sul on vaja terrain rect v22rtuse asemel collison boxi v22rtusi just row,col koordinaatidel.
                    try:
                        collision_items = {item[4] for item in UniversalVariables.collision_boxes}  # teeb id seti. 
                        
                        if self.terrain_data[row][col] in collision_items:
                            Collisions.player_hit_collision(self, terrain_rect)
                        
                        else:
                            sprinting = keys[pygame.K_LSHIFT] and keys[pygame.K_d] or \
                                        keys[pygame.K_LSHIFT] and keys[pygame.K_a] or \
                                        keys[pygame.K_LSHIFT] and keys[pygame.K_w] or \
                                        keys[pygame.K_LSHIFT] and keys[pygame.K_s]
                            # Kontrollib kas terrain block jääb faili terrain_data piiridesse
                            if 0 <= row < len(self.terrain_data) and 0 <= col < len(self.terrain_data[row]):

                                in_water = self.terrain_data[row][col] == 0

                                if in_water != True:
                                    # Player asub maal
                                    if sprinting:
                                        # stamina = 0 - playeri speed = base speed
                                        if self.player.stamina.current_stamina == 0:
                                            self.player.stamina.stamina_regenerate(0.05)
                                            self.player.speed.current_speed = self.player.speed.base_speed
                                        else:
                                            self.player.speed.current_speed = self.player.speed.base_speed * 1.5
                                            HUD_class.stamina_bar_decay = 0  # Toob stamina bari uuesti nähtavale
                                            self.player.stamina.use_stamina(0.05)
                                    else:
                                        self.player.speed.current_speed = self.player.speed.base_speed
                                        self.player.stamina.stamina_regenerate(0.05)

                                else:  # Player asub vees
                                    if sprinting:
                                        # stamina = 0 - playeri speed = base speed
                                        if self.player.stamina.current_stamina == 0:
                                            self.player.stamina.stamina_regenerate(0.05)
                                            self.player.speed.current_speed = self.player.speed.base_speed / 2
                                        else:
                                            self.player.speed.current_speed = self.player.speed.base_speed
                                            HUD_class.stamina_bar_decay = 0  # Toob stamina bari uuesti nähtavale
                                            self.player.stamina.use_stamina(0.05)
                                    else:
                                        self.player.speed.current_speed = self.player.speed.base_speed / 2
                                        self.player.stamina.stamina_regenerate(0.05)
                                        
                    except Exception as e:  print('Error @ collisions.py, collison_terrain_types:', e)