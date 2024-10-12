import random
from variables import UniversalVariables
from update import EssentialsUpdate

def find_random_index_in_list_of_lists(grid_data, number, grid_name='block_maze'):
    occurrences = []


    # TODO: praegu v6tab lihtsalt esimese block mazei. V6iks randomly valida millist muudab.
    
    # Assuming UniversalVariables.map_list contains the names of the grids in the same order as list_of_lists    
    for y, sublist in enumerate(UniversalVariables.map_list):
        for x, value in enumerate(sublist):

            if grid_name == UniversalVariables.map_list[y][x]:
                start_cut_x = 40*x + 1
                start_cut_y = 40*y + 1

                end_cut_x = (len(UniversalVariables.map_list[1]) - x - 1) * 40
                end_cut_y = (len(UniversalVariables.map_list) - y - 1) * 40
                
                grid_data = grid_data[start_cut_y:-end_cut_y]  # Remove Ylemine ja alumine rida.

                if end_cut_x == 0:  end_cut_x = 1
                grid_data = [row[start_cut_x:-end_cut_x] for row in grid_data]  # Remove vasak ja parem 22r

                #for row in grid_data: print(row)
                # Find occurrences of the number in the grid
                for row_index, sublist in enumerate(grid_data):
                    for col_index, element in enumerate(sublist):                        
                        if element == number:
                            # FIXME: see et ta lisab start_cuti, keerab self.terrain_dataga v6rreldes koordinaadid perse.
                                # element peaks olema kas 98,99. Grid datas on 6ige aga self.terrain-datas on vale, +-1 peab kuidagi tekkima sia >:D
                            occurrences.append((col_index + start_cut_x, row_index + start_cut_y))  # liidan start cuti, sest self.terrain_dataga ei klapiks muidu
    
    # Return a random occurrence if found, otherwise return None
    if occurrences:
        return random.choice(occurrences)
    else:
        return None
    
    
class MazeChanges:

    times_changed: int = 0
    max_amount_of_changes = 150

    def change_maze(self):
        """ Muudab random maze pathwayisid (id 98) maze blockideks (id 99) ja vastupidi. """        

        if EssentialsUpdate.day_night_text == 'Day':
            MazeChanges.times_changed = 0
            pass

        else:
            if not MazeChanges.times_changed > MazeChanges.max_amount_of_changes:
                try:
                    index_of_wall = find_random_index_in_list_of_lists(self.terrain_data, 99)            
                    self.terrain_data[index_of_wall[1]][index_of_wall[0]] = 98

                    index_of_pathway = find_random_index_in_list_of_lists(self.terrain_data, 98)
                    self.terrain_data[index_of_pathway[1]][index_of_pathway[0]] = 99
                    
                    MazeChanges.times_changed += 1
                except Exception as e: print('Error @ maze_changes.py.', e)