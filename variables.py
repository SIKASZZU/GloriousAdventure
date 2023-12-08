import random
import pygame

from map import MapData

class UniversalVariables:
    # ******************** PLAYER ******************** #

    block_size: int = 100
    player_height = block_size * 0.65
    player_width = block_size * 0.45


    player_hitbox_offset_x = 0.29 * block_size
    player_hitbox_offset_y = 0.22 * block_size
    player_x: int = random.randint(9 * block_size, 9 * block_size)
    player_y: int = random.randint(68 * block_size, 68 * block_size)

    # ******************** SCREEN ******************** #
    screen_x: int = 1000
    screen_y: int = 750
    screen = pygame.display.set_mode((screen_x, screen_y))

    # ******************** OTHER ******************** #
    collision_boxes: list = []  # collision
    terrain_data = MapData.map_creation()  # map data
    glade_data = MapData.glade_creation()  # glade data

    # ******************** OFFSET ******************** #
    offset_x: int = 0
    offset_y: int = 0