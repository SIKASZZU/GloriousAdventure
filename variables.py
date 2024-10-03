import random
import pygame

from enum import Enum


class GameConfig(Enum):
    # Render: wheat -> rock -> stump -> tree
    OBJECT_RENDER_ORDER: tuple[int, ...] = (7, 2, 5, 4)

    RANDOM_PLACEMENT: tuple[int, ...] = (2, 4, 5, 10, 12, 13, 1001, 1002, 1003)  # Random position items

    INITIAL_GLADE_ITEMS : tuple[int, ...] = (1, 2, 3, 4, 5, 8, 9)

    FARMABLES           : tuple[int, ...] = (7, 71, 74, 77)
    WHEAT_STAGES        : tuple[int, ...] = (69, 70)
    CARROT_TAGES        : tuple[int, ...] = (75, 76)
    CORN_STAGES         : tuple[int, ...] = (78, 79)
    POTATO_STAGES       : tuple[int, ...] = (72, 73)

    FARMABLE_STAGES     : tuple[int, ...] = WHEAT_STAGES + CARROT_TAGES + CORN_STAGES  + POTATO_STAGES

    FARMLAND_IMAGE      : tuple[int, ...] = FARMABLES + FARMABLE_STAGES + (107, )

    GROUND_IMAGE        : tuple[int, ...] = INITIAL_GLADE_ITEMS + tuple(id for id in range(1004, 1016))  # GLADE_ITEMS + 1004 -> 1015
    MAZE_GROUND_IMAGE   : tuple[int, ...] = (
        # 6,                      # String
        10, 12, 13,             # Maze Keys
        90, 91, 92, 93, 933,    # Maze Doors
        98,                     # Maze Ground
        1001, 1002, 1003,       # Barrel, Chest
    )
    GLADE_ITEMS         : tuple[int, ...] = INITIAL_GLADE_ITEMS + FARMABLES
    INTERACTABLE_ITEMS  : tuple[int, ...] = (2, 4, 6, 10, 94, 95, 96, 97, 981, 982, 1001, 1002)  # ei renderi topelt map_renderi all

    RENDER_RANGE_SMALL  : tuple[int, ...] = (
        10, 11, 12, 13,                                 # Key
        90, 91, 92, 93, 93, 94, 95, 96, 97, 933, 977,   # Uksed
        98, 99,                                         # Ground ja Wall
        981, 982,                                       # Keyholder
        1001, 1002, 1003,                               # Barrel, Chest
        989, 98998, 9099, 909998, 900                   # Blade walls, Grounds
    )


    ### FIXME: MIND POLE VAJA JU VÕI ON??? Paneme pildid ainult sinna kuhu vaja
    ###        ja mujale mitte ehk ss GROUND_IMAGE ja MAZE_GROUND_IMAGE jne...
    NO_TERRAIN_BACKGROUND_ITEMS: tuple[int, ...] = (
        None,
        98, 99,  # Ground ja Wall
        981, 982,  # Keyholder
        500, 550, 555, 988, 999  # Portal, ground, wall
    )

    OPEN_DOOR_IDS: tuple[int, ...] = (90, 91, 92, 93, 933)
    CLOSED_DOOR_IDS: tuple[int, ...] = (94, 95, 96, 97, 977)
    ALL_THE_DOORS: tuple[int, ...] = OPEN_DOOR_IDS + CLOSED_DOOR_IDS  # Combine the tuples

    COOKING_STATIONS: tuple[int, ...] = (8, )  # Campfire

