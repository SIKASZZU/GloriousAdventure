from map import MapData
from variables import UniversalVariables
class AddingMazeAtPosition:
    row = []
    col = []

    def add_maze_to_specific_position_top(map_list, row_index, col_index):
        max_col_index = len(map_list[0])

        if abs(max_col_index - row_index) == len(map_list[0]):
            new_row = ['place' for _ in range(len(map_list[0]))]
            map_list.insert(0, new_row)

        if map_list[row_index][col_index] == 'place':
            map_list[row_index][col_index] = 'maze'


    def add_maze_to_specific_position_bottom(self, map_list, row_index, col_index):

        if row_index == len(map_list):
            new_row = ['place' for _ in range(len(map_list[0]))]
            map_list.append(new_row)

        if map_list[row_index][col_index] == 'place':
            map_list[row_index][col_index] = 'maze'

            new_maze = MapData.get_data('maze', 'top')

            start_row = row_index *  39
            start_col = col_index *  39

            for i in range(40):
                for j in range(40):
                    self.terrain_data[start_row + i][start_col + j] = new_maze[i][j]
        else:
            print(f'Something fishy: add_maze_to_specific_position_bottom:{[row_index],[col_index]}')


    def add_maze_to_specific_position_left(self, map_list, row_index, col_index):

        # [
        #  row row row row row row row col
        # ['maze', 'maze'],            col
        # ['place', 'glade']           col
        #                              col
        # ]                            col

        # Kui col_index == 0 siis ta lisab igale row'ile place'i mis listis on.
        if col_index == 0:
            for row in map_list:
                row.insert(0, 'place')

            for row in self.terrain_data:
                for row_len in range(39):
                    row.insert(0, None)

        # Kui valitud asukohal on juba place siis ta muudab selle maze'iks
        if map_list[col_index][row_index] == 'place':
            map_list[col_index][row_index] = 'maze'

            new_maze = MapData.get_data('maze', 'right')  # uks tuleb paremale - maze tuleb vasakule

            # Arvutab algus row'i ja col'i self.terrain_data jaoks
            start_row = row_index * 39
            start_col = col_index * 39

            for i in range(40):
                for j in range(40):
                    self.terrain_data[start_row + i][start_col + j] = new_maze[i][j]

        else:
            print(f'Something fishy: add_maze_to_specific_position_left:{[col_index],[row_index]}')


    def add_maze_to_specific_position_right(self, map_list, row_index, col_index):

        # [
        #  row row row row row row row col
        # ['maze', 'maze'],            col
        # ['place', 'glade']           col
        #                              col
        # ]                            col

        # Kui col_index == [list'i esimese row'i andmete kogus] siis ta lisab igale row'ile place'i mis listis on.
        if col_index == len(map_list[0]):  # Igal row'il on sama andmete kogus
            for row in map_list:
                row.append('place')

            for row in self.terrain_data:
                row.extend([None] * 39)

        # Kui valitud asukohal on juba place siis ta muudab selle maze'iks
        if map_list[row_index][col_index] == 'place':
            map_list[row_index][col_index] = 'maze'

            new_maze = MapData.get_data('maze', 'left')  # uks tuleb vasakule - maze tuleb paremale

            # Arvutab algus row'i ja col'i self.terrain_data jaoks
            start_row = row_index * 39
            start_col = col_index * 39

            for i in range(40):
                for j in range(40):
                    self.terrain_data[start_row + i][start_col + j] = new_maze[i][j]

        else:
            print(f'Something fishy: add_maze_to_specific_position_right:{[row_index],[col_index]}')


    def update_terrain(self, location, coordinate, grid_other, object_id, grid_main):
        ### location on 1 ylesse, 2 alla, 3 vasakule, 4 paremale

        if location == 3:
            gridx, gridy = grid_main, grid_other
            row_index = int(((gridx + 1) // 40))

            if grid_main == 19:
                coordinate += 19
                # self.terrain_data[coordinate][grid_other + 40] = object_id
                # self.terrain_data[coordinate + 1][grid_other + 40] = object_id
                col_index = ((gridy + 21) // 40)

            else:
                coordinate += 20
                # self.terrain_data[coordinate][grid_other + 40] = object_id
                # self.terrain_data[coordinate - 1][grid_other + 40] = object_id
                col_index = ((gridy + 20) // 40)

            AddingMazeAtPosition.add_maze_to_specific_position_left(self, UniversalVariables.map_list, row_index, col_index)

        if location == 4:
            gridx, gridy = grid_main, grid_other
            row_index = int(((gridx + 1) // 40))

            if grid_main == 19:
                coordinate += 19
                # self.terrain_data[coordinate][grid_other] = object_id
                # self.terrain_data[coordinate + 1][grid_other] = object_id
                col_index = ((gridy + 21) // 40)

            else:
                coordinate += 20
                # self.terrain_data[coordinate][grid_other] = object_id
                # self.terrain_data[coordinate - 1][grid_other] = object_id
                col_index = ((gridy + 20) // 40)

            AddingMazeAtPosition.add_maze_to_specific_position_right(self, UniversalVariables.map_list, row_index, col_index)

        if location == 1:
            gridx, gridy = grid_main, grid_other
            row_index = int(((gridx + 1) // 40))
            if grid_main == 19:
               # self.terrain_data[coordinate + 40][grid_other + 19] = object_id
               # self.terrain_data[coordinate + 40][grid_other + 20] = object_id
                col_index = ((gridy + 21) // 40)

            else:
                # self.terrain_data[coordinate][grid_other + 19] = object_id
                # self.terrain_data[coordinate][grid_other + 20] = object_id
                col_index = ((gridy + 20) // 40)

            AddingMazeAtPosition.add_maze_to_specific_position_top(UniversalVariables.map_list, row_index, col_index)

        if location == 2:
            gridx, gridy = grid_other, grid_main
            row_index = int(((gridx + 1) // 40))

            if grid_main == 19:
                # self.terrain_data[coordinate][grid_other + 19] = object_id
                # self.terrain_data[coordinate][grid_other + 20] = object_id
                col_index = ((gridy + 21) // 40)

            else:
                # self.terrain_data[coordinate][grid_other + 19] = object_id
                # self.terrain_data[coordinate][grid_other + 20] = object_id
                col_index = ((gridy + 20) // 40)

            AddingMazeAtPosition.add_maze_to_specific_position_bottom(self, UniversalVariables.map_list, row_index, col_index)


if __name__ == '__main__': ...
