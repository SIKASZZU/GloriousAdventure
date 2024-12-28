import random
import pygame

from enum import Enum


class GameConfig(Enum):
    # Render: wheat -> rock -> stump -> tree
    OBJECT_RENDER_ORDER: tuple[int, ...] = (7, 2, 5, 4)

    RANDOM_PLACEMENT: tuple[int, ...] = (2, 4, 5, 10, 12, 13, 1001, 1002, 1003)  # Random position items

    INITIAL_GLADE_ITEMS : tuple[int, ...] = (1, 2, 3, 4, 5, 8, 9, 708)

    FARMABLES           : tuple[int, ...] = (7, 71, 74, 77)
    WHEAT_STAGES        : tuple[int, ...] = (69, 70)
    CARROT_STAGES        : tuple[int, ...] = (75, 76)
    CORN_STAGES         : tuple[int, ...] = (78, 79)
    POTATO_STAGES       : tuple[int, ...] = (72, 73)

    FARMABLE_STAGES     : tuple[int, ...] = WHEAT_STAGES + CARROT_STAGES + CORN_STAGES  + POTATO_STAGES

    FARMLAND_IMAGE      : tuple[int, ...] = FARMABLES + FARMABLE_STAGES + (107, )

    GROUND_IMAGE        : tuple[int, ...] = INITIAL_GLADE_ITEMS + tuple(id for id in range(1004, 1017))  # GLADE_ITEMS + 1004 -> 1015
    MAZE_GROUND_IMAGE   : tuple[int, ...] = (
        # 6,                      # String
        10, 12, 13,             # Maze Keys
        90, 91, 92, 93, 933,    # Maze Doors
        98,                     # Maze Ground
        1001, 1002, 1003,       # Barrel, Chest
    )

    OPEN_DOOR_IDS: tuple[int, ...] = (90, 91, 92, 93, 933)
    CLOSED_DOOR_IDS: tuple[int, ...] = (94, 95, 96, 97, 977)
    ALL_THE_DOORS: tuple[int, ...] = OPEN_DOOR_IDS + CLOSED_DOOR_IDS  # Combine the tuples

    GLADE_ITEMS         : tuple[int, ...] = INITIAL_GLADE_ITEMS + FARMABLES
    ABND_GLADE_ITEMS    : tuple[int, ...] = (1004, 1005, 1006)
    BERRY_ITEMS         : tuple[int, ...] = (1008, 1010, 1012, 1013, 1015, 1016)
    
    # TODO: interactalbe itemid on siis objekt itemid? K6ik objekt itemid ei ole ju interactable? mdea.. hetkel k6ik interactable itemid renderib object_renderer.
    INTERACTABLE_ITEMS  : tuple[int, ...] = (2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 981, 982, 1001, 1002, 708) + ALL_THE_DOORS + BERRY_ITEMS + ABND_GLADE_ITEMS # ei renderi topelt map_renderi all
    COLLISION_ITEMS     : tuple[int, ...] = (99, 981, 982)

    RENDER_RANGE_SMALL  : tuple[int, ...] = (
        10, 11, 12, 13,                                 # Key
        90, 91, 92, 93, 93, 94, 95, 96, 97, 933, 977,   # Uksed
        98, 99,                                         # Ground ja Wall
        981, 982,                                       # Keyholder
        1001, 1002, 1003,                               # Barrel, Chest
        989, 98998, 9099, 909998, 900                   # Blade walls, Grounds
    )

    COOKING_STATIONS: tuple[int, ...] = (8, )  # Campfire

