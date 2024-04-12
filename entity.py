import random

from variables import UniversalVariables
from update import EssentsialsUpdate 




class Enemy:

    spawned_enemy_dict: dict = {}

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
            x = 0

            for spawn_point in UniversalVariables.enemy_spawnpoint_list:
                # Check if the spawn point is far enough from the player
                if (abs(player_grid[0] - spawn_point[0]) > distance_from_player or
                        abs(player_grid[1] - spawn_point[1]) > distance_from_player):

                    # Spawn an enemy
                    Enemy.spawned_enemy_dict[f'Enemy_{UniversalVariables.enemy_counter}'] = (spawn_point[0], spawn_point[1])
                    self.terrain_data[spawn_point[0]][spawn_point[1]] = 2
                    x += 1
                    UniversalVariables.enemy_counter += 1

                    # Limit to 5 spawns
                    if x >= (5*UniversalVariables.maze_counter):
                        break


    def despawn(self):
        # {'Enemy_0': (26, 21),
        if EssentsialsUpdate.day_night_text == 'Day':
            for key, value in Enemy.spawned_enemy_dict.items():
                self.terrain_data[value[0]][value[1]] = 98
            Enemy.spawned_enemy_dict: dict = {}
            UniversalVariables.enemy_spawnpoint_list = set()
            UniversalVariables.enemy_counter = 0
            print('despawned Enemy')


    def move(self):
        """ Liikumine paremale, vasakule, yles, alla. Liigub playeri suunas, kui detected. Liigub ainult object idl 98. """

        # Function to calculate speed based on movement
        def calculate_speed(x1, y1, x2, y2, default_speed, block_size):
            if (x2 - x1) != 0 and (y2 - y1) != 0:  # If movement is along both axes
                return default_speed
            else:
                # Calculate number of blocks moved in each axis
                blocks_moved_x = abs(x2 - x1) / block_size
                blocks_moved_y = abs(y2 - y1) / block_size
                # Speed increases by the total number of blocks moved in both axes
                return default_speed + blocks_moved_x + blocks_moved_y

        block_size = UniversalVariables.block_size
        x = abs(x)


        if x - block_size > x < x + block_size:
            # do that
            ...


    def detection(self):
        ... ### enemy peaks detectima playeri 5 blocki kauguselt


    def hit(self):
        ...


    def update(self):
        Enemy.spawn(self)
        print('Enemy.spawned_enemy_dict', Enemy.spawned_enemy_dict)
        Enemy.despawn(self)
