import random
import pygame
import inspect
import os
import time

from functools import wraps
class Decorators:
    """ Neid funce tuleb kutsuda @func """

    def log_execution_time(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            rounded_time = round(execution_time, 10)  # Rounding to 6 decimal places
            print(f"{func.__name__} executed in {rounded_time} seconds")
            return result

        return wrapper

    def memoize(func):
        cache = {}

        @wraps(func)
        def memoizer(*args, **kwargs):
            key = args + tuple(sorted(kwargs.items()))
            if key not in cache:
                cache[key] = func(*args, **kwargs)
            return cache[key]

        return memoizer

    def cache_results(func):
        cached_results = {}

        def wrapper(*args):
            if args not in cached_results:
                cached_results[args] = func(*args)
            return cached_results[args]

        return wrapper

    # ütleb mis funci kutsutakse, rida ja argumendid
    def log_calls_with_location(func):
        """ Ütleb mis funci kutsuti, mis failist, mis reast, kõik argumendid. Näiteks:
         Calling load_image from objects.py at line 109 with arguments: 'Oak_Tree' """

        def wrapper(*args, **kwargs):
            frame = inspect.currentframe().f_back
            file_name = os.path.basename(frame.f_code.co_filename)
            line_number = frame.f_lineno

            arg_str = ", ".join(map(repr, args))
            kwarg_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())

            if args and kwargs:
                args_str = f"{arg_str}, {kwarg_str}"
            else:
                args_str = arg_str if args else kwarg_str

            print(f"Calling {func.__name__} from {file_name} at line {line_number} with arguments: {args_str}")

            return func(*args, **kwargs)
        return wrapper


class UniversalVariables:
    # ******************** Settings ******************** #

    # Windowi suurus x, y
    screen_x: int = 1280  # 1024 × 576 | 1152 × 648 | 1280 × 720 (HD) | 1366 × 768 | 1600 × 900 | 1920 × 1080 (full HD) | 2560 × 1440 | 3840 × 2160 (4K UHD)
    screen_y: int = 720

    # Mängu heli tugevus
    sound_volume: int = 0.05

    # Mängu max tick rate
    FPS = 60


    # ******************** Screen ******************** #
    screen = pygame.display.set_mode((screen_x, screen_y))

    # Block size muutmiseks kui zoomitakse sisse või välja
    jagatis = 15
    block_size: int = screen_x // jagatis
    prev_block_size: int = 0


    # ******************** PLAYER ******************** #
    player_height: int = block_size * 0.65
    player_width: int = block_size * 0.65

    player_hitbox_offset_x = 0.29 * player_width
    player_hitbox_offset_y = 0.22 * player_height

    
    # Playeri koordinaatide arvutamine
    player_x: int = random.randint(1 * block_size, 38 * block_size)
    player_y: int = random.randint(40 * block_size, 77 * block_size)

    health_status = None
    player_range = block_size * 1.5

    # ******************** COLLISION ******************** #
    collision_boxes: list = []  # collision


    # ******************** VISION ******************** #
    light_range = 420
    opposite_light_range = 75
    walls = []  # Collision boxide seinad
    last_input = 's'  # See peab olema üks neist: [a, s, d, w], muidu annab errori - sest visionis tahab selle len() saada


    # ******************** MAZE ******************** #
    maze_counter = 1
    enemy_counter = 0
    final_maze = bool
    final_maze_key_slots: set = set()
    portal_frames: int = 0


    cutscene = False
    portal_frame_rect = None
    portal_list = []

    # ******************** Render ******************** #
    map_list = [['maze'], ['glade']]
    blits_sequence = []
    text_sequence = []
    no_terrain_background_items = [98, 99, 999 ,988, None, 500, 550, 555, 981, 982]
    no_shadow_needed = [0, 1, 2, 4, 7, 9, 107, 988, None, 500, 550, 555, 1000]
    door_ids = [90, 91, 92, 93, 94, 95, 96, 97, 933, 977]

    offset_x: int = 0
    offset_y: int = 0
    screen_x_08 = screen_x * 0.8
    screen_y_08 = screen_y * 0.8


    # ******************** Enemy ******************** #
    enemy_spawnpoint_list = set()
    enemy_speed = 0.03  # Enemy kiirus grid size'ina

    # Et ei arvutaks uut pathi 24/7 vaid arvutab seda seatud aja tagant
    enemy_path_update_tick = 10 + random.randint(-5, 5)

    # ******************** Counters ******************** #
    hitbox_count: int = 0


    # if mapdata is done, create enemy spawnpoints
    @staticmethod
    def find_spawnpoints_in_map_data(terrain_data):
        if terrain_data is not None:
            spawnpoints = set()
            for row in range(len(terrain_data)):
                for column in range(len(terrain_data[row])):
                    if terrain_data[row][column] == 98:
                        spawnpoints.add((row, column))

            count = 0
            for spawnpoint in spawnpoints:

                if count < 10 * UniversalVariables.maze_counter and spawnpoint not in UniversalVariables.enemy_spawnpoint_list:
                    UniversalVariables.enemy_spawnpoint_list.add(spawnpoint)
                    count += 1
                else:
                    break