class UniversalVariables():

    debug_mode = True

    # ******************** Settings ******************** #

    # Windowi suurus x, y
    screen_x: int = 1366  # 1024 × 576 | 1152 × 648 | 1280 × 720 (HD) | 1366 × 768 | 1600 × 900 | 1920 × 1080 (full HD) | 2560 × 1440 | 3840 × 2160 (4K UHD)
    screen_y: int = 768

    # Mängu max tick rate

    # ******************** Screen ******************** #
    screen = pygame.display.set_mode((screen_x, screen_y))

    # Double buffering, flickerimise fiximiseks
    buffer_collision = pygame.Surface(screen.get_size())
    buffer_collision = buffer_collision.convert()

    buffer_objects = pygame.Surface(screen.get_size())
    buffer_objects = buffer_objects.convert()

    # Effectide suurused
    icon_width: int = 60
    icon_height: int = 60

    fps_list = []
    fps_list_max_size = 1000  # Limit the size of fps_list, avg tekib ka selle listi jargi.
    fps_lock = False

    # Block size muutmiseks kui zoomitakse sisse või välja
    prev_block_size: int = 0

    if debug_mode:
        jagatis: float = 10

        game_minute_lenght = 5

        # Mängu heli tugevus
        sound_volume: int = 0

        # Mängu max tick rate
        FPS: int = 200

        block_size: int = screen_x // jagatis
        player_range: int = block_size * 15

        entity_speed: float = 0.05  # entity kiirus grid size'ina

        cooking_range:int = 5  # Grid


    else:
        jagatis: float = 10

        game_minute_lenght = 75

        # Mängu heli tugevus
        sound_volume: int = 0.1

        # Mängu max tick rate
        FPS: int = 60

        block_size: int = screen_x // jagatis
        player_range: int = block_size * 1.5

        entity_speed: float = 0.03  # entity kiirus grid size'ina

        cooking_range:int = 2  # Grid

    # ******************** Dropping ******************** #
    items_to_drop = {}
    dropped_items: dict = {}
    despawn_timer_default: int = 800  # Dropped itemite despawn timer

    # ******************** Attacking ******************** #
    object_hp_dict: dict = {}
    object_reset_timer: int = 200  # Kui reset timer jõuab 0 siis kaob 'object_hp_dict' ära

    # ******************** PLAYER ******************** #
    animation_index = 2

    current_equipped_item = None
    current_equipped_item_item_type = None
    interaction_delay = 100  # Delay tegevuse vahel, näiteks söömine, ehitamine, asjade ülesse võtmine
    interaction_delay_max = interaction_delay


    player_height_factor  = 0.45
    player_width_factor   = 0.45
    player_height: int = block_size * player_height_factor
    player_width:  int = block_size * player_width_factor

    player_hitbox_offset_x: float = 0.29 * player_width
    player_hitbox_offset_y: float = 0.22 * player_height

    # Playeri koordinaatide arvutamine
    # Player_x/_y ei ole offsetti lisatud
    player_x: int = 2500 # random.randint(1 * block_size, 38 * block_size)
    player_y: int = 10100 # random.randint(40 * block_size, 77 * block_size)

    health_status      = None
    hunger_resistance  = 0
    thirst_resistance  = 0
    player_poisoned    = False
    player_infected    = False
    player_bleeding    = False
    serum_active       = False
    player_sprinting   = False
    player_sneaking    = False
    attack_key_pressed = (False, (False, False, False, False))  # [0] bool TRUE if pressed, [1] tuple, and which arrow key is pressed: up, down, left, right
    allow_movement     = True
    render_after       = bool  # Vajalik teadmiseks kas player renderida enne v6i p2rast objekte


    player_damage: float = 2

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
    base_light_range: int = 420
    base_opposite_light_range: int = player_width

    light_range: int = 420
    opposite_light_range: int = player_width

    walls: list = []  # Collision boxide seinad
    last_input: str = 'asd'  # See peab olema üks neist: [a, s, d, w], muidu annab errori - sest visionis tahab selle len() saada

    # ******************** MAZE ******************** #

    # General
    maze_counter: int = 1
    entity_counter: int = 0

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
    update_view = True
    
    # ******************** entity ******************** #
    entity_spawnpoint_list = set()

    # Et ei arvutaks uut pathi 24/7 vaid arvutab seda seatud aja tagant
    entity_path_update_tick = 5 + random.randint(15, 20)

    ghost_hp = 8

    # ******************** Counters ******************** #
    render_boxes_counter: bool = True

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

    # ******************** Items ******************** #
    geiger_chosen_grid = None

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
        UniversalVariables.entity_spawnpoint_list = set()  # resetib ka ikka selle sitajunni
        if terrain_data is not None:
            spawnpoints = set()
            for row in range(len(terrain_data)):
                for column in range(len(terrain_data[row])):
                    if terrain_data[row][column] == 98:
                        spawnpoints.add((row, column))

            count = 0
            for spawnpoint in spawnpoints:

                if count < 10 * UniversalVariables.maze_counter and spawnpoint not in UniversalVariables.entity_spawnpoint_list:
                    UniversalVariables.entity_spawnpoint_list.add(spawnpoint)
                    count += 1
                else:
                    break

    @staticmethod
    def print_debug_text(text: any):
        if UniversalVariables.debug_mode:
            print(text)
