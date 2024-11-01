import random
import pygame

from images import ImageLoader

class TileSet:

    @staticmethod
    def get_tileset_image(image_name, image_path):
        return ImageLoader.load_image(image_name, image_path=image_path)

    @staticmethod
    def get_tile(tileset, tile_size, col, row):
        rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
        tile = tileset.subsurface(rect)
        return tile

    def check_surroundings(self, row: int, col: int, terrain_values: tuple):
        top_empty = row > 0 and self.terrain_data[row - 1][col] in terrain_values
        bottom_empty = row < len(self.terrain_data) - 1 and self.terrain_data[row + 1][col] in terrain_values
        left_empty = col > 0 and self.terrain_data[row][col - 1] in terrain_values
        right_empty = col < len(self.terrain_data[0]) - 1 and self.terrain_data[row][col + 1] in terrain_values
        return top_empty, bottom_empty, left_empty, right_empty


    def determine_ground_image(self, surroundings):
        top_empty, bottom_empty, left_empty, right_empty = surroundings
        tileset_image = TileSet.get_tileset_image('Water_Ground_Tileset', 'images/Tile_Sets/Water_Ground_Tileset.png')

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

    def determine_string_image(self, surroundings):
        top_empty, bottom_empty, left_empty, right_empty = surroundings
        tileset_image = TileSet.get_tileset_image('String_Tile_Set', 'images/Tile_Sets/String_Tile_Set.png')

        if right_empty and left_empty and top_empty and bottom_empty:
            return TileSet.get_tile(tileset_image, 32, 1, 1)

        # if right_empty and left_empty and bottom_empty:
        #     return TileSet.get_tile(tileset_image, 32, 3, 2)
        # if right_empty and left_empty and top_empty:
        #     return TileSet.get_tile(tileset_image, 32, 3, 0)
        # if right_empty and top_empty and bottom_empty:
        #     return TileSet.get_tile(tileset_image, 32, 6, 0)
        # if left_empty and top_empty and bottom_empty:
        #     return TileSet.get_tile(tileset_image, 32, 4, 0)
        #
        # if right_empty and bottom_empty:
        #     return TileSet.get_tile(tileset_image, 32, 2, 2)
        # if left_empty and bottom_empty:
        #     return TileSet.get_tile(tileset_image, 32, 0, 2)
        # if left_empty and top_empty:
        #     return TileSet.get_tile(tileset_image, 32, 0, 0)
        # if right_empty and top_empty:
        #     return TileSet.get_tile(tileset_image, 32, 2, 0)
        #
        # if right_empty and left_empty:
        #     return TileSet.get_tile(tileset_image, 32, 3, 1)
        # if top_empty and bottom_empty:
        #     return TileSet.get_tile(tileset_image, 32, 5, 0)
        #
        # if right_empty:
        #     return TileSet.get_tile(tileset_image, 32, 2, 1)
        # if left_empty:
        #     return TileSet.get_tile(tileset_image, 32, 0, 1)
        # if bottom_empty:
        #     return TileSet.get_tile(tileset_image, 32, 1, 2)
        # if top_empty:
        #     return TileSet.get_tile(tileset_image, 32, 1, 0)
        #
        # if random.random() < 0.5:
        #     return 'Ground_19'
        # else:
        #     return 'Ground_' + str(random.randint(0, 18))

    def determine_farmland_image_name(self, surroundings):
        top_empty, bottom_empty, left_empty, right_empty = surroundings

        conditions = [
            (bottom_empty and top_empty and left_empty and right_empty, "Farmland_Stand_Alone"),
            (right_empty and left_empty and bottom_empty, "Farmland_Straight_Down"),
            (right_empty and left_empty and top_empty, "Farmland_Straight_Up"),
            (right_empty and top_empty and bottom_empty, "Farmland_Straight_Right"),
            (left_empty and top_empty and bottom_empty, "Farmland_Straight_Left"),
            (right_empty and left_empty, "Farmland_Top_To_Bottom"),
            (top_empty and bottom_empty, "Farmland_Left_To_Right"),
            (right_empty and bottom_empty, 'Farmland_Inside_Top_Left'),
            (left_empty and bottom_empty, 'Farmland_Inside_Top_Right'),
            (left_empty and top_empty, 'Farmland_Inside_Bottom_Right'),
            (right_empty and top_empty, 'Farmland_Inside_Bottom_Left'),
            (right_empty, 'Farmland_Inside_Left'),
            (left_empty, 'Farmland_Inside_Right'),
            (bottom_empty, 'Farmland_Inside_Top'),
            (top_empty, 'Farmland_Inside_Bottom')
        ]

        for condition, image_name in conditions:
            if condition:
                return image_name

        return 'Farmland_Full'