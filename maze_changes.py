import random
from variables import UniversalVariables
from update import EssentialsUpdate


def find_random_index_in_list_of_lists(grid_data, number, grid_name='block_maze'):
    occurrences = []
    
    # Assuming UniversalVariables.map_list contains the names of the grids in the same order as list_of_lists
    for y, sublist in enumerate(UniversalVariables.map_list):
        for x in sublist:
            print(y, x, 'INDEX', UniversalVariables.map_list)
            if x == grid_name:
                # TODO: grid data peaks olema ainult 40x40 ala, MITTE KOGU FKING TERRAIN DATA             


                grid_data = grid_data[2:-1]  # Remove first and last rows
                grid_data = [row[2:-1] for row in grid_data]  # Remove first and last columns from each remaining row

                # Find occurrences of the number in the grid
                for row_index, sublist in enumerate(grid_data):
                    for col_index, element in enumerate(sublist):
                        if element == number:
                            occurrences.append((col_index+1, row_index+1))  # Append tuple (row_index, col_index)
    
    # Return a random occurrence if found, otherwise return None
    if occurrences:
        return random.choice(occurrences)
    else:
        return None
    
    
class MazeChanges:

    times_changed: int = 0

    def change_maze(self):
        """ Muudab random maze pathwayisid (id 98) maze blockideks (id 99) ja vastupidi. """        

        # if EssentialsUpdate.day_night_text == 'Day':
        #     MazeChanges.times_changed = 0
        
        # # only change maze at night
        # else:
        if MazeChanges.times_changed > 155550:
            pass
        else:
            try:
                # peab olema mingi in range. Mingi min, max peaks olema 
                index_of_wall = find_random_index_in_list_of_lists(self.terrain_data, 99)
                if index_of_wall != None:  self.terrain_data[index_of_wall[0]][index_of_wall[1]] = 2
                index_of_pathway = find_random_index_in_list_of_lists(self.terrain_data, 98)
                if index_of_pathway != None:  self.terrain_data[index_of_pathway[0]][index_of_pathway[1]] = 2
                
                MazeChanges.times_changed += 1
            except Exception as ex: print(ex)