class UniversalVariables():

    debug_mode = True

    # ******************** Settings ******************** #

    # Windowi suurus x, y
    screen_x: int = 1366  # 1024 × 576 | 1152 × 648 | 1280 × 720 (HD) | 1366 × 768 | 1600 × 900 | 1920 × 1080 (full HD) | 2560 × 1440 | 3840 × 2160 (4K UHD)
    screen_y: int = 768

    # Mängu heli tugevus
    sound_volume: int = 0.1

    # Mängu max tick rate

    # ******************** Screen ******************** #
    screen = pygame.display.set_mode((screen_x, screen_y))

    # Effectide suurused

    icon_width: int = 60
    icon_height: int = 60

    # Block size muutmiseks kui zoomitakse sisse või välja
    prev_block_size: int = 0

    if debug_mode:
        jagatis: float = 10

        # Mängu max tick rate
        FPS: int = 200

        block_size: int = screen_x // jagatis
        player_range: int = block_size * 15

        enemy_speed: float = 0.05  # Enemy kiirus grid size'ina

        cooking_range:int = 5  # Grid


    else:
        jagatis: float = 10

        # Mängu max tick rate
        FPS: int = 60

        block_size: int = screen_x // jagatis
        player_range: int = block_size * 1.5

        enemy_speed: float = 0.03  # Enemy kiirus grid size'ina

        cooking_range:int = 2  # Grid

    # ******************** PLAYER ******************** #
    current_equipped_item = None
    current_equipped_item_item_type = None
    interaction_delay = 100  # Delay tegevuse vahel, näiteks söömine, ehitamine, asjade ülesse võtmine
    interaction_delay_max = interaction_delay

    player_height: int = block_size * 0.45
    player_width: int = block_size * 0.45

    player_hitbox_offset_x: float = 0.29 * player_width
    player_hitbox_offset_y: float = 0.22 * player_height

    # Playeri koordinaatide arvutamine
    player_x: int = 2500 # random.randint(1 * block_size, 38 * block_size)
    player_y: int = 10100 # random.randint(40 * block_size, 77 * block_size)

    health_status     = None
    hunger_resistance = 0
    thirst_resistance = 0
    player_poisoned   = False
    player_infected   = False
    player_bleeding   = False
    serum_active      = False
    player_sprinting  = False

    # ******************** Screen ******************** #
    ui_elements: list = []

    loot = [
        #("Stick", (2, 5)),
        #("Stone_Shard", 1),
        #("Wood_Pickaxe", 1),
        #("Oak_Planks", (2, 3)),
        #("Small_Rock_Sword", 1),
        #("Oak_Planks", (2, 3)),
        #("Oak_Wood", (1, 2)),
        ("Flashlight", 1),
        ("Serum", 1),
        ("Bread", (2, 3)),
        ("Raw_Meat", (2, 3)),
        ("Bandage", (1, 4)),
        ("Bottle_Water", (2, 3)),
        ("Glowstick", (1, 3)),
        ("String", (1, 3)),

    ]

    # ******************** COLLISION ******************** #
    collision_boxes:    list = []  # terrain_x, terrain_y, collision_box_width, collision_box_height, object_id
    object_list:        list = []  # terrain_x, terrain_y, object_width, object_height, object_image, object_id

    # ******************** VISION ******************** #
    light_range: int = 420
    opposite_light_range: int = player_width // 1.5  # vision.py overwritib selle. Line 51 vmdgi
    walls: list = []  # Collision boxide seinad
    last_input: str = 'asd'  # See peab olema üks neist: [a, s, d, w], muidu annab errori - sest visionis tahab selle len() saada

    # ******************** MAZE ******************** #

    # General
    maze_counter: int = 1
    enemy_counter: int = 0

    # 0 col / row maze fix
    first_time = True

    # Final maze
    portal_frame_rect = None

    final_maze = False
    cutscene = False

    final_maze_key_slots: set = set()
    portal_list: list = []
    portal_frames: int = 0

    # Blade maze
    blades_spawned = False
    already_looped_blades = None

    # ******************** Render ******************** #
    map_list: list = [['block_maze'], ['glade']]

    blits_sequence_collision: list = []
    blits_sequence_objects: list = []
    text_sequence: list = []

    offset_x: int = 0
    offset_y: int = 0

    # ******************** Enemy ******************** #
    enemy_spawnpoint_list = set()
    enemy_detection_range = block_size * 20

    # Et ei arvutaks uut pathi 24/7 vaid arvutab seda seatud aja tagant
    enemy_path_update_tick = 5 + random.randint(15, 20)

    # ******************** Counters ******************** #
    render_boxes_counter: int = 0

    # ******************** Cooking ******************** #
    station_capacity = 24  # Max raw ja cooked item'ite kogus cooking station'is

    is_cooking: bool = False  # Invi lockimiseks
    cooking_range: int  # Muuda üleval -> 'debub | normal - mode'
    cooking_delay = 150  # Kaua läheb itemi cookimisega -> Default 300
    cooking_menu = False

    # ******************** Building ******************** #
    allow_building = True

    # ******************** Farming ******************** #
    farmable_stage_list = []


    # Avg Growth Time
    avg_growth_time_wheat   = 105  # (real - time)
    avg_growth_time_potato  = 90   # (real - time)
    avg_growth_time_corn    = 80   # (real - time)
    avg_growth_time_carrot  = 75   # (real - time)

    wheat_stage_growth_time = 20 * avg_growth_time_wheat  # Default: 75 * avg_growth_time_wheat
    wheat_minus_random_range = (0, wheat_stage_growth_time // 1.1)

    potato_stage_growth_time = avg_growth_time_potato * wheat_stage_growth_time // avg_growth_time_wheat
    potato_minus_random_range = (0, potato_stage_growth_time // 1.1)

    corn_stage_growth_time = avg_growth_time_corn * wheat_stage_growth_time // avg_growth_time_wheat
    corn_minus_random_range = (0, corn_stage_growth_time // 1.1)

    carrot_stage_growth_time = avg_growth_time_carrot * wheat_stage_growth_time // avg_growth_time_wheat
    carrot_minus_random_range = (0, carrot_stage_growth_time // 1.1)

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
