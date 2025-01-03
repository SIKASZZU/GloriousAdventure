import pygame
import math
from collections import deque

from functions import UniversalFunctions
import random

class Entity:
    def __init__(self, td, cam, pupdate, ess, player, peffect, inv, image_loader, o_management, variables, ALL_THE_DOORS, GLADE_ITEMS):  # ma ei viitsi enam kirjutada .. lyhendatud ver nimetustest
        self.terrain_data = td
        self.player_update = pupdate
        self.essentials = ess
        self.camera = cam
        self.player = player
        self.player_effect = peffect
        self.inv = inv
        self.image_loader = image_loader
        self.object_management = o_management
        self.variables = variables
        self.ALL_THE_DOORS = ALL_THE_DOORS
        self.GLADE_ITEMS = GLADE_ITEMS

        self.ghost_image      = pygame.transform.scale(self.image_loader.load_sprite_image("Ghost"),
            (self.variables.block_size // 1.5, self.variables.block_size // 1.5))
        self.ghost_dead_image = pygame.transform.scale(self.image_loader.load_sprite_image("Ghost_Dead"),
            (self.variables.block_size // 1.5, self.variables.block_size // 1.5))
        self.ghost_dead_geiger_image = pygame.transform.scale(self.image_loader.load_sprite_image("Ghost_Dead_Geiger"),
            (self.variables.block_size // 1.5, self.variables.block_size // 1.5))

        self.spawned_entity_dict: dict[str, tuple[pygame.Surface, int, int, float]] = {}  # (entity_image, y, x, HP)
        self.entity_in_range: set[tuple[str, str]] = set()
        self.dead_entity_list: dict[str] = {}

        self.damage_delay: int = 50  # esimese hiti jaoks, et esimene hit oleks kiirem kui teised
        self.path_ticks = {}
        self.path = {}
        self.save_entity_direction_x = int
        self.save_entity_direction_y = int

        self.entity_restricted_areas = [99, 981, 982,  # maze wall stuff
                                      9099, 989, 900]  # blade wall stuff
        self.combined_restricted_areas = set(self.entity_restricted_areas).union(set(self.ALL_THE_DOORS.value))
        self.combined_restricted_areas = set(self.combined_restricted_areas).union(set(self.GLADE_ITEMS.value))

    def spawn(self):
        """ Spawns enemies based on certain conditions. """

        if not self.spawned_entity_dict and self.essentials.day_night_text == 'Night':
            entity_spawnpoint_list = UniversalFunctions.find_spawnpoints_in_map_data(self, self.terrain_data)

            # Player grid calculation
            player_x_row = int(self.variables.player_x // self.variables.block_size)
            player_y_col = int(self.variables.player_y // self.variables.block_size)
            player_grid = (player_y_col, player_x_row)

            distance_from_player = int(self.variables.light_range / self.variables.block_size)

            # Count of spawned enemies
            spawned_entity_count = 0

            for spawn_point in entity_spawnpoint_list:
                # Check if the spawn point is far enough from the player
                if (abs(player_grid[0] - spawn_point[0]) > distance_from_player or
                        abs(player_grid[1] - spawn_point[1]) > distance_from_player):

                    # Spawn an entity
                    self.spawned_entity_dict[f'entity_{self.variables.entity_counter}'] = self.ghost_image, \
                        spawn_point[1], spawn_point[0], self.variables.ghost_hp

                    spawned_entity_count += 1
                    self.variables.entity_counter += 1

                    # Limiteerib Enemite arvu vastvalt maze_counterile
                    max_enenmy = 5 * self.variables.maze_counter
                    if self.variables.maze_counter == 1: max_enenmy = 2  # Kui on ainult 1 maze siis spawnib max 2 enemit
                    if spawned_entity_count >= max_enenmy:
                        break

        # spawn alive enemies
        entity_blits_list = []
        for entity in self.spawned_entity_dict.values():
            entity_x = entity[1] * self.variables.block_size + self.variables.offset_x
            entity_y = entity[2] * self.variables.block_size + self.variables.offset_y
            entity_blits_list.append((entity[0], (entity_x, entity_y)))

        # spawn dead enemies
        for entity in self.dead_entity_list.values():
            entity_x = entity[0] * self.variables.block_size + self.variables.offset_x
            entity_y = entity[1] * self.variables.block_size + self.variables.offset_y
            
            image = self.ghost_dead_image
            if entity[2] == True:  image = self.ghost_dead_geiger_image
            entity_blits_list.append((image, (entity_x, entity_y)))

        self.variables.screen.blits(entity_blits_list, doreturn=False)

    def despawn(self):
        """ Despawns enemies during the day.  """
        """ Doesn't despawn detected enemies. """

        if self.essentials.day_night_text == 'Day':
            detected_enemies = {entity_name for entity_name, _ in self.entity_in_range}
            enemies_to_remove = set()

            for entity_name, _ in self.spawned_entity_dict.items():
                if entity_name not in detected_enemies or self.path[entity_name] is None:
                    enemies_to_remove.add(entity_name)  # Add to the list of enemies to remove

            for entity_name in list(enemies_to_remove):
                if entity_name in self.path:
                    del self.path[entity_name]
                del self.spawned_entity_dict[entity_name]
            

            self.entity_in_range.clear()

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
        
        if in_terrain_bounds and self.terrain_data[x][y] not in self.combined_restricted_areas:
            return True
            
    def find_path_bfs(self, start, end):
        """ Breadth-First Search algorithm with randomness to create more natural AI movement. """

        try:
            # Check if the player is in a restricted area
            if self.terrain_data[int(self.player_update.player_rect.center[1] // self.variables.block_size)][int(self.player_update.player_rect.center[0] // self.variables.block_size)] in self.combined_restricted_areas:
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
                            if self.is_valid(new_x, new_y):
                                new_path = path + [(new_x, new_y)]

                                # Add randomness to enqueue order
                                if random.random() > 0.3:  # 70% chance to follow this path
                                    queue.append(((new_x, new_y), new_path))
                                else:
                                    queue.appendleft(((new_x, new_y), new_path))

                return None
        except IndexError:
            pass

    def move(self):
        """ Move enemies based on their individual decisions."""

        entity_speed = self.variables.entity_speed

        for entity_name, entity_info in self.spawned_entity_dict.items():
            image, x, y, HP = entity_info
            direction = None

            # Check if the player is in range
            for entity_name_, dir_ in self.entity_in_range:
                if entity_name == entity_name_:
                    direction = dir_
                    break
            if direction:
                entity_grid = (self.custom_round(entity_info[2]), self.custom_round(entity_info[1]))
                player_grid = (self.custom_round(self.player_update.player_rect.centery // self.variables.block_size),
                                self.custom_round(self.player_update.player_rect.centerx // self.variables.block_size))

                if entity_name not in self.path or self.path_ticks[
                    entity_name] >= self.variables.entity_path_update_tick:

                    path = self.find_path_bfs(entity_grid, player_grid)

                    self.path[entity_name] = path
                    self.path_ticks[entity_name] = 0

                next_x, next_y = x, y
                if self.path[entity_name] is not None and len(self.path[entity_name]) > 0:  # enemil on path playerini olemas
                    next_grid = self.path[entity_name][0]

                    if (entity_grid[0], entity_grid[1]) == (next_grid[0], next_grid[1]):
                        self.path[entity_name].pop(0)  # Remove the first element if the entity has reached it

                    if len(self.path[entity_name]) > 0:
                        # Otsib playerit grididega
                        next_grid = ((self.path[entity_name][0][1] - entity_grid[1]), (self.path[entity_name][0][0] - entity_grid[0]))

                        # Move entity based on the next grid
                        next_x += (next_grid[0] * entity_speed)
                        next_y += (next_grid[1] * entity_speed)
                
                elif entity_grid == player_grid:  # playeri ja mangija grid on smad
                    # Otsib playerit koordinaatidega
                    if direction == 'right':
                        next_x += entity_speed
                    elif direction == 'left':
                        next_x -= entity_speed
                    elif direction == 'down':
                        next_y += entity_speed
                    elif direction == 'up':
                        next_y -= entity_speed

                next_x, next_y = round(next_x, 3), round(next_y, 3)  # performance gain
            
                # Adjust entity position to avoid moving through walls
                if next_x == x and next_y != y and str(next_x).endswith('.5'):
                    next_x = math.ceil(next_x)
                if next_y == y and next_x != x and str(next_y).endswith('.5'):
                    next_y = math.ceil(next_y)                        

                self.spawned_entity_dict[entity_name] = image, next_x, next_y, HP

                # Increment path ticks
                if entity_name in self.path_ticks:
                    self.path_ticks[entity_name] += 1

    def detection(self):
        player_window_x = self.camera.player_window_x
        player_window_y = self.camera.player_window_y

        if self.variables.player_sprinting: detect_range = 25 * self.variables.block_size
        elif self.variables.player_sneaking:  detect_range = 5 * self.variables.block_size
        elif self.variables.player_standing:  detect_range = 3 * self.variables.block_size
        else: detect_range = 10 * self.variables.block_size

        self.entity_in_range = set()

        for entity_name, entity_info in self.spawned_entity_dict.items():
            entity_x_grid, entity_y_grid = entity_info[1], entity_info[2]

            entity_x = entity_x_grid * self.variables.block_size + self.variables.offset_x
            entity_y = entity_y_grid * self.variables.block_size + self.variables.offset_y

            distance_to_player_x_grid = player_window_x - entity_x
            distance_to_player_y_grid = player_window_y - entity_y
                
            if abs(distance_to_player_x_grid) <= detect_range and abs(distance_to_player_y_grid) <= detect_range:
                direction: str = 'none'

                if abs(distance_to_player_x_grid) < self.variables.block_size * 0.75 \
                    and abs(distance_to_player_y_grid) < self.variables.block_size * 0.75:
                    if self.player.health.get_health() > 0:
                        self.attack(3, entity_x, entity_y)

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
                self.entity_in_range.add((entity_name, direction))

    def attack(self, damage, entity_direct_x, entity_direct_y):
        """ Kui Ghost on playeri peal siis saab damage'i. """
        
        if self.damage_delay == 50:
            self.save_entity_direction_x = entity_direct_x
            self.save_entity_direction_y = entity_direct_y

        if self.damage_delay >= 60:

            if not self.variables.player_bleeding and random.randint(1, 10) <= 6:
                self.variables.player_bleeding = True

            if not self.variables.player_infected and random.randint(1, 10) <= 3:
                self.variables.player_infected = True

            self.player.health.damage(damage)
            self.player_effect.infection()
            self.player_effect.bleed()

            # Calculate knockback direction
            dx = self.camera.player_window_x - self.save_entity_direction_x
            dy = self.camera.player_window_y - self.save_entity_direction_y

            if dx == 0 and dy == 0:
                dx = random.uniform(-1, 1)
                dy = random.uniform(-1, 1)

            distance = (dx ** 2 + dy ** 2) ** 0.5
            dx /= distance
            dy /= distance

            self.player.apply_knockback(dx, dy)

            self.damage_delay = 0
        self.damage_delay += 1

    def collision_with_entities(self):
        for entity_name, entity_info in list(self.spawned_entity_dict.items()):
            entity_rect = pygame.Rect(entity_info[1] * self.variables.block_size,
                                     entity_info[2] * self.variables.block_size, 73, 73)

            # Check for collisions between enemies
            for other_entity_name, other_entity_info in list(self.spawned_entity_dict.items()):
                if entity_name != other_entity_name:
                    other_entity_rect = pygame.Rect(other_entity_info[1] * self.variables.block_size,
                                                   other_entity_info[2] * self.variables.block_size, 73, 73)
                    if entity_rect.colliderect(other_entity_rect):
                        entity_x = entity_info[1]
                        entity_y = entity_info[2]
                        
                        other_entity_x = other_entity_info[1]
                        other_entity_y = other_entity_info[2]

                        # Calculate displacement vector
                        dx = entity_x - other_entity_x
                        dy = entity_y - other_entity_y

                        if dx == 0 and dy == 0:
                            dx = random.uniform(-1, 1)
                            dy = random.uniform(-1, 1)

                        # Normalize the displacement vector
                        distance = (dx ** 2 + dy ** 2) ** 0.5
                        dx /= distance
                        dy /= distance

                        # Move the entity along the displacement vector
                        displacement = 3.0  # See kontrollib, kaugele ta tagasi t6rjutakse
                        entity_x += dx * displacement
                        entity_y += dy * displacement

                        # update position
                        self.spawned_entity_dict[entity_name] = (entity_info[0], entity_x, entity_y, entity_info[3])

    def loot(self):
        """ Loot geiger from ghost! Nothing else atm. """

        def collect_geiger(click=None, press=None):
            for entity_name, entity_info in self.dead_entity_list.items():
                if_geiger = entity_info[2]
                if not if_geiger:
                    continue

                entity_dead_grid = (int(entity_info[0]), int(entity_info[1]))
                
                # vaatab self.camera.click_positioni j2rgi kas click toimus ja ss kasutab kamera clicki edasi et leida clicki grid
                if click and if_geiger:
                    grid = self.camera.click_on_screen_to_grid(self.camera.click_x, self.camera.click_y)
                    grid = (grid[1], grid[0])  # p66ran ymber need v22rtused sest mdea watafak :D
                    if grid != entity_dead_grid:
                        continue  # GOOD

                elif press and if_geiger:
                    if press != entity_dead_grid:
                        continue  # GOOD
                            
                self.dead_entity_list[entity_name] = (entity_info[0], entity_info[1], False)
                self.object_management.add_object_from_inv("Geiger", 1)

        # spacebar
        keys = pygame.key.get_pressed()  # Jälgib keyboard inputte
        if keys[pygame.K_SPACE]:
            x = self.variables.player_x // self.variables.block_size
            y = self.variables.player_y // self.variables.block_size
            collect_geiger(press=(x, y))

        # click
        if self.camera.right_click_position:
            collect_geiger(click=self.camera.click_position)

    def update(self):
        self.detection()
        self.move()
        self.collision_with_entities()
        self.loot()
        self.despawn()
