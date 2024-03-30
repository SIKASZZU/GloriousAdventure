import random

from variables import UniversalVariables




class Enemy:

    def __init__(self) -> None:
        ...

    def spawn(self):
        """
        Spawns enemies based on certain conditions.
        """

        # Playeri gridi arvutamine
        player_x_row = int(UniversalVariables.player_x // UniversalVariables.block_size)
        player_y_col = int(UniversalVariables.player_y // UniversalVariables.block_size)
        player_grid = (player_y_col, player_x_row)

        distance_from_player = int(UniversalVariables.light_range / UniversalVariables.block_size)
        # light rangei ei spawni enemyt
        x = 0
        while x <= 5:
            enemy_spawn_location = random.choice(UniversalVariables.enemy_spawnpoint_list)
            # Kui enemy spawn on kaugemal, kui vision range (light_range).
            if (abs(player_grid[0] - enemy_spawn_location[0]) > distance_from_player or
                abs(player_grid[1] - enemy_spawn_location[1]) > distance_from_player):

                print()
                print("Enemy spawn location:", enemy_spawn_location)
                print("Player grid:", player_grid)
                print("Distance from player:", distance_from_player)
                print("X value:", x)

                # spawn mob.
                self.terrain_data[enemy_spawn_location[0]][enemy_spawn_location[1]] = 2
                x += 1

                    
            # spawn night 1 max 3, night 2 max 5, Maze count ka arvesse v6tta
            # yhes mazeis max 5 tykki



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