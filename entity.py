import pygame
import math
from collections import deque

from camera import Camera
from images import ImageLoader
from update import EssentialsUpdate
from variables import UniversalVariables
import random


### TODO:
# ghost collision
# kui ghost on samal gridil mis player, v6i selle k6rval, ss hakkab koordinaatidega arvutama.


class Enemy:
    ghost_image = pygame.transform.scale(ImageLoader.load_sprite_image("Ghost"),
                                         (UniversalVariables.block_size // 1.5, UniversalVariables.block_size // 1.5))
    spawned_enemy_dict: dict[str, tuple[pygame.Surface, int, int]] = {}  # (Enemy_image, y, x)
    enemy_in_range: set[tuple[str, str]] = set()

    damage_delay: int = 50  # esimese hiti jaoks, et esimene hit oleks kiirem kui teised
    path_ticks = {}
    path = {}
    save_enemy_direction_x = int
    save_enemy_direction_y = int

    enemy_restricted_areas = [99, 981, 982,  # maze wall stuff
                            9099, 989, 900]  # blade wall stuff
    combined_restricted_areas = set(enemy_restricted_areas).union(set(UniversalVariables.closed_door_ids))
    
    print(combined_restricted_areas)
    def spawn(self):
        """ Spawns enemies based on certain conditions. """

        if not Enemy.spawned_enemy_dict and EssentialsUpdate.day_night_text == 'Night':
            UniversalVariables.find_spawnpoints_in_map_data(self.terrain_data)

            # Player grid calculation
            player_x_row = int(UniversalVariables.player_x // UniversalVariables.block_size)
            player_y_col = int(UniversalVariables.player_y // UniversalVariables.block_size)
            player_grid = (player_y_col, player_x_row)

            distance_from_player = int(UniversalVariables.light_range / UniversalVariables.block_size)

            # Count of spawned enemies
            spawned_enemy_count = 0

            for spawn_point in UniversalVariables.enemy_spawnpoint_list:
                # Check if the spawn point is far enough from the player
                if (abs(player_grid[0] - spawn_point[0]) > distance_from_player or
                        abs(player_grid[1] - spawn_point[1]) > distance_from_player):

                    # Spawn an enemy
                    Enemy.spawned_enemy_dict[f'Enemy_{UniversalVariables.enemy_counter}'] = Enemy.ghost_image, \
                        spawn_point[1], \
                        spawn_point[0]

                    spawned_enemy_count += 1
                    UniversalVariables.enemy_counter += 1

                    # Limiteerib Enemite arvu vastvalt maze_counterile
                    max_enenmy = 5 * UniversalVariables.maze_counter
                    if UniversalVariables.maze_counter == 1: max_enenmy = 2  # Kui on ainult 1 maze siis spawnib max 2 enemit
                    if spawned_enemy_count >= max_enenmy:
                        break

        for enemy in Enemy.spawned_enemy_dict.values():
            enemy_x = enemy[1] * UniversalVariables.block_size + UniversalVariables.offset_x
            enemy_y = enemy[2] * UniversalVariables.block_size + UniversalVariables.offset_y

            UniversalVariables.screen.blit(enemy[0], (enemy_x, enemy_y))

    @staticmethod
    def despawn():
        """ Despawns enemies during the day.  """
        """ Doesn't despawn detected enemies. """

        if EssentialsUpdate.day_night_text == 'Day':
            detected_enemies = {enemy_name for enemy_name, _ in Enemy.enemy_in_range}

            enemies_to_remove = set()

            for enemy_name, _ in Enemy.spawned_enemy_dict.items():
                if enemy_name not in detected_enemies or Enemy.path[enemy_name] == None:
                    enemies_to_remove.add(enemy_name)  # ei saa koheselt removeida, peab tegema uue listi

            for enemy_name in enemies_to_remove:
                del Enemy.spawned_enemy_dict[enemy_name]
            

            Enemy.enemy_in_range.clear()

    @staticmethod
    def custom_round(number):
        if number - math.floor(number) < 0.5:

            return math.floor(number)
        else:
            return math.ceil(number)

    def is_valid(self, x, y):
        """ Check if coordinates (x, y) are valid in the maze. """
        x, y = int(x), int(y)
        
        in_terrain_bounds = 0 <= x < len(self.terrain_data) and 0 <= y < len(self.terrain_data[x])
        
        if in_terrain_bounds and self.terrain_data[x][y] not in Enemy.combined_restricted_areas:
            return True
            
    def find_path_bfs(self, start, end):
        """ Breadth-First Search algorithm to find a path from start to end in the maze. """

        try:
            if self.terrain_data[int(self.player_rect.center[1] // UniversalVariables.block_size)][int(self.player_rect.center[0] // UniversalVariables.block_size)] in Enemy.combined_restricted_areas:
                return None
            else:
                queue = deque([(start, [])])
                visited = set()
                directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

                while queue:
                    (x, y), path = queue.popleft()
                    if (x, y) == end:
                        return path

                    if (x, y) not in visited:
                        visited.add((x, y))
                        for dx, dy in directions:
                            new_x, new_y = x + dx, y + dy
                            if Enemy.is_valid(self, new_x, new_y):
                                new_path = path + [(new_x, new_y)]
                                queue.append(((new_x, new_y), new_path))

                return None
        except IndexError: pass

    @staticmethod
    def move(self):
        """ Move enemies based on their individual decisions."""
        for enemy_name, enemy_info in Enemy.spawned_enemy_dict.items():
            image, x, y = enemy_info
            direction = None

            # Check if the player is in range
            for enemy_name_, dir_ in Enemy.enemy_in_range:
                if enemy_name == enemy_name_:
                    direction = dir_
                    break

            if direction:
                
                enemy_grid = (Enemy.custom_round(enemy_info[2]), Enemy.custom_round(enemy_info[1]))
                if enemy_name not in Enemy.path_ticks or Enemy.path[enemy_name] is None or \
                    Enemy.path_ticks[enemy_name] >= UniversalVariables.enemy_path_update_tick:
                    
                        player_grid = (Enemy.custom_round(self.player_rect.centery // UniversalVariables.block_size),
                                    Enemy.custom_round(self.player_rect.centerx // UniversalVariables.block_size))
                        
                        Enemy.path[enemy_name] = Enemy.find_path_bfs(self, enemy_grid, player_grid)
                        Enemy.path_ticks[enemy_name] = 0
                
                if Enemy.path[enemy_name] == None:
                    pass

                elif len(Enemy.path[enemy_name]) <= 1:
                    # Otsib playerit koordinaatidega
                    next_x, next_y = x, y
                    if direction == 'right':
                        next_x += UniversalVariables.enemy_speed
                    elif direction == 'left':
                        next_x -= UniversalVariables.enemy_speed
                    elif direction == 'down':
                        next_y += UniversalVariables.enemy_speed
                    elif direction == 'up':
                        next_y -= UniversalVariables.enemy_speed

                    next_x, next_y = round(next_x, 3), round(next_y, 3)
                    Enemy.spawned_enemy_dict[enemy_name] = image, next_x, next_y
                
                else:
                    # Otsib playerit grididega
                    next_grid = ((Enemy.path[enemy_name][0][1] - enemy_grid[1]), (Enemy.path[enemy_name][0][0] - enemy_grid[0]))
                    next_x, next_y = x, y

                    # Move enemy based on the next grid
                    next_x += (next_grid[0] * UniversalVariables.enemy_speed)
                    next_y += (next_grid[1] * UniversalVariables.enemy_speed)

                    next_x, next_y = round(next_x, 3), round(next_y, 3)

                    # IMPROVE THIS>>> Entity positsiooni muutmine gridi keskele, sest muidu jookseb seinte sees.
                    if next_x == x and next_y != y:
                        if str(next_x).endswith('.5'):
                            next_x = math.ceil(next_x)
                    if next_y == y and next_x != x:
                        if str(next_y).endswith('.5'):
                            next_y = math.ceil(next_y)
                
                    Enemy.spawned_enemy_dict[enemy_name] = image, next_x, next_y

            # Increment path ticks
            if enemy_name in Enemy.path_ticks:
                Enemy.path_ticks[enemy_name] += 1

    def detection(self):
        player_window_x = Camera.player_window_x
        player_window_y = Camera.player_window_y

        Enemy.enemy_in_range = set()

        for enemy_name, enemy_info in Enemy.spawned_enemy_dict.items():
            enemy_x_grid, enemy_y_grid = enemy_info[1], enemy_info[2]

            enemy_x = enemy_x_grid * UniversalVariables.block_size + UniversalVariables.offset_x
            enemy_y = enemy_y_grid * UniversalVariables.block_size + UniversalVariables.offset_y

            distance_to_player_x_grid = player_window_x - enemy_x
            distance_to_player_y_grid = player_window_y - enemy_y

            if abs(distance_to_player_x_grid) <= 1000 and abs(distance_to_player_y_grid) <= 1000:
                direction: str = 'none'

                if abs(distance_to_player_x_grid) < UniversalVariables.block_size * 0.75 \
                    and abs(distance_to_player_y_grid) < UniversalVariables.block_size * 0.75:
                    if self.player.health.get_health() > 0:
                        Enemy.attack(self, 3, enemy_x, enemy_y)

                if abs(distance_to_player_x_grid) > abs(distance_to_player_y_grid):
                    if distance_to_player_x_grid > 0:
                        direction = 'right'
                    else:
                        direction = 'left'

                else:
                    if distance_to_player_y_grid > 0:
                        direction = 'down'
                    else:
                        direction = 'up'
                Enemy.enemy_in_range.add((enemy_name, direction))

    def attack(self, damage, enemy_direct_x, enemy_direct_y):
        """ Kui Ghost on playeri peal siis saab damage'i. """
        
        if Enemy.damage_delay == 50:
            Enemy.save_enemy_direction_x = enemy_direct_x
            Enemy.save_enemy_direction_y = enemy_direct_y

        if Enemy.damage_delay >= 60:
            self.player.health.damage(damage)
            
            # Calculate knockback direction
            dx = Camera.player_window_x - Enemy.save_enemy_direction_x
            dy = Camera.player_window_y - Enemy.save_enemy_direction_y

            if dx == 0 and dy == 0:
                dx = random.uniform(-1, 1)
                dy = random.uniform(-1, 1)

            distance = (dx ** 2 + dy ** 2) ** 0.5
            dx /= distance
            dy /= distance

            self.player.apply_knockback(dx, dy)

            Enemy.damage_delay = 0
        Enemy.damage_delay += 1

    def health(self):
        """ Has health """
        pass

    def damage_taken(self):
        """ Takes damage. Can die. """
        pass

    @staticmethod
    def collision_with_entities():
        for enemy_name, enemy_info in list(Enemy.spawned_enemy_dict.items()):
            enemy_rect = pygame.Rect(enemy_info[1] * UniversalVariables.block_size,
                                     enemy_info[2] * UniversalVariables.block_size, 73, 73)

            # Check for collisions between enemies
            for other_enemy_name, other_enemy_info in list(Enemy.spawned_enemy_dict.items()):
                if enemy_name != other_enemy_name:
                    other_enemy_rect = pygame.Rect(other_enemy_info[1] * UniversalVariables.block_size,
                                                   other_enemy_info[2] * UniversalVariables.block_size, 73, 73)
                    if enemy_rect.colliderect(other_enemy_rect):
                        enemy_x = enemy_info[1]
                        enemy_y = enemy_info[2]
                        
                        other_enemy_x = other_enemy_info[1]
                        other_enemy_y = other_enemy_info[2]

                        # Calculate displacement vector
                        dx = enemy_x - other_enemy_x
                        dy = enemy_y - other_enemy_y

                        if dx == 0 and dy == 0:
                            dx = random.uniform(-1, 1)
                            dy = random.uniform(-1, 1)

                        # Normalize the displacement vector
                        distance = (dx ** 2 + dy ** 2) ** 0.5
                        dx /= distance
                        dy /= distance

                        # Move the enemy along the displacement vector
                        displacement = 3.0  # See kontrollib, kaugele ta tagasi t6rjutakse
                        enemy_x += dx * displacement
                        enemy_y += dy * displacement

                        # update position
                        Enemy.spawned_enemy_dict[enemy_name] = (enemy_info[0], enemy_x, enemy_y)

    def update(self):
        Enemy.detection(self)
        Enemy.move(self)
        Enemy.collision_with_entities()
        Enemy.despawn()
