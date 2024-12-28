from map import MapData
from variables import UniversalVariables
from objects import ObjectManagement
from camera import Camera
from text import Fading_text
from inventory import Inventory

import numpy as np


def find_number_in_radius(list_of_lists, number, player_row, player_col, radius=5):
    # Search within the defined radius
    coordinates = set()

    for row_index in range(player_row - radius, player_row + radius):
        for col_index in range(player_col - radius, player_col + radius):

            if list_of_lists[row_index][col_index] == number:
                coordinates.add((row_index, col_index))

    return coordinates


class AddingMazeAtPosition:
    row = []
    col = []
    maze_type = 'block_maze'  # regular maze is 'block_maze', final maze is 'final_maze'

    def add_maze_to_specific_position_top(self, map_list, row_index, col_index, maze_type):

        # Kui valitud asukohal on glade või maze siis teeb lihtsalt uksed lahti
        if map_list[row_index][col_index] in ['labyrinth_maze', 'block_maze', 'blade_maze', 'final_maze', 'abandoned_glade']:
            Fading_text.re_display_fading_text("This place looks familiar.")

            # Arvutab algus row'i ja col'i self.terrain_data jaoks
            player_row = int(UniversalVariables.player_y // UniversalVariables.block_size)
            player_col = int(UniversalVariables.player_x // UniversalVariables.block_size)

            coordinates = find_number_in_radius(self.terrain_data, 95, player_row, player_col)

            for tuple in coordinates:
                start_row, start_col = tuple
                self.terrain_data[start_row][start_col] = 933

            return

        # Kui valitud asukohal on juba place siis ta muudab selle maze'iks
        if map_list[row_index][col_index] == 'place':
            map_list[row_index][col_index] = maze_type

            new_maze = MapData.get_data(self, maze_type, 'bottom')  # uks läheb alla - maze ülesse

            # Kui teed esimese maze siis muudab selle ukse 933'ks,
            # et need hakkaksid öö/päeva vältel kinni/lahti käima
            if UniversalVariables.maze_counter == 0:
                for row in new_maze:
                    row[:] = [933 if value == 93 else value for value in row]

            # Arvutab algus row'i ja col'i self.terrain_data jaoks
            start_row = row_index * 39
            start_col = col_index * 39

            for i in range(40):
                for j in range(40):
                    self.terrain_data[start_row + i][start_col + j] = new_maze[i][j]

            ObjectManagement.remove_object_from_inv('Maze_Key')  # remove maze key
            UniversalVariables.maze_counter += 1  # add maze counter, to calculate extra entity spawns
            AddingMazeAtPosition.maze_type = maze_type
            Inventory.calculate(self, calc_slots_only=True)
            return

            # # Muudab uue maze uksed 933.
            # # Kui maze uks on 933 siis see läheb öösel kinni ja päeval tuleb lahti
            # player_row = int(UniversalVariables.player_y // UniversalVariables.block_size)
            # player_col = int(UniversalVariables.player_x // UniversalVariables.block_size)
            #
            # coordinates = find_number_in_radius(self.terrain_data, 93, player_row, player_col)
            # for tuple in coordinates:
            #     start_row, start_col = tuple
            #     self.terrain_data[start_row][start_col] = 933

    def add_maze_to_specific_position_bottom(self, map_list, row_index, col_index, maze_type):

        # Kui row_index on võrdne mapis map_list'is olevale listide
        # arvuga siis lisab igale list'is olevale row'ile place'i.
        if row_index == len(map_list):
            new_row = ['place' for _ in range(len(map_list[0]))]
            map_list.append(new_row)

            row = []
            for i in range(40):
                row = [None] * len(self.terrain_data[0])
                self.terrain_data.append(row)

        # Kui valitud asukohal on glade või maze siis teeb lihtsalt uksed lahti
        if map_list[row_index][col_index] in ['labyrinth_maze', 'block_maze', 'blade_maze', 'final_maze', 'abandoned_glade']:
            Fading_text.re_display_fading_text("This place looks familiar.")

            # Arvutab algus row'i ja col'i self.terrain_data jaoks
            player_row = int(UniversalVariables.player_y // UniversalVariables.block_size)
            player_col = int(UniversalVariables.player_x // UniversalVariables.block_size)

            coordinates = find_number_in_radius(self.terrain_data, 97, player_row, player_col)

            for tuple in coordinates:
                start_row, start_col = tuple
                self.terrain_data[start_row][start_col] = 933

            return

        # Kui valitud asukohal on juba place siis ta muudab selle maze'iks
        if map_list[row_index][col_index] == 'place':
            map_list[row_index][col_index] = maze_type

            new_maze = MapData.get_data(self, maze_type, 'top')

            # Arvutab algus row'i ja col'i self.terrain_data jaoks
            start_row = row_index * 39
            start_col = col_index * 39
            for i in range(40):
                for j in range(40):
                    self.terrain_data[start_row + i][start_col + j] = new_maze[i][j]

            ObjectManagement.remove_object_from_inv('Maze_Key')  # remove maze key
            UniversalVariables.maze_counter += 1  # add maze counter, to calculate extra entity spawns
            AddingMazeAtPosition.maze_type = maze_type
            Inventory.calculate(self, calc_slots_only=True)
            return

            # # Muudab uue maze uksed 933.
            # # Kui maze uks on 933 siis see läheb öösel kinni ja päeval tuleb lahti
            # player_row = int(UniversalVariables.player_y // UniversalVariables.block_size)
            # player_col = int(UniversalVariables.player_x // UniversalVariables.block_size)
            #
            # coordinates = find_number_in_radius(self.terrain_data, 91, player_row, player_col)
            # for tuple in coordinates:
            #     start_row, start_col = tuple
            #     self.terrain_data[start_row][start_col] = 933


    def add_maze_to_specific_position_left(self, map_list, row_index, col_index, maze_type):

        # Kui valitud asukohal on glade või maze siis teeb lihtsalt uksed lahti
        if map_list[row_index][col_index] in ['labyrinth_maze', 'block_maze', 'blade_maze', 'final_maze', 'abandoned_glade']:
            Fading_text.re_display_fading_text("This place looks familiar.")

            # Arvutab algus row'i ja col'i self.terrain_data jaoks
            player_row = int(UniversalVariables.player_y // UniversalVariables.block_size)
            player_col = int(UniversalVariables.player_x // UniversalVariables.block_size)

            coordinates = find_number_in_radius(self.terrain_data, 94, player_row, player_col)

            for tuple in coordinates:
                start_row, start_col = tuple
                self.terrain_data[start_row][start_col] = 933

            return

        # Kui valitud asukohal on juba place siis ta muudab selle maze'iks
        if map_list[row_index][col_index] == 'place':
            map_list[row_index][col_index] = maze_type

            new_maze = MapData.get_data(self, maze_type, 'right')  # uks tuleb paremale - maze tuleb vasakule

            # Arvutab algus row'i ja col'i self.terrain_data jaoks
            start_row = row_index * 39
            start_col = col_index * 39

            for i in range(40):
                for j in range(40):
                    self.terrain_data[start_row + i][start_col + j] = new_maze[i][j]

            ObjectManagement.remove_object_from_inv('Maze_Key')  # remove maze key
            UniversalVariables.maze_counter += 1  # add maze counter, to calculate extra entity spawns
            AddingMazeAtPosition.maze_type = maze_type
            Inventory.calculate(self, calc_slots_only=True)
            return

            # # Muudab uue maze uksed 933.
            # # Kui maze uks on 933 siis see läheb öösel kinni ja päeval tuleb lahti
            # player_row = int(UniversalVariables.player_y // UniversalVariables.block_size)
            # player_col = int(UniversalVariables.player_x // UniversalVariables.block_size)
            #
            # coordinates = find_number_in_radius(self.terrain_data, 92, player_row, player_col)
            # for tuple in coordinates:
            #     start_row, start_col = tuple
            #     self.terrain_data[start_row][start_col] = 933

    def add_maze_to_specific_position_right(self, map_list, row_index, col_index, maze_type):

        # Kui col_index == [list'i esimese row'i andmete kogus] siis ta lisab igale row'ile place'i mis listis on.
        if col_index == len(map_list[0]):  # Igal row'il on sama andmete kogus
            for row in map_list:
                row.append('place')

            for row in self.terrain_data:
                row.extend([None] * 39)

        # Kui valitud asukohal on glade või maze siis teeb lihtsalt uksed lahti
        if map_list[row_index][col_index] in ['labyrinth_maze', 'block_maze', 'blade_maze', 'final_maze', 'abandoned_glade']:
            Fading_text.re_display_fading_text("This place looks familiar.")

            # Arvutab algus row'i ja col'i self.terrain_data jaoks
            player_row = int(UniversalVariables.player_y // UniversalVariables.block_size)
            player_col = int(UniversalVariables.player_x // UniversalVariables.block_size)

            coordinates = find_number_in_radius(self.terrain_data, 96, player_row, player_col)

            for tuple in coordinates:
                start_row, start_col = tuple
                self.terrain_data[start_row][start_col] = 933

            return

        # Kui valitud asukohal on juba place siis ta muudab selle maze'iks
        if map_list[row_index][col_index] == 'place':
            map_list[row_index][col_index] = maze_type

            new_maze = MapData.get_data(self, maze_type, 'left')  # uks tuleb vasakule - maze paremale

            # Arvutab algus row'i ja col'i self.terrain_data jaoks
            start_row = row_index * 39
            start_col = col_index * 39

            for i in range(40):
                for j in range(40):
                    self.terrain_data[start_row + i][start_col + j] = new_maze[i][j]

            ObjectManagement.remove_object_from_inv('Maze_Key')  # remove maze key
            UniversalVariables.maze_counter += 1  # add maze counter, to calculate extra entity spawns
            AddingMazeAtPosition.maze_type = maze_type
            Inventory.calculate(self, calc_slots_only=True)
            return

            # # Muudab uue maze uksed 933.
            # # Kui maze uks on 933 siis see läheb öösel kinni ja päeval tuleb lahti
            # player_row = int(UniversalVariables.player_y // UniversalVariables.block_size)
            # player_col = int(UniversalVariables.player_x // UniversalVariables.block_size)
            #
            # coordinates = find_number_in_radius(self.terrain_data, 90, player_row, player_col)
            # for tuple in coordinates:
            #     start_row, start_col = tuple
            #     self.terrain_data[start_row][start_col] = 933

    def update_terrain(self, location, coordinate, grid_other, object_id, grid_main):
        if UniversalVariables.maze_counter == 0:  # Kõige esimene maze on alati 'block_maze'
            choices = ['block_maze']
            probabilities = [1]  # 100 % alati olema

        elif AddingMazeAtPosition.maze_type == 'blade_maze' or UniversalVariables.maze_counter == 1:
            # 40 % 'labyrinth_maze' ja 60 % 'block_maze'
            choices = ['labyrinth_maze', 'block_maze', 'abandoned_glade']
            probabilities = [0.09, 0.83, 0.08]  # 100 % alati olema

        elif UniversalVariables.final_maze:
            # 30 % 'labyrinth_maze' ja 60 % 'block_maze' ja 10 % 'blade_maze'
            choices = ['labyrinth_maze', 'block_maze', 'blade_maze', 'abandoned_glade']
            probabilities = [0.25, 0.49, 0.19, 0.07, ]  # 100 % alati olema

        else:
            # 25 % 'labyrinth_maze' ja 45 % 'block_maze' ja 20 % 'blade_maze' ja 10 % 'final_maze'
            choices = ['labyrinth_maze', 'block_maze', 'blade_maze', 'final_maze', 'abandoned_glade']
            probabilities = [0.23, 0.43, 0.20, 0.10, 0.04]  # 100 % alati olema

        maze_type = np.random.choice(choices, p=probabilities)
        print("Next maze", maze_type, 'Kui maze ei tekkinud, ss map.pys vaadata maze_type functioni. Ilmselt listi, numpyarray kyhvel.')

        # location on 1 ylesse, 2 alla, 3 vasakule, 4 paremale
        if location == 3:  # left
            gridx, gridy = grid_main, grid_other
            row_index = int(((gridx + 1) // 40))

            if grid_main == 19:
                coordinate += 19
                col_index = ((gridy - 21) // 40)

            else:
                coordinate += 20
                col_index = ((gridy - 20) // 40)
            if col_index < 0: col_index = 0

            # Kui siia ei pane seda siis läheb hiljem perse
            if col_index == 0:

                for row in UniversalVariables.map_list:
                    row.insert(0, 'place')

                for row in self.terrain_data:
                    for row_len in range(39):
                        row.insert(0, None)

                # teleb playeri ja camera 6igesse kohta
                UniversalVariables.player_x += 39 * UniversalVariables.block_size
                Camera.camera_rect.left = Camera.camera_rect.left + 39 * UniversalVariables.block_size

                # Kuna lisas uue placei listi algusesse siis peab ka indexi lisama
                col_index += 1


            AddingMazeAtPosition.add_maze_to_specific_position_left(self, UniversalVariables.map_list, row_index,
                                                                    col_index, maze_type)

        if location == 4:
            gridx, gridy = grid_main, grid_other
            row_index = int(((gridx + 1) // 40))

            if grid_main == 19:
                coordinate += 19
                col_index = ((gridy + 21) // 40)

            else:
                coordinate += 20
                col_index = ((gridy + 20) // 40)
            AddingMazeAtPosition.add_maze_to_specific_position_right(self, UniversalVariables.map_list, row_index,
                                                                     col_index, maze_type)

        if location == 1:
            gridx, gridy = grid_other, grid_main
            col_index = int(((gridx + 1) // 40))

            if grid_main == 19:
                row_index = ((gridy - 21) // 40)
            else:
                row_index = ((gridy - 20) // 40)
            if row_index < 0: row_index = 0

            # Kui siia ei pane seda siis läheb hiljem perse
            if row_index == 0:

                new_row = ['place' for _ in range(len(UniversalVariables.map_list[0]))]
                UniversalVariables.map_list.insert(0, new_row)

                for row in range(39):
                    self.terrain_data.insert(0, [None] * len(self.terrain_data[0]))

                # teleb playeri ja camera 6igesse kohta
                UniversalVariables.player_y += 39 * UniversalVariables.block_size
                Camera.camera_rect.top = Camera.camera_rect.top + 39 * UniversalVariables.block_size

                # Kuna lisas uue placei listi algusesse siis peab ka indexi lisama
                row_index += 1

            AddingMazeAtPosition.add_maze_to_specific_position_top(self, UniversalVariables.map_list, row_index,
                                                                   col_index, maze_type)

        if location == 2:
            gridx, gridy = grid_other, grid_main
            col_index = int(((gridx + 1) // 40))

            if grid_main == 19:
                row_index = ((gridy + 21) // 40)
            else:
                row_index = ((gridy + 20) // 40)
            if row_index < 0: row_index = 0
            AddingMazeAtPosition.add_maze_to_specific_position_bottom(self, UniversalVariables.map_list, row_index,
                                                                      col_index, maze_type)

        # # # Do stuff here after adding maze
        # print()
        # for row in UniversalVariables.map_list: print(row)  # print maze list
        # print(UniversalVariables.maze_counter)


if __name__ == '__main__':
    ...