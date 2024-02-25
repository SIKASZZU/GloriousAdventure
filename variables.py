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
    # ******************** SCREEN ******************** #
    screen_x: int = 1650
    screen_y: int = 1020

    screen = pygame.display.set_mode((screen_x, screen_y))
    jagatis = 15

    block_size: int = screen_x // jagatis

    # ******************** PLAYER ******************** #
    player_height: int = block_size * 0.65
    player_width: int = block_size * 0.45

    player_hitbox_offset_x = 0.29 * block_size
    player_hitbox_offset_y = 0.22 * block_size
    player_x: int = random.randint(3 * block_size, 3 * block_size)
    player_y: int = random.randint(25 * block_size, 25 * block_size)

    # ******************** OTHER ******************** #
    collision_boxes: list = []  # collision

    # ******************** VISION ******************** #
    light_range = 420
    walls = []  # Collision boxide seinad

    # ******************** OFFSET ******************** #
    offset_x: int = 0
    offset_y: int = 0

    map_list = [

        ['maze'],
        ['glade']
    ]

    blits_sequence = []