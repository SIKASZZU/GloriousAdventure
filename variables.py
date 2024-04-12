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
    prev_block_size: int = 0

    # ******************** PLAYER ******************** #
    player_height: int = block_size * 0.65
    player_width: int = block_size * 0.65

    player_hitbox_offset_x = 0.29 * player_width
    player_hitbox_offset_y = 0.22 * player_height
    
    # Playeri koordinaatide arvutamine
    player_x: int = random.randint(1 * block_size, 38 * block_size)
    player_y: int = random.randint(40 * block_size, 77 * block_size)

    # ******************** COLLISION ******************** #
    collision_boxes: list = []  # collision

    # ******************** VISION ******************** #
    light_range = 420
    opposite_light_range = 75
    walls = []  # Collision boxide seinad
    last_input = str

    # ******************** OFFSET ******************** #
    offset_x: int = 0
    offset_y: int = 0
    screen_x_08 = screen_x * 0.8
    screen_y_08 = screen_y * 0.8

    # ******************** MAZE ******************** #
    maze_counter = 1
    enemy_counter = 0

    # ******************** LISTS ******************** #
    map_list = [['maze'], ['glade']]
    blits_sequence = []
    text_sequence = []
    no_terrain_background_items = [98, 99]
    no_shadow_needed = [0,1,2,4,7,9,107,933]
    enemy_spawnpoint_list = set()

    # if mapdata is done, create enemy spawnpoints
    def find_spawnpoints_in_map_data(terrain_data):
        if terrain_data is not None:
            spawnpoints = set()
            for row in range(len(terrain_data)):
                for column in range(len(terrain_data[row])):
                    if terrain_data[row][column] == 98:
                        spawnpoints.add((row, column))

            # Add up to 5 new spawn points to the list
            count = 0
            
            for spawnpoint in spawnpoints:
                
                spawn_point_counter = (10*UniversalVariables.maze_counter)
                if UniversalVariables.maze_counter == 1: spawn_point_counter = 2

                if count < spawn_point_counter and spawnpoint not in UniversalVariables.enemy_spawnpoint_list:
                    UniversalVariables.enemy_spawnpoint_list.add(spawnpoint)
                    count += 1
                else:
                    break

    def render_text(self, text: str, position: tuple[int, int] = None,
                    color: tuple[int, int, int] = (255, 255, 255),
                    font: str = 'Arial', size: int = 20, background_opacity: float = 0.3) -> None:
        """
        Renderdab teksti mänguaknale, pakkudes kohandamise võimalusi teksti värvi, asukoha,
        fondi, suuruse ja tausta läbipaistvuse osas.

        Parameetrid:
        - text (str): Kuvatav tekst.
        - position (tuple[int, int], valikuline): Teksti asukoht ekraanil (x, y). Kui ei ole määratud,
          siis tekst keskendatakse ekraani allosas.
        - color (tuple[int, int, int], valikuline): Teksti värv RGB formaadis. Vaikimisi valge.
        - font (str, valikuline): Fondi nimi. Vaikimisi 'Arial'.
        - size (int, valikuline): Fondi suurus. Vaikimisi 20.
        - background_opacity (float, valikuline): Teksti tausta läbipaistvus (0 kuni 1). Vaikimisi 0.3.
        """

        font = pygame.font.SysFont(font, size)
        words = text.split(' ')
        lines = []
        current_line = []

        # Split text into lines
        for word in words:
            test_line = ' '.join(current_line + [word])
            line_width, line_height = font.size(test_line)
            if line_width <= UniversalVariables.screen_x_08:  # Use 80% of screen width
                current_line.append(word)
            else:
                if current_line:  # Add the current line if it's not empty
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:  # Add the last line
            lines.append(' '.join(current_line))

        # Calculate total height of the text block to center it vertically within the 80% height
        total_height = len(lines) * line_height

        # Adjust Y position based on whether a specific position is provided
        if position:
            base_y_position = position[1]
        else:
            # Center vertically within the 80% height area
            base_y_position = (UniversalVariables.screen_y + UniversalVariables.screen_y_08 - total_height) / 2

        for i, line in enumerate(lines):
            line_surface = font.render(line, True, color)
            line_width, _ = font.size(line)

            # Adjust X position to center the line or use the provided position
            if position:
                line_x_position = position[0]
            else:
                line_x_position = (UniversalVariables.screen_x - line_width) / 2

            line_y_position = base_y_position - i * line_height

            # Create and blit the background surface
            background_surface = pygame.Surface((line_width, line_height))
            background_surface.set_alpha(int(255 * background_opacity))
            background_surface.fill((0, 0, 0))
            self.screen.blit(background_surface, (line_x_position, line_y_position))
            self.screen.blit(line_surface, (line_x_position, line_y_position))