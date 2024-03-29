import pygame

from items import items_list
from components import player
from inventory import Inventory
from render import RenderPictures
from update import EssentsialsUpdate
from objects import ObjectManagement
from variables import UniversalVariables
from components import StaminaComponent
from mazecalculation import AddingMazeAtPosition
from camera import Camera

class Collisions:

    render_after = bool  # Vajalik teadmiseks kas player renderida enne v6i p2rast objekte
    keylock = 0

    def check_collisions(self) -> None:
        keys = pygame.key.get_pressed()

        interaction_boxes = {}  # Object id, pilt, ja pildi suurus

        for collision_box_x, collision_box_y, collision_box_width, collision_box_height, object_id, collision_box_offset_x, collision_box_offset_y in UniversalVariables.collision_boxes:

            # See mis listis on, seda on vaja, et see listist ära võtta, ära võttes kaob see mapi pealt ära
            obj_collision_box = (
            collision_box_x, collision_box_y, collision_box_width, collision_box_height, object_id, collision_box_offset_x, collision_box_offset_y)

            terrain_x: int = collision_box_x - collision_box_offset_x
            terrain_y: int = collision_box_y - collision_box_offset_y

            for item in items_list:
                if item.get("Type") == "Object" and item.get("ID") == object_id:
                    width = item.get("Object_width")
                    height = item.get("Object_height")
                    render_when = item.get("Render_when")

                    interaction_boxes[object_id] = (width, height)

            collision_object_rect = pygame.Rect(terrain_x, terrain_y, width, height)  # See on täpsemate arvudega, kui self.collision_box


            # Clickides saab avada ukse - uue maze
            if EssentsialsUpdate.day_night_text != 'Day':
                ### TODO: not open door at night WRITE ON SCREEN
                
                pass
            else:
                if self.click_window_x and self.click_window_y:
                    if terrain_x < Camera.click_x < terrain_x + width and terrain_y < Camera.click_y < terrain_y + height:

                        # Kinniste uste ID'd
                        if object_id in [94, 95, 96, 97]:
                            
                            # For opening the door remove one key from inventory
                            if 'Maze_Key' in Inventory.inventory:
                                ObjectManagement.remove_object_from_inv('Maze_Key')

                                if Collisions.keylock == 0:
                                    Collisions.keylock += 1

                                    # Sellega saab suuna kätte, '94: 3' - vasakule
                                    locations = {95: 1, 97: 2, 94: 3, 96: 4}  # location on 1 ylesse, 2 alla, 3 vasakule, 4 paremale
                                    location = locations[object_id]

                                    grid_x, grid_y = terrain_x // UniversalVariables.block_size, terrain_y // UniversalVariables.block_size

                                    j = (grid_y // 39) * 39  # Y koordinaat
                                    i = (grid_x // 39) * 39  # X kooridnaat

                                    if location == 1 or location == 2:
                                        AddingMazeAtPosition.update_terrain(self, location, i, grid_x, object_id, grid_y)  # Vaatab x coordinaati
                                    else:   # 3, 4
                                        AddingMazeAtPosition.update_terrain(self, location, j, grid_x, object_id, grid_y)  # Vaatab y coordinaati
            
            if self.player_rect.colliderect(collision_object_rect):
                if keys[pygame.K_SPACE]:
                    ObjectManagement.remove_object_at_position(self, terrain_x, terrain_y, obj_collision_box, object_id)

                if object_id == 99 or object_id == 98:
                    Collisions.render_after = True

                else:
                    if (collision_object_rect[1] + render_when) <= self.player_rect[1]:
                        Collisions.render_after = True
                    else: 
                        Collisions.render_after = False

        # Peale checkimist clearib click x/y history ära
        if self.click_window_x and self.click_window_y and self.click_position:
            self.click_position: tuple[int, int] = ()
            self.click_window_x = None
            self.click_window_y = None

        Collisions.collision_hitbox(self)


    def collision_hitbox(self) -> None:
        keys = pygame.key.get_pressed()  # Jälgib keyboard inputte
        for \
                collision_box_x, collision_box_y, \
                collision_box_width, collision_box_height,\
                object_id, collision_box_offset_x,\
                collision_box_offset_y in UniversalVariables.collision_boxes:

            collision_object_hitbox = pygame.Rect(collision_box_x, collision_box_y, collision_box_width, collision_box_height)

            # Kui player jookseb siis ta ei lähe läbi objektide
            if keys[pygame.K_LSHIFT] and player.stamina.current_stamina != 0:
                collision_move = 10

            else:
                collision_move = 4

            # Kui läheb vastu hitboxi siis ei lase sellest läbi minna
            if self.player_rect.colliderect(collision_object_hitbox):

                # Arvutab, kui palju objekti hitbox on suurem (või väiksem) kui mängija hitbox
                dx = (self.player_rect.centerx - collision_object_hitbox.centerx) / (
                            UniversalVariables.player_width / 2 + collision_box_width / 2)
                dy = (self.player_rect.centery - collision_object_hitbox.centery) / (
                            UniversalVariables.player_height / 2 + collision_box_height / 2)

                # Horisontaalne kokkupuude
                if abs(dx) > abs(dy):
                    # Paremalt poolt
                    if dx > 0:
                        UniversalVariables.player_x += collision_move  # Liigutab mängijat paremale
                    # Vasakultpoolt
                    else:
                        UniversalVariables.player_x -= collision_move  # Liigutab mängijat vasakule

                # Vertikaalne kokkupuude
                else:
                    # Alt
                    if dy > 0:
                        UniversalVariables.player_y += collision_move  # Liigutab mängijat alla
                    # Ülevalt
                    else:
                        UniversalVariables.player_y -= collision_move  # Liigutab mängijat ülesse


    def collison_terrain(self) -> None:
        keys = pygame.key.get_pressed()

        player_grid_row = int(UniversalVariables.player_x // UniversalVariables.block_size)
        player_grid_col = int(UniversalVariables.player_y // UniversalVariables.block_size)

        # Vaatab terraini mida ta renerib ja selle järgi kontrollib collisoneid
        for i in range(player_grid_col - RenderPictures.render_range, player_grid_col + RenderPictures.render_range + 1):
            for j in range(player_grid_row - RenderPictures.render_range, player_grid_row + RenderPictures.render_range + 1):

                # Vaatab terrain recti ja playeri collisoneid
                terrain_rect = pygame.Rect(j * UniversalVariables.block_size, i * UniversalVariables.block_size, UniversalVariables.block_size, UniversalVariables.block_size)
                if self.player_rect.colliderect(terrain_rect):
                    sprinting = keys[pygame.K_LSHIFT] and keys[pygame.K_d] or \
                        keys[pygame.K_LSHIFT] and keys[pygame.K_a] or \
                        keys[pygame.K_LSHIFT] and keys[pygame.K_w] or \
                        keys[pygame.K_LSHIFT] and keys[pygame.K_s]
                    # Kontrollib kas terrain block jääb faili terrain_data piiridesse
                    if 0 <= i < len(self.terrain_data) and 0 <= j < len(self.terrain_data[i]):

                        in_water = self.terrain_data[i][j] == 0

                        
                        if in_water != True:
                            # Player asub maal
                            if sprinting:
                                # stamina = 0 - playeri speed = base speed
                                if player.stamina.current_stamina == 0:
                                    player.stamina.stamina_regenerate(0.05)
                                    player.speed.current_speed = player.speed.base_speed
                                else:
                                    player.speed.current_speed = player.speed.base_speed * 2.5
                                    StaminaComponent.stamina_bar_decay = 0  # Toob stamina bari uuesti nähtavale
                                    player.stamina.use_stamina(0.05)
                            else:
                                player.speed.current_speed = player.speed.base_speed
                                player.stamina.stamina_regenerate(0.05)

                        ### Siin on koodikordus sellest, et kas on vees v6i mapist v2ljas.

                        else:  # Player asub vees
                            if sprinting:
                                # stamina = 0 - playeri speed = base speed
                                if player.stamina.current_stamina == 0:
                                    player.stamina.stamina_regenerate(0.05)
                                    player.speed.current_speed = player.speed.base_speed / 2
                                else:
                                    player.speed.current_speed = player.speed.base_speed
                                    StaminaComponent.stamina_bar_decay = 0  # Toob stamina bari uuesti nähtavale
                                    player.stamina.use_stamina(0.05)
                            else:
                                player.speed.current_speed = player.speed.base_speed / 2
                                player.stamina.stamina_regenerate(0.05)

                    else:  # Player asub mapist v2ljas
                        if sprinting:
                            # stamina = 0 - playeri speed = base speed
                            if player.stamina.current_stamina == 0:
                                player.stamina.stamina_regenerate(0.05)
                                player.speed.current_speed = player.speed.base_speed / 2
                            else:
                                player.speed.current_speed = player.speed.base_speed
                                StaminaComponent.stamina_bar_decay = 0  # Toob stamina bari uuesti nähtavale
                                player.stamina.use_stamina(0.05)
                        else:
                            player.speed.current_speed = player.speed.base_speed / 2
                            player.stamina.stamina_regenerate(0.05)
