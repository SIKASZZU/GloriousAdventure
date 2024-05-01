import pygame
from collections import deque

from camera import Camera
from images import ImageLoader
from update import EssentsialsUpdate
from variables import UniversalVariables


### TODO:
    # ghost collision
    # kui ghost on samal gridil mis player, v6i selle k6rval, ss hakkab koordinaatidega arvutama.


class Enemy:
    ghost_image = pygame.transform.scale(ImageLoader.load_sprite_image("Ghost"), (UniversalVariables.block_size // 1.5, UniversalVariables.block_size // 1.5))
    spawned_enemy_dict: dict[str, tuple[pygame.Surface, int, int]] = {}  # (Enemy_image, y, x)
    enemy_in_range: set[tuple[str, str]] = set()

    damage_delay: int = 30

    def spawn(self):
        """ Spawns enemies based on certain conditions. """

        if not Enemy.spawned_enemy_dict and EssentsialsUpdate.day_night_text == 'Night':
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
                    if UniversalVariables.maze_counter == 1: max_enenmy = 1  # Kui on ainult 1 maze siis spawnib max 2 enemit
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

        if EssentsialsUpdate.day_night_text == 'Day':
            detected_enemies = {enemy_name for enemy_name, _ in Enemy.enemy_in_range}
            
            enemies_to_remove = set()

            for enemy_name, _ in Enemy.spawned_enemy_dict.items():
                if enemy_name not in detected_enemies:
                    enemies_to_remove.add(enemy_name) # ei saa koheselt removeida, peab tegema uue listi

            for enemy_name in enemies_to_remove:
                del Enemy.spawned_enemy_dict[enemy_name]

            Enemy.enemy_in_range.clear()


    # TODO: pathfinding eraldi faili viia
    def is_valid(self, x, y):
            """ Check if coordinates (x, y) are valid in the maze. """
            x, y = int(x), int(y)

            return 0 <= x < len(self.terrain_data) and 0 <= y < len(self.terrain_data[x]) and self.terrain_data[x][y] != 99


    def find_path_bfs(self, start, end):
        """ Breadth-First Search algorithm to find a path from start to end in the maze. """

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
    


    def move(self):
        """ Move enemies based on their individual decisions."""
    
        for enemy_name, enemy_info in Enemy.spawned_enemy_dict.items():
            image, x, y = enemy_info
            direction = None
    
            for enemy_name_, dir_ in Enemy.enemy_in_range:
                if enemy_name == enemy_name_:
                    direction = dir_
                    break
                
            # finds path, looks with grids
            player_grid = (int(UniversalVariables.player_y // UniversalVariables.block_size), int(UniversalVariables.player_x // UniversalVariables.block_size))
            print(x, y)
            enemy_grid = (int(y), int(x))
            print('rounded,', enemy_grid)
            
            path = Enemy.find_path_bfs(self, enemy_grid, player_grid)
            print(path)
            
            if path:
                next_grid = ((path[0][1] - enemy_grid[1]) , (path[0][0] - enemy_grid[0]))  # Calculate position of next grid to determine to direction of entity's movement
                print('next_grid', next_grid)
                if direction:

                    # direction peab olema arvutatud järgmise pathfinder gridi järgi
                    next_x, next_y = x, y
                    if next_grid[0] == 1: 
                        next_x += 0.03

                    elif next_grid[0] == -1: 
                        next_x -= 0.03

                    elif next_grid[1] == 1: 
                        next_y += 0.03

                    elif next_grid[1] == -1: 
                        next_y -= 0.03

                    print('ghost', enemy_grid)
                    Enemy.spawned_enemy_dict[enemy_name] = image, next_x, next_y
                    print('player', player_grid)
                print()


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

                if abs(distance_to_player_x_grid) < UniversalVariables.block_size * 0.75 and abs(distance_to_player_y_grid) < UniversalVariables.block_size * 0.75:
                    Enemy.attack(self, 3)

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


    def attack(self, damage):
        """ Kui Ghost on playeri peal siis saab damage'i. """
        
        if Enemy.damage_delay >= 60:
            self.player.health.damage(damage)
            Enemy.damage_delay = 0
        Enemy.damage_delay += 1


    def update(self):
        Enemy.detection(self)
        Enemy.move(self)
        Enemy.despawn()

