import random

from variables import UniversalVariables




class Enemy:

    spawned_enemy_list: dict = {}

    def spawn(self):
        """ Spawns enemies based on certain conditions. """

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
                Enemy.spawned_enemy_list[f'Enemy_{UniversalVariables.enemy_counter}'] = (spawn_point[0], spawn_point[1])
                self.terrain_data[spawn_point[0]][spawn_point[1]] = 2
                x += 1
                UniversalVariables.enemy_counter += 1

                # Limit to 5 spawns
                if x >= 5:
                    break

        print()
        print(Enemy.spawned_enemy_list)


    def despawn(self):
        ...


    def move(self):
        """
        Liikumine paremale, vasakule, yles, alla. Liigub playeri suunas, kui detected. Liigub ainult object idl 98
        """
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

#           
# 
#        
        #  self.terrain-data 98 liigub aind
        # vaatab self.terrain_data 98 

        # kiirus suureneb kui ainult yks koordinaat piedvalt muutub (x, y)
            # block sizina peab arvutama


    def detection(self):
        ... ### enemy peaks detectima playeri 5 blocki kauguselt


    def hit(self):
        ...