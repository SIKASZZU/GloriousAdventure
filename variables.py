import random
import pygame

from map import MapData

class UniversalVariables:
    # ******************** PLAYER ******************** #
    player_x: int = random.randint(400, 400)
    player_y: int = random.randint(400, 400)

    block_size: int = 100
    player_height = block_size * 0.65
    player_width = block_size * 0.45

    # ******************** SCREEN ******************** #
    screen_x: int = 1000
    screen_y: int = 750
    screen = pygame.display.set_mode((screen_x, screen_y))

    # ******************** OTHER ******************** #
    collision_boxes: list = []  # collision
    terrain_data = MapData.glade_creation()  # map

    # offset
    offset_x: int = 0
    offset_y: int = 0
