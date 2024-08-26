import random
import pygame

from images import ImageLoader

class TileSet:

    @staticmethod
    def get_tileset_image(image_path):
        return ImageLoader.load_image(None, image_path=image_path)

    @staticmethod
    def get_tile(tileset, tile_size, col, row):
        rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
        tile = tileset.subsurface(rect)
        return tile

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
        top_empty, bottom_empty, left_empty, right_empty, _, _, _, _ = surroundings
        tileset_image = TileSet.get_tileset_image('images/Tile_Sets/Water_Ground_Tileset.png')

        if right_empty and left_empty and top_empty and bottom_empty:
            return TileSet.get_tile(tileset_image, 32, 6, 1)
        if right_empty and left_empty and bottom_empty:
            return TileSet.get_tile(tileset_image, 32, 3, 2)
        if right_empty and left_empty and top_empty:
            return TileSet.get_tile(tileset_image, 32, 3, 0)
        if right_empty and top_empty and bottom_empty:
            return TileSet.get_tile(tileset_image, 32, 6, 0)
        if left_empty and top_empty and bottom_empty:
            return TileSet.get_tile(tileset_image, 32, 4, 0)

        if right_empty and bottom_empty:
            return TileSet.get_tile(tileset_image, 32, 2, 2)
        if left_empty and bottom_empty:
            return TileSet.get_tile(tileset_image, 32, 0, 2)
        if left_empty and top_empty:
            return TileSet.get_tile(tileset_image, 32, 0, 0)
        if right_empty and top_empty:
            return TileSet.get_tile(tileset_image, 32, 2, 0)

        if right_empty and left_empty:
            return TileSet.get_tile(tileset_image, 32, 3, 1)
        if top_empty and bottom_empty:
            return TileSet.get_tile(tileset_image, 32, 5, 0)

        if right_empty:
            return TileSet.get_tile(tileset_image, 32, 2, 1)
        if left_empty:
            return TileSet.get_tile(tileset_image, 32, 0, 1)
        if bottom_empty:
            return TileSet.get_tile(tileset_image, 32, 1, 2)
        if top_empty:
            return TileSet.get_tile(tileset_image, 32, 1, 0)

        if random.random() < 0.5:
            return 'Ground_19'
        else:
            return 'Ground_' + str(random.randint(0, 18))


    def determine_farmland_image_name(self, row, col):
        top_empty = row > 0 and self.terrain_data[row - 1][col] in [1, 2, 4, 5]
        bottom_empty = row < len(self.terrain_data) - 1 and self.terrain_data[row + 1][col] in [1, 2, 4, 5]
        left_empty = col > 0 and self.terrain_data[row][col - 1] in [1, 2, 4, 5]
        right_empty = col < len(self.terrain_data[0]) - 1 and self.terrain_data[row][col + 1] in [1, 2, 4, 5]

        if bottom_empty and top_empty and left_empty and right_empty:
            return "Farmland_Stand_Alone"
        if right_empty and left_empty and bottom_empty:
            return "Farmland_Straight_Down"
        if right_empty and left_empty and top_empty:
            return "Farmland_Straight_Up"
        if right_empty and top_empty and bottom_empty:
            return "Farmland_Straight_Right"
        if left_empty and top_empty and bottom_empty:
            return "Farmland_Straight_Left"

        if right_empty and left_empty:
            return "Farmland_Top_To_Bottom"
        if top_empty and bottom_empty:
            return "Farmland_Left_To_Right"

        if right_empty and bottom_empty:
            return 'Farmland_Inside_Top_Left'
        if left_empty and bottom_empty:
            return 'Farmland_Inside_Top_Right'
        if left_empty and top_empty:
            return 'Farmland_Inside_Bottom_Right'
        if right_empty and top_empty:
            return 'Farmland_Inside_Bottom_Left'

        if right_empty:
            return 'Farmland_Inside_Left'
        if left_empty:
            return 'Farmland_Inside_Right'
        if bottom_empty:
            return 'Farmland_Inside_Top'
        if top_empty:
            return 'Farmland_Inside_Bottom'

        return 'Farmland_Full'