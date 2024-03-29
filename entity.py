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
        while True:
            enemy_spawn_location = random.choice(UniversalVariables.enemy_spawnpoint_list)

            if (abs(player_grid[0] - enemy_spawn_location[0]) > distance_from_player or
                abs(player_grid[1] - enemy_spawn_location[1]) > distance_from_player):
                
                print(x)
                # spawn mob.
                if x < 5:
                    self.terrain_data[enemy_spawn_location[0]][enemy_spawn_location[1]] = 2
                    x += 1 
                else:
                    break
    

                    
            # spawn night 1 max 3, night 2 max 5, Maze count ka arvesse v6tta
            # yhes mazeis max 5 tykki



    def despawn(self):
        ...


    def move(self):
        """
        Liikumine paremale, vasakule, yles, alla. Liigub playeri suunas, kui detected. Liigub ainult object idl 98
        """

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

# Example usage
mob_position_x = 0
mob_position_y = 0
mob_new_position_x = 0
mob_new_position_y = 1
default_speed = 10
block_size = 20

speed = calculate_speed(mob_position_x, mob_position_y, mob_new_position_x, mob_new_position_y, default_speed, block_size)
print("Mob Speed:", speed)