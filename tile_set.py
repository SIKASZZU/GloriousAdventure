
class TileSet:
    def check_surroundings(self, row, col, terrain_value):
        top_empty = row > 0 and self.terrain_data[row - 1][col] == terrain_value
        bottom_empty = row < len(self.terrain_data) - 1 and self.terrain_data[row + 1][col] == terrain_value
        left_empty = col > 0 and self.terrain_data[row][col - 1] == terrain_value
        right_empty = col < len(self.terrain_data[0]) - 1 and self.terrain_data[row][col + 1] == terrain_value
        top_left_empty = row > 0 and col > 0 and self.terrain_data[row - 1][col - 1] == 0
        top_right_empty = row > 0 and col < len(self.terrain_data[0]) - 1 and self.terrain_data[row - 1][col + 1] == terrain_value
        bottom_left_empty = row < len(self.terrain_data) - 1 and col > 0 and self.terrain_data[row + 1][col - 1] == terrain_value
        bottom_right_empty = row < len(self.terrain_data) - 1 and col < len(self.terrain_data[0]) - 1 and self.terrain_data[row + 1][col + 1] == terrain_value
        return top_empty, bottom_empty, left_empty, right_empty, top_left_empty, top_right_empty, bottom_left_empty, bottom_right_empty


    def determine_ground_image_name(self, surroundings):
        top_empty, bottom_empty, left_empty, right_empty, top_left_empty, top_right_empty, bottom_left_empty, bottom_right_empty = surroundings


        if right_empty and left_empty and top_empty and bottom_empty and top_right_empty and top_left_empty and bottom_right_empty and bottom_left_empty:
            return "Ground_Island"
        if right_empty and left_empty and bottom_right_empty and bottom_left_empty and bottom_empty:
            return "Ground_Straight_Down"
        if right_empty and left_empty and top_right_empty and top_left_empty and top_empty:
            return "Ground_Straight_Up"
        if right_empty and top_empty and top_right_empty and bottom_empty and bottom_right_empty:
            return "Ground_Straight_Right"
        if left_empty and top_empty and top_left_empty and bottom_empty and bottom_left_empty:
            return "Ground_Straight_Left"

        if right_empty and left_empty:
            return "Ground_Top_To_Bottom"
        if top_empty and bottom_empty:
            return "Ground_Left_To_Right"

        if right_empty and bottom_right_empty and bottom_empty:
            return 'Ground_Inside_Top_Left'
        if left_empty and bottom_left_empty and bottom_empty:
            return 'Ground_Inside_Top_Right'
        if left_empty and top_left_empty and top_empty:
            return 'Ground_Inside_Bottom_Right'
        if right_empty and top_right_empty and top_empty:
            return 'Ground_Inside_Bottom_Left'

        if right_empty:
            return 'Ground_Inside_Left'
        if left_empty:
            return 'Ground_Inside_Right'
        if bottom_empty:
            return 'Ground_Inside_Top'
        if top_empty:
            return 'Ground_Inside_Bottom'

        if bottom_right_empty:
            return 'Ground_Puddle_Bottom_Right'
        if bottom_left_empty:
            return 'Ground_Puddle_Bottom_Left'
        if top_left_empty:
            return 'Ground_Puddle_Top_Left'
        if top_right_empty:
            return 'Ground_Puddle_Top_Right'

        return None


    def determine_farmland_image_name(self, row, col):
        top_empty = row > 0 and self.terrain_data[row - 1][col] in [1, 2, 4, 5]
        bottom_empty = row < len(self.terrain_data) - 1 and self.terrain_data[row + 1][col] in [1, 2, 4, 5]
        left_empty = col > 0 and self.terrain_data[row][col - 1] in [1, 2, 4, 5]
        right_empty = col < len(self.terrain_data[0]) - 1 and self.terrain_data[row][col + 1] in [1, 2, 4, 5]
        top_left_empty = row > 0 and col > 0 and self.terrain_data[row - 1][col - 1] in [1, 2, 4, 5]
        top_right_empty = row > 0 and col < len(self.terrain_data[0]) - 1 and self.terrain_data[row - 1][col + 1] in [1, 2, 4, 5]
        bottom_left_empty = row < len(self.terrain_data) - 1 and col > 0 and self.terrain_data[row + 1][col - 1] in [1, 2, 4, 5]
        bottom_right_empty = row < len(self.terrain_data) - 1 and col < len(self.terrain_data[0]) - 1 and self.terrain_data[row + 1][col + 1] in [1, 2, 4, 5]

        if bottom_empty and bottom_left_empty and bottom_right_empty and top_empty and top_left_empty and top_right_empty and left_empty and right_empty:
            return "Farmland_Stand_Alone"
        if right_empty and left_empty and bottom_right_empty and bottom_left_empty and bottom_empty:
            return "Farmland_Straight_Down"
        if right_empty and left_empty and top_right_empty and top_left_empty and top_empty:
            return "Farmland_Straight_Up"
        if right_empty and top_empty and top_right_empty and bottom_empty and bottom_right_empty:
            return "Farmland_Straight_Right"
        if left_empty and top_empty and top_left_empty and bottom_empty and bottom_left_empty:
            return "Farmland_Straight_Left"

        if right_empty and left_empty:
            return "Farmland_Top_To_Bottom"
        if top_empty and bottom_empty:
            return "Farmland_Left_To_Right"

        if right_empty and bottom_right_empty and bottom_empty:
            return 'Farmland_Inside_Top_Left'
        if left_empty and bottom_left_empty and bottom_empty:
            return 'Farmland_Inside_Top_Right'
        if left_empty and top_left_empty and top_empty:
            return 'Farmland_Inside_Bottom_Right'
        if right_empty and top_right_empty and top_empty:
            return 'Farmland_Inside_Bottom_Left'

        if right_empty:
            return 'Farmland_Inside_Left'
        if left_empty:
            return 'Farmland_Inside_Right'
        if bottom_empty:
            return 'Farmland_Inside_Top'
        if top_empty:
            return 'Farmland_Inside_Bottom'

        if bottom_right_empty:
            return 'Farmland_Puddle_Bottom_Right'
        if bottom_left_empty:
            return 'Farmland_Puddle_Bottom_Left'
        if top_left_empty:
            return 'Farmland_Puddle_Top_Left'
        if top_right_empty:
            return 'Farmland_Puddle_Top_Right'

        return 'Farmland_Full'