import random

class MazeChanges:

    def __init__(self, dn_text, variables):
        self.day_night_text = dn_text
        self.times_changed: int = 0
        self.loop_counter:  int = 0
        self.max_amount_of_changes = 150
        self.already_changed = set()
        self.variables = variables

    def find_random_index_in_list_of_lists(self, grid_data, number, grid_name='block_maze'):
        occurrences = []

        # TODO: praegu v6tab lihtsalt esimese block mazei. V6iks randomly valida millist muudab.
        #
        # Assuming self.variables.map_list contains the names of the grids in the same order as list_of_lists
        for y, sublist in enumerate(self.variables.map_list):
            for x, value in enumerate(sublist):

                if grid_name != self.variables.map_list[y][x]:
                    continue

                start_cut_x = 40*x + 1
                start_cut_y = 40*y + 1

                end_cut_x = (len(self.variables.map_list[1]) - x - 1) * 40
                end_cut_y = (len(self.variables.map_list) - y - 1) * 40

                grid_data = grid_data[start_cut_y:-end_cut_y]  # Remove Ylemine ja alumine rida.

                if end_cut_x == 0:  end_cut_x = 1
                grid_data = [row[start_cut_x:-end_cut_x] for row in grid_data]  # Remove vasak ja parem 22r

                #for row in grid_data: print(row)
                # Find occurrences of the number in the grid
                for row_index, sublist in enumerate(grid_data):
                    for col_index, element in enumerate(sublist):
                        if element == number:
                            grid = (col_index + start_cut_x, row_index + start_cut_y)
                            if grid not in already_changed:
                                occurrences.append(grid)  # liidan start cuti, sest self.terrain_dataga ei klapiks muidu

        # Return a random occurrence if found, otherwise return None
        if occurrences:
            chosen_grid = random.choice(occurrences)
            already_changed.add(chosen_grid)
            return chosen_grid
        else:
            return None
    def change_maze(self):
        """ Muudab random maze pathwayisid (id 98) maze blockideks (id 99) ja vastupidi. """

        if self.variables.maze_counter == 0:
            return
        
        if self.day_night_text == 'Day':
            self.times_changed = 0
            global already_changed
            already_changed = set()            
            return

        # iga nelja framei tagant muuta seina ja groundi. Night on 599 framei pikk ehk.. 599/150(muudatuste arv) ning saad framei kuna peab muutma
        if self.loop_counter < 4:  self.loop_counter += 1

        elif not self.times_changed > self.max_amount_of_changes:
            self.loop_counter = 0  # uue seina ja groundi valja vahetamine

            index_of_wall = self.find_random_index_in_list_of_lists(self.terrain_data, 99)
            self.terrain_data[index_of_wall[1]][index_of_wall[0]] = 98

            index_of_pathway = self.find_random_index_in_list_of_lists(self.terrain_data, 98)
            self.terrain_data[index_of_pathway[1]][index_of_pathway[0]] = 99

            self.times_changed += 1
