import pygame

from variables import UniversalVariables
from update import EssentsialsUpdate
from images import ImageLoader

ghost_image = pygame.transform.scale(ImageLoader.load_sprite_image("Ghost"), (UniversalVariables.block_size, UniversalVariables.block_size))


class Enemy:
    spawned_enemy_dict: dict[str, tuple[pygame.Surface, int, int]] = {}  # (Enemy_image, y, x)

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
                    Enemy.spawned_enemy_dict[f'Enemy_{UniversalVariables.enemy_counter}'] = ghost_image, spawn_point[1], \
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

            UniversalVariables.screen.blit(pygame.transform.scale(enemy[0], (UniversalVariables.block_size, UniversalVariables.block_size)), (enemy_x, enemy_y))

    @staticmethod
    def despawn(self):
        # {'Enemy_0': (26, 21),
        if EssentsialsUpdate.day_night_text == 'Day':
            Enemy.spawned_enemy_dict: dict[str, tuple[pygame.Surface, int, int]] = {}  # resetting list of enemies (Enemy_image, y, x)
            UniversalVariables.enemy_spawnpoint_list = set()
            UniversalVariables.enemy_counter = 0

    def move(self):
        """ Liikumine paremale, vasakule, yles, alla. Liigub playeri suunas, kui detected. Liigub ainult object idl 98. """

        def calculate_next_step(current_position, next_position):
            if next_position == 'right': next_step = (1, 0)  # +1
            if next_position == 'left': next_step = (-1, 0)  # -1
            if next_position == 'top': next_step = (0, -1) 
            if next_position == 'down': next_step = (0, 1)


            ''' next position on suund, mitte koordinaat. left, right, up, down. '''
            for enemy in Enemy.spawned_enemy_dict.values():
                if enemy[1][2] == current_position:
                    enemy[1][2] 

        # funk, et arvutada kiirendus kummitusele.
        def calculate_speed(x1, y1, x2, y2, default_speed, block_size):
            if (x2 - x1) != 0 and (y2 - y1) != 0:  # If movement is along both axes
                return default_speed
            else:
                # Calculate number of blocks moved in each axis
                blocks_moved_x = abs(x2 - x1) / block_size
                blocks_moved_y = abs(y2 - y1) / block_size
                # Speed increases by the total number of blocks moved in both axes
                return default_speed + blocks_moved_x + blocks_moved_y

        
        # detectioni peale hakkab liikuma
        if self.direction != 'none': 
            for enemy in Enemy.spawned_enemy_dict.values():
                current_position = (enemy[1], enemy[2])
                calculate_next_step(current_position, self.direction)
        


        # hakkab liikuma oma rutiinset sitta, yles alla paremale vasakule
        block_size = UniversalVariables.block_size
        x = abs(x)
        if x - block_size > x < x + block_size:
            # do that
            ...


    def detection(self):
        block_size = UniversalVariables.block_size
        player_x = UniversalVariables.player_x
        player_y = UniversalVariables.player_y

        for enemy_name, enemy_info in Enemy.spawned_enemy_dict.items():
            enemy_x, enemy_y = enemy_info[1], enemy_info[2]

            player_x_grid = int(player_x // block_size)
            player_y_grid = int(player_y // block_size)
            
            dx = player_x_grid - enemy_x
            dy = player_y_grid - enemy_y
            
            distance_to_player_x_grid = abs(player_x_grid - enemy_x)
            distance_to_player_y_grid = abs(player_y_grid - enemy_y)

            if abs(distance_to_player_x_grid) <= 10 and abs(distance_to_player_y_grid) <= 10:

                # Update direction
                if abs(dx) == abs(dy):
                    print('ontop')   # vb peab olema pass, player dead

                elif abs(dx) > abs(dy):
                    if dx > 0:
                        self.direction = 'right'
                        print('right')
                    else:
                        self.direction = 'left'
                        print('left')
                else:
                    if dy > 0:
                        self.direction = 'down'
                        print('down')
                    else:
                        self.direction = 'up'
                        print('up')
            else:
                self.direction = 'none'

    def attack(self):
        ...

    def update(self):
        Enemy.spawn(self)
        Enemy.detection(self)
        Enemy.despawn(self)
