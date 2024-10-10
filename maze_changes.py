import random
from variables import UniversalVariables
from update import EssentialsUpdate


def find_random_index_in_list_of_lists(grid_data, number, grid_name='block_maze'):
    occurrences = []
    
    # Assuming UniversalVariables.map_list contains the names of the grids in the same order as list_of_lists
    for y, sublist in enumerate(UniversalVariables.map_list):
        for x, value in enumerate(sublist):
            print()
            print(x,y, value, 'INDEX', UniversalVariables.map_list[y][x])
            for row in UniversalVariables.map_list: print(row)
            print()
            print()

            if grid_name == UniversalVariables.map_list[y][x]:
                # TODO: grid data peaks olema ainult 40x40 ala, MITTE KOGU FKING TERRAIN DATA             


                # before data
                start_cut_x = 39*x
                start_cut_y = 39*y
                print('start cutting', x,y, start_cut_x, start_cut_y)


                print(len(UniversalVariables.map_list), len(UniversalVariables.map_list[1]))
                # after data
                max_len_remain_x = (len(UniversalVariables.map_list[1]) - x - 1) * 39
                max_len_remain_y = (len(UniversalVariables.map_list) - y - 1) * 39
                print('remain', max_len_remain_x, max_len_remain_y)

                print('0', grid_data)
                grid_data = grid_data[start_cut_y:-max_len_remain_y]  # Remove first and last rows
                print('1', grid_data)

                if max_len_remain_x != 0:
                    grid_data = [row[start_cut_x:-max_len_remain_x] for row in grid_data]  # Remove first and last columns from each remaining row

                    print('2', grid_data,)

                # Find occurrences of the number in the grid
                for row_index, sublist in enumerate(grid_data):
                    print('enu 1')
                    for col_index, element in enumerate(sublist):
                        print('enum 2')
                        
                        if element == number:
                            print("Added", col_index+1 ,row_index+1)
                            occurrences.append((col_index+1, row_index+1))  # Append tuple (row_index, col_index)
    
    # Return a random occurrence if found, otherwise return None
    print('occurrences', occurrences)

    if occurrences:
        return random.choice(occurrences)
    else:
        return None
    
    
class MazeChanges:

    times_changed: int = 0

    def change_maze(self):
        """ Muudab random maze pathwayisid (id 98) maze blockideks (id 99) ja vastupidi. """        

        # peab olema mingi in range. Mingi min, max peaks olema 
        index_of_wall = find_random_index_in_list_of_lists(self.terrain_data, 99)
        print(index_of_wall)
        
        if index_of_wall != None:  self.terrain_data[index_of_wall[0]][index_of_wall[1]] = 2
        index_of_pathway = find_random_index_in_list_of_lists(self.terrain_data, 98)
        if index_of_pathway != None:  self.terrain_data[index_of_pathway[0]][index_of_pathway[1]] = 2
        
        MazeChanges.times_changed += 1
