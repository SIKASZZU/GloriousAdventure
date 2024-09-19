import random
from variables import UniversalVariables
from update import EssentialsUpdate


def find_random_index_in_list_of_lists(list_of_lists, number, grid_name='block_maze'):
    occurrences = []
    
    # Assuming UniversalVariables.map_list contains the names of the grids in the same order as list_of_lists
    for index, grid in enumerate(UniversalVariables.map_list):
        if grid == grid_name:
            #grid_data = # nyyd siia vot peaks tulema selle leitud mazei data....
            
            # Optionally trim edges (remove first and last row/column)
            grid_data = grid_data[1:-1]  # Remove first and last rows
            grid_data = [row[1:-1] for row in grid_data]  # Remove first and last columns from each remaining row
            
            # Find occurrences of the number in the grid
            for row_index, sublist in enumerate(grid_data):
                for col_index, element in enumerate(sublist):
                    if element == number:
                        occurrences.append((row_index, col_index))  # Append tuple (row_index, col_index)
    
    # Return a random occurrence if found, otherwise return None
    if occurrences:
        return random.choice(occurrences)
    else:
        return None
    
    
class MazeChanges:

    times_changed: int = 0

    def change_maze(self):
        """ Muudab random maze pathwayisid (id 98) maze blockideks (id 99) ja vastupidi. """        

        if EssentialsUpdate.day_night_text == 'Day':
            MazeChanges.times_changed = 0
        
        # only change maze at night
        else:
            if MazeChanges.times_changed > 150:
                pass
            else:
                # peab olema mingi in range. Mingi min, max peaks olema 
                index_of_wall = find_random_index_in_list_of_lists(self.terrain_data, 99)
                self.terrain_data[index_of_wall[0]][index_of_wall[1]] = 98
                index_of_pathway = find_random_index_in_list_of_lists(self.terrain_data, 98)
                self.terrain_data[index_of_pathway[0]][index_of_pathway[1]] = 99
                
                MazeChanges.times_changed += 1
