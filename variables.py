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

    def __init__(self):
            

        self.debug_mode = True

        # ******************** Settings ******************** #

        # Windowi suurus x, y
        # 1024 × 576 | 1152 × 648 | 1280 × 720 (HD) | 1366 × 768 | 1600 × 900 | 1920 × 1080 (full HD) | 2560 × 1440
        resolution_tuple = ((1024, 576), (1152, 648), (1280, 720), (1366, 768), (1600, 900), (1920, 1080), (2560, 1440))
        CHOOSE_RESOLUTION = resolution_tuple[2]
        self.screen_x: int = CHOOSE_RESOLUTION[0]
        self.screen_y: int = CHOOSE_RESOLUTION[1]

        # Mängu max tick rate

        # ******************** Screen ******************** #
        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y))

        # Double buffering, flickerimise fiximiseks
        self.buffer_collision = pygame.Surface(self.screen.get_size())
        self.buffer_collision = self.buffer_collision.convert()

        self.buffer_objects = pygame.Surface(self.screen.get_size())
        self.buffer_objects = self.buffer_objects.convert()

        # Effectide suurused
        self.icon_width: int = 60
        self.icon_height: int = 60

        self.fps_list = []
        self.fps_list_max_size = 1000  # Limit the size of fps_list, avg tekib ka selle listi jargi.
        self.fps_lock = False

        # Block size muutmiseks kui zoomitakse sisse või välja
        self.prev_block_size: int = 0

        if self.debug_mode:
            jagatis: float = 10

            self.game_minute_lenght = 5

            # Mängu heli tugevus
            self.sound_volume: int = 0

            # Mängu max tick rate
            self.FPS: int = 200

            self.block_size: float = self.screen_x // jagatis
            self.player_range: float = self.block_size * 15

            self.entity_speed: float = 0.05  # entity kiirus grid size'ina

            self.cooking_range: float = 5  # Grid


        else:
            jagatis: float = 10

            self.game_minute_lenght = 75

            # Mängu heli tugevus
            self.sound_volume: float = 0.1

            # Mängu max tick rate
            self.FPS: int = 60

            self.block_size: float = self.screen_x // jagatis
            self.player_range: float = self.block_size * 1.5

            self.entity_speed: float = 0.03  # entity kiirus grid size'ina

            self.cooking_range:int = 2  # Grid

        # ******************** Dropping ******************** #
        self.items_to_drop = {}
        self.dropped_items: dict = {}
        self.despawn_timer_default: int = 800  # Dropped itemite despawn timer

        # ******************** Attacking ******************** #
        self.object_hp_dict: dict = {}
        self.object_reset_timer: int = 200  # Kui reset timer jõuab 0 siis kaob 'object_hp_dict' ära

        # ******************** PLAYER ******************** #
        self.animation_index = 2

        self.current_equipped_item = None
        self.current_equipped_item_item_type = None
        self.interaction_delay = 100  # Delay tegevuse vahel, näiteks söömine, ehitamine, asjade ülesse võtmine
        self.interaction_delay_max = self.interaction_delay


        self.player_height_factor = 0.45
        self.player_width_factor = 0.45
        self.player_height: float = self.block_size * self.player_height_factor
        self.player_width:  float = self.block_size * self.player_width_factor

        self.player_hitbox_offset_x: float = 0.29 * self.player_width
        self.player_hitbox_offset_y: float = 0.22 * self.player_height

        # Playeri koordinaatide arvutamine
        # Player_x/_y ei ole offsetti lisatud
        self.player_x: int = 2500 # random.randint(1 * block_size, 38 * block_size)
        self.player_y: int = 1010 # random.randint(40 * block_size, 77 * block_size)

        self.health_status     = None
        self.hunger_resistance = 0
        self.thirst_resistance = 0
        self.player_poisoned   = False
        self.player_infected   = False
        self.player_bleeding   = False
        self.serum_active      = False
        
        self.player_sprinting = False
        self.player_sneaking  = False
        self.player_walking   = False
        self.player_standing  = False

        self.attack_key_pressed = (False, (False, False, False, False))  # [0] bool TRUE if pressed, [1] tuple, and which arrow key is pressed: up, down, left, right
        self.allow_movement     = True
        self.render_after       = bool  # Vajalik teadmiseks kas player renderida enne v6i p2rast objekte


        self.player_damage: float = 2

        # ******************** Screen ******************** #
        self.ui_elements: list = []

        self.loot = [
            # ("Stick", (2, 5)),
            # ("Stone_Shard", 1),
            # ("Wood_Pickaxe", 1),
            # ("Oak_Planks", (2, 3)),
            # ("Small_Rock_Sword", 1),
            # ("Oak_Planks", (2, 3)),
            # ("Oak_Wood", (1, 2)),
            # ("Flashlight", 1),
            # ("Serum", 1),
            ("Bread", (2, 3)),
            # ("Raw_Meat", (2, 3)),
            # ("Bandage", (1, 4)),
            # ("Bottle_Water", (2, 3)),
            # ("Glowstick", (1, 3)),
            # ("String", (1, 3)),

        ]

        # ******************** COLLISION ******************** #
        self.collision_boxes:    list = []  # terrain_x, terrain_y, collision_box_width, collision_box_height, object_id
        self.object_list:        list = []  # terrain_x, terrain_y, object_width, object_height, object_image, object_id

        # ******************** VISION ******************** #
        self.base_light_range: int = 420
        self.base_opposite_light_range: int = self.player_width

        self.light_range: int = 420
        self.opposite_light_range: int = self.player_width

        self.walls: list = []  # Collision boxide seinad
        self.last_input: str = 's'  # See peab olema üks neist: [a, s, d, w], muidu annab errori - sest visionis tahab selle len() saada

        # ******************** MAZE ******************** #

        # General
        self.maze_counter: int = 0
        self.entity_counter: int = 0

        # 0 col / row maze fix
        self.first_time = True

        # Final maze
        self.portal_frame_rect = None

        self.final_maze = False
        self.cutscene = False

        self.final_maze_key_slots: set = set()
        self.portal_list: list = []
        self.portal_frames: int = 0

        # Blade maze
        self.blades_spawned = False
        self.already_looped_blades = None

        # ******************** Render ******************** #
        self.map_list: list = [['glade']]

        self.blits_sequence_collision: list = []
        self.blits_sequence_objects: list = []
        self.text_sequence: list = []

        self.offset_x: int = 0
        self.offset_y: int = 0
        self.update_view = True
        
        # ******************** entity ******************** #
        self.entity_spawnpoint_list = set()

        # Et ei arvutaks uut pathi 24/7 vaid arvutab seda seatud aja tagant
        self.entity_path_update_tick = 5 + random.randint(15, 20)

        self.ghost_hp = 8

        # ******************** Counters ******************** #
        self.render_boxes_counter: bool = True

        # ******************** Cooking ******************** #
        self.station_capacity = 24  # Max raw ja cooked item'ite kogus cooking station'is

        self.is_cooking: bool = False  # Invi lockimiseks
        self.cooking_range: int  # Muuda üleval -> 'debub | normal - mode'
        self.cooking_delay = 150  # Kaua läheb itemi cookimisega -> Default 300
        self.cooking_menu = False

        # ******************** Building ******************** #
        self.allow_building = True

        # ******************** Farming ******************** #
        self.farmable_stage_list = []

        # ******************** Items ******************** #
        self.geiger_chosen_grid = None

        # Avg Growth Time
        self.avg_growth_time_wheat   = 105  # (real - time)
        self.avg_growth_time_potato  = 90   # (real - time)
        self.avg_growth_time_corn    = 80   # (real - time)
        self.avg_growth_time_carrot  = 75   # (real - time)

        self.wheat_stage_growth_time = 20 * self.avg_growth_time_wheat  # Default: 75 * avg_growth_time_wheat
        self.wheat_minus_random_range = (0, self.wheat_stage_growth_time // 1.1)

        self.potato_stage_growth_time = self.avg_growth_time_potato * self.wheat_stage_growth_time // self.avg_growth_time_wheat
        self.potato_minus_random_range = (0, self.potato_stage_growth_time // 1.1)

        self.corn_stage_growth_time = self.avg_growth_time_corn * self.wheat_stage_growth_time // self.avg_growth_time_wheat
        self.corn_minus_random_range = (0, self.corn_stage_growth_time // 1.1)

        self.carrot_stage_growth_time = self.avg_growth_time_carrot * self.wheat_stage_growth_time // self.avg_growth_time_wheat
        self.carrot_minus_random_range = (0, self.carrot_stage_growth_time // 1.1)