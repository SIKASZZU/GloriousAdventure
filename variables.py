import random
import pygame
import time

class UniversalVariables():

    debug_mode = False

    # ******************** Settings ******************** #

    # Windowi suurus x, y
    screen_x: int = 1366  # 1024 × 576 | 1152 × 648 | 1280 × 720 (HD) | 1366 × 768 | 1600 × 900 | 1920 × 1080 (full HD) | 2560 × 1440 | 3840 × 2160 (4K UHD)
    screen_y: int = 768

    # Mängu heli tugevus
    sound_volume: int = 0.05

    # Mängu max tick rate

    # ******************** Screen ******************** #
    screen = pygame.display.set_mode((screen_x, screen_y))

    # Block size muutmiseks kui zoomitakse sisse või välja
    jagatis: float = 15
    block_size: int = screen_x // jagatis
    prev_block_size: int = 0

    if debug_mode:
        # Mängu max tick rate
        FPS = 600

        player_range: int = block_size * 15

        enemy_speed = 0.05  # Enemy kiirus grid size'ina


    else:
        # Mängu max tick rate
        FPS = 60

        player_range: int = block_size * 1.5

        enemy_speed = 0.03  # Enemy kiirus grid size'ina


    # ******************** PLAYER ******************** #
    old_equipped_item = None
    old_equipped_item_item_type = None
    equipped_item: tuple = ()  # Käes oleva itemi trackimiseks

    player_height: int = block_size * 0.65
    player_width: int = block_size * 0.65

    player_hitbox_offset_x: float = 0.29 * player_width
    player_hitbox_offset_y: float = 0.22 * player_height

    # Playeri koordinaatide arvutamine
    player_x: int = random.randint(1 * block_size, 38 * block_size)
    player_y: int = random.randint(40 * block_size, 77 * block_size)

    health_status = None

    # ******************** Screen ******************** #
    ui_elements: list = []

    loot = [
        # ("Stick", (2, 5)),  # Kui itemil on range näiteks (2, 5) siis ta võtab random numbri nende seast - (2, 3, 4, 5)
        # ("Stone_Shard", 1),
        # ("Wood_Pickaxe", 1),
        # ("Oak_Planks", (2, 3)),
        # ("Small_Rock_Sword", 1),
        # ("Oak_Planks", (2, 3)),
        # ("Oak_Wood", (1, 2)),
        ('Flashlight', 1),
        #('Meat', 1),
        ('Bread', (1, 2)),
    ]

    # ******************** COLLISION ******************** #
    collision_boxes: list = []  # collision

    # ******************** VISION ******************** #
    light_range: int = 420
    opposite_light_range: int = 75
    walls: list = []  # Collision boxide seinad
    last_input: str = 'asd'  # See peab olema üks neist: [a, s, d, w], muidu annab errori - sest visionis tahab selle len() saada

    # ******************** MAZE ******************** #
    maze_counter: int = 1
    enemy_counter: int = 0
    final_maze = bool
    final_maze_spawned = False  # safety measure, et rohkem kui yhte final mazei ei tekiks.
    final_maze_key_slots: set = set()
    portal_frames: int = 0

    blades_spawned = False
    already_looped_blades = None
    
    cutscene = False
    portal_frame_rect = None
    portal_list: list = []

    # ******************** Render ******************** #
    map_list: list = [['maze'], ['glade']]
    blits_sequence: list = []
    text_sequence: list = []

    render_range_small: list = [
        10, 11,  # Key
        90, 91, 92, 93, 93, 94, 95, 96, 97, 977,  # Uksed
        98, 99,  # Ground ja Wall
        981, 982,  # Keyholder
        1001, 1002,  # Barrel
        989, 989_98, 9099, 9099_98, 900,  # Blade walls, grounds
    ]
    
    no_terrain_background_items: list = [
        None,
        98, 99,  # Ground ja Wall
        981, 982,  # Keyholder
        500, 550, 555, 988, 999,  # Portal, ground, wall
        #
    ]

    no_shadow_needed: list = [
        None,
        0, 1, 2, 4, 7, 107, 9,  # Mineralid
        500, 550, 555, 988, 999, 1000,  # Portal, ground, wall
        #
    ]

    door_ids: list = [90, 91, 92, 93, 94, 95, 96, 97]

    offset_x: int = 0
    offset_y: int = 0

    # ******************** Enemy ******************** #
    enemy_spawnpoint_list = set()

    # Et ei arvutaks uut pathi 24/7 vaid arvutab seda seatud aja tagant
    enemy_path_update_tick = 10 + random.randint(-5, 5)

    # ******************** Counters ******************** #
    hitbox_count: int = 0

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
