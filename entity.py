import pygame
import math
from collections import deque

from camera import Camera
from images import ImageLoader
from update import EssentialsUpdate
from variables import UniversalVariables, GameConfig
from status import PlayerStatus
from objects import ObjectManagement
import random

class Enemy:
    ghost_image      = pygame.transform.scale(ImageLoader.load_sprite_image("Ghost"),
        (UniversalVariables.block_size // 1.5, UniversalVariables.block_size // 1.5))
    ghost_dead_image = pygame.transform.scale(ImageLoader.load_sprite_image("Ghost_Dead"),
        (UniversalVariables.block_size // 1.5, UniversalVariables.block_size // 1.5))
    ghost_dead_geiger_image = pygame.transform.scale(ImageLoader.load_sprite_image("Ghost_Dead_Geiger"),
        (UniversalVariables.block_size // 1.5, UniversalVariables.block_size // 1.5))

    spawned_enemy_dict: dict[str, tuple[pygame.Surface, int, int, float]] = {}  # (Enemy_image, y, x, HP)
    enemy_in_range: set[tuple[str, str]] = set()
    dead_enemy_list: dict[str] = {}

    damage_delay: int = 50  # esimese hiti jaoks, et esimene hit oleks kiirem kui teised
    path_ticks = {}
    path = {}
    save_enemy_direction_x = int
    save_enemy_direction_y = int

    enemy_restricted_areas = [99, 981, 982,  # maze wall stuff
                            9099, 989, 900]  # blade wall stuff
    combined_restricted_areas = set(enemy_restricted_areas).union(set(GameConfig.ALL_THE_DOORS.value))
    combined_restricted_areas = set(combined_restricted_areas).union(set(GameConfig.GLADE_ITEMS.value))

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
                        spawn_point[1], spawn_point[0], UniversalVariables.ghost_hp

                    spawned_enemy_count += 1
                    UniversalVariables.enemy_counter += 1

                    # Limiteerib Enemite arvu vastvalt maze_counterile
                    max_enenmy = 5 * UniversalVariables.maze_counter
                    if UniversalVariables.maze_counter == 1: max_enenmy = 2  # Kui on ainult 1 maze siis spawnib max 2 enemit
                    if spawned_enemy_count >= max_enenmy:
                        break

        # spawn alive enemies
        enemy_blits_list = []
        for enemy in Enemy.spawned_enemy_dict.values():
            enemy_x = enemy[1] * UniversalVariables.block_size + UniversalVariables.offset_x
            enemy_y = enemy[2] * UniversalVariables.block_size + UniversalVariables.offset_y
            enemy_blits_list.append((enemy[0], (enemy_x, enemy_y)))

        # spawn dead enemies
        for enemy in Enemy.dead_enemy_list.values():
            enemy_x = enemy[0] * UniversalVariables.block_size + UniversalVariables.offset_x
            enemy_y = enemy[1] * UniversalVariables.block_size + UniversalVariables.offset_y
            
            image = Enemy.ghost_dead_image
            if enemy[2] == True:  image = Enemy.ghost_dead_geiger_image
            enemy_blits_list.append((image, (enemy_x, enemy_y)))

        UniversalVariables.screen.blits(enemy_blits_list, doreturn=False)

    @staticmethod
    def despawn():
        """ Despawns enemies during the day.  """
        """ Doesn't despawn detected enemies. """

        if EssentialsUpdate.day_night_text == 'Day':
            detected_enemies = {enemy_name for enemy_name, _ in Enemy.enemy_in_range}
            enemies_to_remove = set()

            for enemy_name, _ in Enemy.spawned_enemy_dict.items():
                if enemy_name not in detected_enemies or Enemy.path[enemy_name] is None:
                    enemies_to_remove.add(enemy_name)  # Add to the list of enemies to remove

            for enemy_name in list(enemies_to_remove):
                if enemy_name in Enemy.path:
                    del Enemy.path[enemy_name]
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
        """ Breadth-First Search algorithm with randomness to create more natural AI movement. """

        try:
            # Check if the player is in a restricted area
            if self.terrain_data[int(self.player_rect.center[1] // UniversalVariables.block_size)][int(self.player_rect.center[0] // UniversalVariables.block_size)] in Enemy.combined_restricted_areas:
                return None
            else:
                queue = deque([(start, [])])
                visited = set()

                # Define primary directions and shuffle them for randomness
                base_directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
                directions = base_directions.copy()
                random.shuffle(directions)

                while queue:
                    (x, y), path = queue.popleft()

                    # If the current position is the target, return the path
                    if (x, y) == end:
                        return path

                    if (x, y) not in visited:
                        visited.add((x, y))

                        # Randomly shuffle directions at each step for less predictability
                        random.shuffle(directions)

                        for dx, dy in directions:
                            new_x, new_y = x + dx, y + dy
                            if Enemy.is_valid(self, new_x, new_y):
                                new_path = path + [(new_x, new_y)]

                                # Add randomness to enqueue order
                                if random.random() > 0.3:  # 70% chance to follow this path
                                    queue.append(((new_x, new_y), new_path))
                                else:
                                    queue.appendleft(((new_x, new_y), new_path))

                return None
        except IndexError:
            pass

    @staticmethod
    def move(self):
        """ Move enemies based on their individual decisions."""

        enemy_speed = UniversalVariables.enemy_speed

        for enemy_name, enemy_info in Enemy.spawned_enemy_dict.items():
            image, x, y, HP = enemy_info
            direction = None

            # Check if the player is in range
            for enemy_name_, dir_ in Enemy.enemy_in_range:
                if enemy_name == enemy_name_:
                    direction = dir_
                    break
            if direction:
                enemy_grid = (Enemy.custom_round(enemy_info[2]), Enemy.custom_round(enemy_info[1]))
                player_grid = (Enemy.custom_round(self.player_rect.centery // UniversalVariables.block_size),
                                Enemy.custom_round(self.player_rect.centerx // UniversalVariables.block_size))

                if enemy_name not in Enemy.path or Enemy.path_ticks[
                    enemy_name] >= UniversalVariables.enemy_path_update_tick:

                    path = Enemy.find_path_bfs(self, enemy_grid, player_grid)

                    Enemy.path[enemy_name] = path
                    Enemy.path_ticks[enemy_name] = 0

                next_x, next_y = x, y
                if Enemy.path[enemy_name] is not None and len(Enemy.path[enemy_name]) > 0:  # enemil on path playerini olemas
                    next_grid = Enemy.path[enemy_name][0]

                    if (enemy_grid[0], enemy_grid[1]) == (next_grid[0], next_grid[1]):
                        Enemy.path[enemy_name].pop(0)  # Remove the first element if the enemy has reached it

                    if len(Enemy.path[enemy_name]) > 0:
                        # Otsib playerit grididega
                        next_grid = ((Enemy.path[enemy_name][0][1] - enemy_grid[1]), (Enemy.path[enemy_name][0][0] - enemy_grid[0]))

                        # Move enemy based on the next grid
                        next_x += (next_grid[0] * enemy_speed)
                        next_y += (next_grid[1] * enemy_speed)
                
                elif enemy_grid == player_grid:  # playeri ja mangija grid on smad
                    # Otsib playerit koordinaatidega
                    if direction == 'right':
                        next_x += enemy_speed
                    elif direction == 'left':
                        next_x -= enemy_speed
                    elif direction == 'down':
                        next_y += enemy_speed
                    elif direction == 'up':
                        next_y -= enemy_speed

                next_x, next_y = round(next_x, 3), round(next_y, 3)  # performance gain
            
                # Adjust entity position to avoid moving through walls
                if next_x == x and next_y != y and str(next_x).endswith('.5'):
                    next_x = math.ceil(next_x)
                if next_y == y and next_x != x and str(next_y).endswith('.5'):
                    next_y = math.ceil(next_y)                        

                Enemy.spawned_enemy_dict[enemy_name] = image, next_x, next_y, HP

                # Increment path ticks
                if enemy_name in Enemy.path_ticks:
                    Enemy.path_ticks[enemy_name] += 1

    def detection(self):
        player_window_x = Camera.player_window_x
        player_window_y = Camera.player_window_y

        if UniversalVariables.player_sprinting: detect_range = 25 * UniversalVariables.block_size
        elif UniversalVariables.player_sneaking:  detect_range = 5 * UniversalVariables.block_size
        else: detect_range = 10 * UniversalVariables.block_size

        Enemy.enemy_in_range = set()

        for enemy_name, enemy_info in Enemy.spawned_enemy_dict.items():
            enemy_x_grid, enemy_y_grid = enemy_info[1], enemy_info[2]

            enemy_x = enemy_x_grid * UniversalVariables.block_size + UniversalVariables.offset_x
            enemy_y = enemy_y_grid * UniversalVariables.block_size + UniversalVariables.offset_y

            distance_to_player_x_grid = player_window_x - enemy_x
            distance_to_player_y_grid = player_window_y - enemy_y
                
            if abs(distance_to_player_x_grid) <= detect_range and abs(distance_to_player_y_grid) <= detect_range:
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

            if not UniversalVariables.player_bleeding and random.randint(1, 10) <= 6:
                UniversalVariables.player_bleeding = True

            if not UniversalVariables.player_infected and random.randint(1, 10) <= 3:
                UniversalVariables.player_infected = True

            self.player.health.damage(damage)
            PlayerStatus.infection(self)
            PlayerStatus.bleed(self)


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

    @staticmethod
    def collision_with_entities(self):
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
                        Enemy.spawned_enemy_dict[enemy_name] = (enemy_info[0], enemy_x, enemy_y, enemy_info[3])

    def loot(self):
        """ Loot geiger from ghost! Nothing else atm. """

        def collect_geiger(click=False, press=False):
            for enemy_name, enemy_info in Enemy.dead_enemy_list.items():
                if_geiger = enemy_info[2]
                if not if_geiger:
                    continue

                enemy_dead_grid = (int(enemy_info[0]), int(enemy_info[1]))
                
                # vaatab self.click_positioni j2rgi kas click toimus ja ss kasutab kamera clicki edasi et leida clicki grid
                if click and if_geiger:
                    grid = Camera.click_on_screen_to_grid(Camera.click_x, Camera.click_y)
                    grid = (grid[1], grid[0])  # p66ran ymber need v22rtused sest mdea watafak :D
                    if grid != enemy_dead_grid:
                        continue  # GOOD

                elif press and if_geiger:
                    if press != enemy_dead_grid:
                        continue  # GOOD
                            
                Enemy.dead_enemy_list[enemy_name] = (enemy_info[0], enemy_info[1], False)
                ObjectManagement.add_object_from_inv("Geiger", 1)

        # spacebar
        keys = pygame.key.get_pressed()  # Jälgib keyboard inputte
        if keys[pygame.K_SPACE]:
            x = UniversalVariables.player_x // UniversalVariables.block_size
            y = UniversalVariables.player_y // UniversalVariables.block_size
            collect_geiger(press=(x, y))

        # click
        if self.click_position:
            collect_geiger(click=self.click_position)

    def update(self):
        Enemy.detection(self)
        Enemy.move(self)
        Enemy.collision_with_entities(self)
        Enemy.loot(self)
        Enemy.despawn()
