from map import MapData
from variables import UniversalVariables
from objects import ObjectManagement
from camera import Camera


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
    maze_type = 'maze'  # regular maze is 'maze', final maze is 'final_maze'

    ### TODO: Kui soovid ust avada kus on juba mingi maze või glade siis teeb uksed lahti aga puzzle pice ära ei võta
    def add_maze_to_specific_position_top(self, map_list, row_index, col_index, maze_type):

        # Kui row_index on 0 ja seal ei ole place siis
        # lisab igale list'is olevale row'ile place'i.
        if row_index == 0 and map_list[row_index][col_index] != 'place':
            new_row = ['place' for _ in range(len(map_list[0]))]
            map_list.insert(0, new_row)

            for row in range(39):
                self.terrain_data.insert(0, [None] * len(self.terrain_data[0]))

            UniversalVariables.player_y += 39 * UniversalVariables.block_size  # teleb playeri 6igesse kohta
            Camera.camera_rect.top = Camera.camera_rect.top + 39 * UniversalVariables.block_size

        # Kui valitud asukohal on glade siis annab errori
        if map_list[row_index][col_index] == 'glade':
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

            new_maze = MapData.get_data(maze_type, 'bottom')  # uks läheb alla - maze ülesse

            # Arvutab algus row'i ja col'i self.terrain_data jaoks
            start_row = row_index * 39
            start_col = col_index * 39

            for i in range(40):
                for j in range(40):
                    self.terrain_data[start_row + i][start_col + j] = new_maze[i][j]
        else:
            print(f'Something fishy: add_maze_to_specific_position_top:{[row_index], [col_index]}')

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

        # Kui valitud asukohal on glade siis annab errori
        if map_list[row_index][col_index] == 'glade':
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

            new_maze = MapData.get_data(maze_type, 'top')

            # Arvutab algus row'i ja col'i self.terrain_data jaoks
            start_row = row_index * 39
            start_col = col_index * 39
            for i in range(40):
                for j in range(40):
                    self.terrain_data[start_row + i][start_col + j] = new_maze[i][j]
        else:
            print(f'Something fishy: add_maze_to_specific_position_bottom:{[row_index], [col_index]}')

    def add_maze_to_specific_position_left(self, map_list, row_index, col_index, maze_type):

        # Kui col_index == 0 ja seal ei ole place siis
        # lisab igale list'is olevale row'ile place'i.
        if col_index == 0 and map_list[row_index][col_index] != 'place' and map_list[row_index][col_index] != 'glade':
            for row in map_list:
                row.insert(0, 'place')

            for row in self.terrain_data:
                for row_len in range(39):
                    row.insert(0, None)

            UniversalVariables.player_x += 39 * UniversalVariables.block_size  # teleb playeri 6igesse kohta
            Camera.camera_rect.left = Camera.camera_rect.left + 39 * UniversalVariables.block_size

        # Kui valitud asukohal on glade siis annab errori
        if map_list[row_index][col_index] == 'glade':

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

            new_maze = MapData.get_data(maze_type, 'right')  # uks tuleb paremale - maze tuleb vasakule

            # Arvutab algus row'i ja col'i self.terrain_data jaoks
            start_row = row_index * 39
            start_col = col_index * 39

            for i in range(40):
                for j in range(40):
                    self.terrain_data[start_row + i][start_col + j] = new_maze[i][j]

        else:
            print(f'Something fishy: add_maze_to_specific_position_left:{[col_index], [row_index]}')

    def add_maze_to_specific_position_right(self, map_list, row_index, col_index, maze_type):

        # Kui col_index == [list'i esimese row'i andmete kogus] siis ta lisab igale row'ile place'i mis listis on.
        if col_index == len(map_list[0]):  # Igal row'il on sama andmete kogus
            for row in map_list:
                row.append('place')

            for row in self.terrain_data:
                row.extend([None] * 39)

        # Kui valitud asukohal on glade siis annab errori
        if map_list[row_index][col_index] == 'glade':
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

            new_maze = MapData.get_data(maze_type, 'left')  # uks tuleb vasakule - maze paremale

            # Arvutab algus row'i ja col'i self.terrain_data jaoks
            start_row = row_index * 39
            start_col = col_index * 39

            for i in range(40):
                for j in range(40):
                    self.terrain_data[start_row + i][start_col + j] = new_maze[i][j]
        else:
            print(f'Something fishy: add_maze_to_specific_position_right:{[row_index], [col_index]}')

    def update_terrain(self, location, coordinate, grid_other, object_id, grid_main):
        if UniversalVariables.final_maze == True and UniversalVariables.final_maze_spawned == False:
            maze_type = 'final_maze'
        else:
            maze_type = AddingMazeAtPosition.maze_type

        # location on 1 ylesse, 2 alla, 3 vasakule, 4 paremale
        if location == 3:
            gridx, gridy = grid_main, grid_other
            row_index = int(((gridx + 1) // 40))

            if grid_main == 19:
                coordinate += 19
                col_index = ((gridy - 21) // 40)

            else:
                coordinate += 20
                col_index = ((gridy - 20) // 40)
            if col_index < 0: col_index = 0
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

        # Do stuff here after adding maze
        # print()
        ObjectManagement.remove_object_from_inv('Maze_Key')  # remove maze key
        UniversalVariables.maze_counter += 1  # add maze counter, to calculate extra enemy spawns
        for row in UniversalVariables.map_list: print(row)  # print maze list
        # print(UniversalVariables.maze_counter)

if __name__ == '__main__':
    ...
