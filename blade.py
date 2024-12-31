from functions import UniversalFunctions


class Blades:
    def __init__(self, terrain_data, essentials, variables):
        self.terrain_data = terrain_data
        self.essentials = essentials
        self.variables = variables

    def change_blades(self):
        if not self.variables.blades_spawned:
            return

        if self.essentials.day_night_text != self.variables.already_looped_blades:

            # Open #
            open_horizon_door_count = UniversalFunctions.count_occurrences_in_list_of_lists(
                self.terrain_data, 989_98)

            open_vertical_door_count = UniversalFunctions.count_occurrences_in_list_of_lists(
                self.terrain_data, 9099_98)

            # Close #
            closed_horizon_door_count = UniversalFunctions.count_occurrences_in_list_of_lists(
                self.terrain_data, 989)

            closed_vertical_door_count = UniversalFunctions.count_occurrences_in_list_of_lists(
                self.terrain_data, 9099)

            # print(
            # 'open_horizon_door_count    989_98',    open_horizon_door_count,
            # 'open_vertical_door_count   9099_98',    open_vertical_door_count,
            # 'closed_horizon_door_count  989',    closed_horizon_door_count,
            # 'closed_vertical_door_count 9099',    closed_vertical_door_count
            # )

            if self.essentials.day_night_text == 'Night':
                self.variables.already_looped_blades = 'Night'

                # Muudab horisontaalsed usked maze groundiks.
                for index in range(closed_horizon_door_count):
                    row, col = UniversalFunctions.find_number_in_list_of_lists(self.terrain_data, 989)
                    self.terrain_data[row][col] = 989_98

                # Vertikaalsed usked tekivad
                for index in range(open_vertical_door_count):
                    row, col = UniversalFunctions.find_number_in_list_of_lists(self.terrain_data, 9099_98)
                    self.terrain_data[row][col] = 9099

            elif self.essentials.day_night_text == 'Day':
                self.variables.already_looped_blades = 'Day'

                # Muudab vertikaalsed usked maze groundiks.
                for index in range(closed_vertical_door_count):
                    row, col = UniversalFunctions.find_number_in_list_of_lists(self.terrain_data, 9099)
                    self.terrain_data[row][col] = 9099_98

                # Horisontaalsed usked tekivad
                for index in range(open_horizon_door_count):
                    row, col = UniversalFunctions.find_number_in_list_of_lists(self.terrain_data, 989_98)
                    self.terrain_data[row][col] = 989
