from camera import Camera


class UniversalFunctions:
    def find_number_in_list_of_lists(list_of_lists, number):
        for row_index, sublist in enumerate(list_of_lists):
            for col_index, element in enumerate(sublist):
                if element == number:
                    return row_index, col_index  # Number found, return its coordinates
        return None, None  # Number not found, return None


    def count_occurrences_in_list_of_lists(list_of_lists, number):
        count = 0
        for sublist in list_of_lists:
            for element in sublist:
                if element == number:
                    count += 1
        return count


    def gray_yellow(self, color):
        if color == 'gray':
            x, y = UniversalFunctions.find_number_in_list_of_lists(self.terrain_data, 550)
            if x != None:
                self.terrain_data[x][y] = 500
                Camera.reset_clicks(self)

        if color == 'yellow':
            x, y = UniversalFunctions.find_number_in_list_of_lists(self.terrain_data, 500)
            self.terrain_data[x][y] = 550
            Camera.reset_clicks(self)


    def yellow_green(self, color):
        if color == 'yellow':
            for i in range(8):
                x, y = UniversalFunctions.find_number_in_list_of_lists(self.terrain_data, 555)
                self.terrain_data[x][y] = 550
                Camera.reset_clicks(self)

            UniversalFunctions.gray_yellow(self, 'gray')


        elif color == 'green':
            for i in range(8):
                x, y = UniversalFunctions.find_number_in_list_of_lists(self.terrain_data, 550)

                self.terrain_data[x][y] = 555
                Camera.reset_clicks(self)
