class AddingMazeAtPosition:
    # Example usage:
    map_list = [

        ['maze'],
        ['glade']
    ]

    row = []
    col = []

    def add_maze_to_specific_position_top(map_list, row_index, col_index):
        max_col_index = len(map_list[0])

        if abs(max_col_index - row_index) == len(map_list[0]):
            new_row = ['place' for _ in range(len(map_list[0]))]
            map_list.insert(0, new_row)

        if map_list[row_index][col_index] == 'place':
            map_list[row_index][col_index] = 'maze'

    def add_maze_to_specific_position_bottom(map_list, row_index, col_index):
        max_col_index = len(map_list[0]) - 1

        try:
            if map_list[row_index][col_index] == 'place':
                map_list[row_index][col_index] = 'maze'
        except IndexError:
            new_row = ['place' for _ in range(max_col_index + 1)]
            map_list.append(new_row)

        if map_list[row_index][col_index] == 'place':
            map_list[row_index][col_index] = 'maze'

    def add_maze_to_specific_position_left(map_list, row_index, col_index):
        for row in map_list:
            pass
        if abs(row_index - (len(row) - 1)) == (len(row) - 1):
            for row in map_list:
                row.insert(0, 'place')
        if map_list[col_index][row_index] == 'place':
            map_list[col_index][row_index] = 'maze'

    def add_maze_to_specific_position_right(map_list, row_index, col_index):
        # Calculate the new length after adding "maze" to the specified position
        new_length = col_index + 1

        # Check if the specified position is within bounds
        if row_index < len(map_list):
            for row in map_list:
                while len(row) < new_length:
                    row.append('place')

        if map_list[row_index][col_index] == 'place':
            map_list[row_index][col_index] = 'maze'


    def update_terrain(self, location, coordinate, grid_other, object_id, grid_main):
        ### location on 1 ylesse, 2 alla, 3 vasakule, 4 paremale

        if location == 3:
            gridx, gridy = grid_main, grid_other
            row_index = int(((gridx + 1) // 40))

            if grid_main == 19:
                coordinate += 19
                self.terrain_data[coordinate][grid_other + 40] = object_id
                self.terrain_data[coordinate + 1][grid_other + 40] = object_id
                col_index = ((gridy + 21) // 40)

            else:
                coordinate += 20
                self.terrain_data[coordinate][grid_other + 40] = object_id
                self.terrain_data[coordinate - 1][grid_other + 40] = object_id
                col_index = ((gridy + 20) // 40)

            AddingMazeAtPosition.add_maze_to_specific_position_left(AddingMazeAtPosition.map_list, row_index, col_index)

        if location == 4:
            gridx, gridy = grid_main, grid_other
            row_index = int(((gridx + 1) // 40))

            if grid_main == 19:
                coordinate += 19
                self.terrain_data[coordinate][grid_other] = object_id
                self.terrain_data[coordinate + 1][grid_other] = object_id
                col_index = ((gridy + 21) // 40)

            else:
                coordinate += 20
                self.terrain_data[coordinate][grid_other] = object_id
                self.terrain_data[coordinate - 1][grid_other] = object_id
                col_index = ((gridy + 20) // 40)

            AddingMazeAtPosition.add_maze_to_specific_position_right(AddingMazeAtPosition.map_list, row_index, col_index)

        if location == 1:
            gridx, gridy = grid_main, grid_other
            row_index = int(((gridx + 1) // 40))
            print(row_index)
            if grid_main == 19:
                self.terrain_data[coordinate + 40][grid_other + 19] = object_id
                self.terrain_data[coordinate + 40][grid_other + 20] = object_id
                col_index = ((gridy + 21) // 40)

            else:
                self.terrain_data[coordinate][grid_other + 19] = object_id
                self.terrain_data[coordinate][grid_other + 20] = object_id
                col_index = ((gridy + 20) // 40)

            AddingMazeAtPosition.add_maze_to_specific_position_top(AddingMazeAtPosition.map_list, row_index, col_index)

        if location == 2:
            gridx, gridy = grid_main, grid_other
            row_index = int(((gridx + 1) // 40))

            if grid_main == 19:
                self.terrain_data[coordinate][grid_other + 19] = object_id
                self.terrain_data[coordinate][grid_other + 20] = object_id
                col_index = ((gridy + 21) // 40)

            else:
                self.terrain_data[coordinate][grid_other + 19] = object_id
                self.terrain_data[coordinate][grid_other + 20] = object_id
                col_index = ((gridy + 20) // 40)

            AddingMazeAtPosition.add_maze_to_specific_position_bottom(AddingMazeAtPosition.map_list, row_index, col_index)


        print(row_index, col_index)
        print()

        for sublist in AddingMazeAtPosition.map_list:
            print(sublist)


if __name__ == '__main__':
    AddingMazeAtPosition.add_maze_to_specific_position_right(AddingMazeAtPosition.map_list, 0, 0)

    print()
    print()
    print()
    for sublist in AddingMazeAtPosition.map_list:
        print(sublist)
    print()
    print()
    print()
