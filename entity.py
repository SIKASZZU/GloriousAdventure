import camera
import random

import pygame

from variables import UniversalVariables
from update import EssentsialsUpdate
from images import ImageLoader


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

        if EssentsialsUpdate.day_night_text == 'Day':
            detected_enemies = {enemy_name for enemy_name, _ in Enemy.enemy_in_range}
            
            enemies_to_remove = set()

            for enemy_name, _ in Enemy.spawned_enemy_dict.items():
                if enemy_name not in detected_enemies:
                    print('f', enemy_name)
                    enemies_to_remove.add(enemy_name) # ei saa koheselt removeida, peab tegema uue listi

            for enemy_name in enemies_to_remove:
                del Enemy.spawned_enemy_dict[enemy_name]

            Enemy.enemy_in_range.clear()


    # TODO: pathfinding eraldi faili viia

    def is_valid(self, x, y):
        """ Check if coordinates (x, y) are valid in the maze. """

        return 0 <= x < len(self.terrain_data) and 0 <= y < len(self.terrain_data[x]) and self.terrain_data[x][y] != 99

    def find_path_bfs(self, start, end):
        """ Breadth-First Search algorithm to find a path from start to end in the maze. """
        from collections import deque

        queue = deque([(start, [])])
        print(queue)
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

            # If the enemy is in range of the player, move accordingly
            if direction:
                # Calculate the next position based on direction
                next_x, next_y = x, y
                if direction == 'right':
                    next_x += 0.03
                elif direction == 'left':
                    next_x -= 0.03
                elif direction == 'down':
                    next_y += 0.03
                elif direction == 'up':
                    next_y -= 0.03

                # If the enemy is not in range, move using pathfinding
                player_grid = (int(UniversalVariables.player_y // UniversalVariables.block_size), int(UniversalVariables.player_x // UniversalVariables.block_size))
                enemy_grid = (enemy_info[2], enemy_info[1])

                player_grid = (int(player_grid[0]), int(player_grid[1]))
                enemy_grid = (int(enemy_grid[0]), int(enemy_grid[1]))

                # Perform pathfinding
                path = Enemy.find_path_bfs(self, enemy_grid, player_grid)
                print('path', path)
                print('player grid', player_grid)
                print((int(enemy_grid[0]), int(enemy_grid[1])))

                if path:
                    # Move towards the next position in the path
                    next_node = path[0]  # Assuming the first node is the current position

                    # next_x = next_node[1] * UniversalVariables.block_size + UniversalVariables.offset_x - 250
                    # next_y = next_node[0] * UniversalVariables.block_size + UniversalVariables.offset_y - 250
                    print('entity next move:', next_x, next_y)
                    x = next_node[1]
                    y = next_node[0]


            else:
                # If no path found, move randomly
                direction = random.choice(['right', 'left', 'down', 'up'])
                next_x, next_y = x, y
                if direction == 'right':
                    next_x += 0.03
                elif direction == 'left':
                    next_x -= 0.03
                elif direction == 'down':
                    next_y += 0.03
                elif direction == 'up':
                    next_y -= 0.03
                x, y = next_x, next_y


            enemy_corner_set: set[tuple[float, float], ...] = set()
            enemy_width = enemy_info[0].get_width()
            enemy_height = enemy_info[0].get_height()

            block_size = UniversalVariables.block_size

            # Testib cornerid 2ra tuleviku koordinaatidega.
            # enemy_corner_set.add((next_x * block_size, next_y * block_size))                                  # Top-Left
            # enemy_corner_set.add((next_x * block_size + enemy_width, next_y * block_size))                    # Top-Right
            # enemy_corner_set.add((next_x * block_size, next_y * block_size + enemy_height))                   # Bottom-Left
            # enemy_corner_set.add((next_x * block_size + enemy_width, next_y * block_size + enemy_height))     # Bottom-Right
            
            # for next_cords in enemy_corner_set:
            #     new_grid_x, new_grid_y = int(next_cords[0] // block_size), int(next_cords[1] // block_size)
            #     if self.terrain_data[new_grid_y][new_grid_x] != 99 and \
            #         self.terrain_data[new_grid_y][new_grid_x] != 933 and \
            #         self.terrain_data[new_grid_y][new_grid_x] != 977:
            #         continue
            #     else:
            #         break
            # else:
            #     x, y = next_x, next_y
            print(Enemy.spawned_enemy_dict[enemy_name])
            print(Enemy.spawned_enemy_dict)
            Enemy.spawned_enemy_dict[enemy_name] = image, x, y


    def detection(self):
        player_window_x = camera.Camera.player_window_x
        player_window_y = camera.Camera.player_window_y

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

