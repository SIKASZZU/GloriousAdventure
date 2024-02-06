import pygame

from items import items_list
from components import player
from render import RenderPictures
from objects import ObjectManagement
from variables import UniversalVariables
from components import StaminaComponent
from mapupdate import NewMaze
import random
from map import MapData
from mazecalculation import AddingMazeAtPosition

class CollisionGrid:
    def __init__(self, grid_size, screen_width, screen_height):
        self.grid_size = grid_size
        self.columns = int(screen_width / grid_size)
        self.rows = int(screen_height / grid_size)
        self.grid = [[[] for _ in range(self.rows)] for _ in range(self.columns)]

    def add_object_to_grid(self, obj_rect, obj_id):
        column = int(obj_rect.x / self.grid_size)
        row = int(obj_rect.y / self.grid_size)
        self.grid[column][row].append(obj_id)

    def get_nearby_objects(self, obj_rect):
        column = int(obj_rect.x / self.grid_size)
        row = int(obj_rect.y / self.grid_size)
        return self.grid[column][row]

class Collisions:
    render_after = bool  # Vajalik teadmiseks kas player renderida enne v6i p2rast objekte
    keylock = 0
    def __init__(self):
        self.collision_grid = CollisionGrid(grid_size, screen_width, screen_height)

    def check_collisions(self) -> None:
        keys = pygame.key.get_pressed()

        # Object id, pilt, ja pildi suurus
        interaction_boxes = {}

        # Store information about the closest object_id 97
        closest_object_97 = None

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

            if self.player_rect.colliderect(collision_object_rect):
                if keys[pygame.K_SPACE]:
                    ObjectManagement.remove_object_at_position(self, terrain_x, terrain_y, obj_collision_box, object_id)

                if object_id == 99 or object_id == 98:
                    Collisions.render_after = True

                if object_id in [94, 95, 96, 97]:
                    ### location on 1 ylesse, 2 alla, 3 vasakule, 4 paremale
                    if keys[pygame.K_l] and Collisions.keylock == 0:
                        Collisions.keylock += 1
                        print(Collisions.keylock)
                        locations = {95: 1, 97: 2, 94: 3, 96: 4}
                        location = locations[object_id]
                        NewMaze.spawn_maze_at_location(self, location)
                        open_doors = {1: 91, 2: 93, 3: 90, 4: 92}
                        object_id = open_doors[location]
                        grid_x, grid_y = terrain_x // UniversalVariables.block_size, terrain_y // UniversalVariables.block_size

                        j = (grid_y // 39) * 39
                        i = (grid_x // 39) * 39
                        if location == 1 or location == 2:
                            AddingMazeAtPosition.update_terrain(self, location, i, grid_y, object_id, grid_x)  # Vaatab x coordinaati

                        else:
                            AddingMazeAtPosition.update_terrain(self, location, j, grid_x, object_id, grid_y)  # Vaatab y coordinaati

                        if location == 1:
                            UniversalVariables.player_y += 39 * UniversalVariables.block_size

                        if location == 3:
                            UniversalVariables.player_x += 39 * UniversalVariables.block_size

                else:
                    if (collision_object_rect[1] + render_when) <= self.player_rect[1]:
                        Collisions.render_after = True
                    else: 
                        Collisions.render_after = False
        Collisions.collision_hitbox(self)
    def add_maze_to_specific_position(map_list, row_index, col_index):
        # Calculate the new length after adding "maze" to the specified position
        new_length = col_index + 1

        # Check if the specified position is within bounds
        if row_index < len(map_list):
            for row in map_list:
                while len(row) < new_length:
                    row.append('place')

            if map_list[row_index][col_index] == 'place':
                map_list[row_index][col_index] = 'maze'
            elif map_list[row_index][col_index] == 'maze':
                print("Cannot add 'maze' at this position, it's already occupied by 'maze'")
            else:
                print("Cannot add 'maze' at this position, it's occupied by 'glade'")
        else:
            print("Cannot add 'maze' at this position, row_index is out of bounds")


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
