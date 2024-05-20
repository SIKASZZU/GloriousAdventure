from update import EssentialsUpdate
from variables import UniversalVariables

def find_number_in_list_of_lists(list_of_lists, number):
    for row_index, sublist in enumerate(list_of_lists):
        for col_index, element in enumerate(sublist):
            if element == number:
                return row_index, col_index  # Number found, return its coordinates
    return None  # Number not found, return None

def count_occurrences_in_list_of_lists(list_of_lists, number):
    count = 0
    for sublist in list_of_lists:
        for element in sublist:
            if element == number:
                count += 1
    return count


def change_blades(self):
    if UniversalVariables.blades_spawned == True:
        if EssentialsUpdate.day_night_text != UniversalVariables.already_looped_blades:
            open_horizon_door_count = count_occurrences_in_list_of_lists(self.terrain_data, 989_98)
            open_vertical_door_count = count_occurrences_in_list_of_lists(self.terrain_data, 9099_98)
            
            closed_horizon_door_count = count_occurrences_in_list_of_lists(self.terrain_data, 989)
            closed_vertical_door_count = count_occurrences_in_list_of_lists(self.terrain_data, 9099)

            # print(
                # 'open_horizon_door_count    989_98',    open_horizon_door_count, 
                # 'open_vertical_door_count   9099_98',    open_vertical_door_count,
                # 'closed_horizon_door_count  989',    closed_horizon_door_count,
                # 'closed_vertical_door_count 9099',    closed_vertical_door_count
            # )

            if EssentialsUpdate.day_night_text == 'Night':
                UniversalVariables.already_looped_blades = 'Night'

                # Muudab horisontaalsed usked maze groundiks.
                for index in range(closed_horizon_door_count): 
                    row, col = find_number_in_list_of_lists(self.terrain_data, 989)
                    self.terrain_data[row][col] = 989_98
                
                # Vertikaalsed usked tekivad
                for index in range(open_vertical_door_count):
                    row, col = find_number_in_list_of_lists(self.terrain_data, 9099_98)
                    self.terrain_data[row][col] = 9099

            elif EssentialsUpdate.day_night_text == 'Day':
                UniversalVariables.already_looped_blades = 'Day'

                # Muudab vertikaalsed usked maze groundiks.
                for index in range(closed_vertical_door_count):
                    row, col = find_number_in_list_of_lists(self.terrain_data, 9099)
                    self.terrain_data[row][col] = 9099_98

                # Horisontaalsed usked tekivad
                for index in range(open_horizon_door_count):
                    row, col = find_number_in_list_of_lists(self.terrain_data, 989_98)
                    self.terrain_data[row][col] = 989