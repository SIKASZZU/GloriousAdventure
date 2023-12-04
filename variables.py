import random
import pygame

from map import MapData

class UniversalVariables:
    # ******************** PLAYER ******************** #
    
    ### TODO: Oleneb, palju maze on addinud ja kuhu siis arvutab gladei asukoha ning spawnib player sinna
    player_x: int = random.randint(900, 900)
    player_y: int = random.randint(6800, 6800)

    block_size: int = 100
    player_height = block_size * 0.65
    player_width = block_size * 0.45

    # ******************** SCREEN ******************** #
    screen_x: int = 1000
    screen_y: int = 750
    screen = pygame.display.set_mode((screen_x, screen_y))

    # ******************** OTHER ******************** #
    collision_boxes: list = []  # collision
    full_map_data = MapData.map_creation()  # map data
    terrain_data = full_map_data
    glade_data = MapData.glade_creation()  # glade data

    # ******************** OFFSET ******************** #
    offset_x: int = 0
    offset_y: int = 0