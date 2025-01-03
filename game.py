# when my code is returning values I can't even explain (theory can only take you so far) - Robert Oppenheimer

# Built-in, downloaded modules
import pygame
import sys
import jurigged
import hashlib

# Other modules
from attack import Attack, AttackEntity, AttackObject
from audio import Player_audio, Tile_Sounds
from blade import Blades
from building import Building
from camera import Camera
from collisions import Collisions
from components import Player
from dropping import Drop
from entity import Entity
from equipped_items import ItemFunctionality
from event_handler import Event_handler
from final_maze import Final_Maze
from functions import UniversalFunctions
from HUD import HUD_class
from interactions import Interaction
from images import ImageLoader
from inventory import Inventory
from loot import Loot
from map import MapData, glade_creation
from mazecalculation import AddingMazeAtPosition
from maze_changes import MazeChanges
from menu import Menu, PauseMenu
from objects import ObjectManagement
from render import RenderPictures, ObjectCreation
from status import PlayerEffect
from text import Fading_text
from tile_set import TileSet
from update import EssentialsUpdate, PlayerUpdate, Framerate
from variables import UniversalVariables, GameConfig
from vision import Vision



jurigged.watch()  # hot reload


class Game:
    def __init__(self):

        # TODO: Booli vms teha, mis jägib evente nt click vms ja kui bool muutub trues ss updateb mappi aka render()

        self.game_menu_state = "main"
        self.pause_menu_state = "main"

        self.menu_states_tuple = (self.game_menu_state, self.pause_menu_state)

        self.print_hp = 0
        self.restrict_looping = False

        self.old_terrain_data = None
        self.click_position = ()
        self.click_window_x = None
        self.click_window_y = None

        self.right_click_position = ()
        self.right_click_window_x = None
        self.right_click_window_y = None

        self.click_tuple = (
            self.click_position,
            self.click_window_x,
            self.click_window_y,
            self.right_click_position,
            self.right_click_window_x,
            self.right_click_window_y
        )

        # initialize #
        self.initialize_variables()
        self.initialize_pygame()  # Alati 1.


        self.terrain_data = glade_creation()
        self.initialize_image_loader()

        self.initialize_fading_text()
        self.initialize_player()
        self.initialize_hud() # enne collisoni ja playerit
        # self.initialize_building()
        self.initialize_essentials()
        self.initialize_functions()
        self.initialize_camera()
        
        self.initialize_inventory()
        self.initialize_map()

        self.initialize_audio()

        self.initialize_tile_set()
        self.initialize_render()
        
        self.initialize_collisions()
        self.initialize_vision()


        # self.initialize_cooking()
        self.initialize_maze_changes()

        self.initialize_final_maze()
        self.initialize_object_creation()

        self.initialize_object_management()
        self.initialize_drop()
        self.initialize_entity()
        self.initialize_attack()
        self.initialize_item_func()
        self.initialize_maze_addition()
        self.initialize_loot()
        self.initialize_interactions()
        self.initialize_event_handler()

        self.initialize_menus()

        # FIXME: Cooking, Building -> Ei tööta

    def initialize_pygame(self):
        pygame.display.set_caption("Glorious Adventure - BETA")
        pygame.font.init()
        pygame.init()

        self.font = pygame.font.SysFont("Verdana", 20)
        self.screen = self.variables.screen
        self.clock = pygame.time.Clock()  # FPS
        self.dim_surface = pygame.Surface((self.variables.screen_x, self.variables.screen_y), pygame.SRCALPHA,
                                          32)
        # audio #
        self.py_mixer = pygame.mixer.init()

    def initialize_camera(self):
        self.camera = Camera(self.screen, self.click_tuple, self.terrain_data, self.player_update, self.fading_text, self.variables, self.functions)

        self.camera_rect = self.camera.camera_rect
        self.player_window_x = self.camera.player_window_x
        self.player_window_y = self.camera.player_window_y
        self.click_x = self.camera.click_x
        self.click_y = self.camera.click_y

        self.camera_click_tuple = (
            self.camera_rect,
            self.player_window_x,
            self.player_window_y,
            self.click_x,
            self.click_y
        )

    # See peaks olema pmst nii, et kui sa paned self.event_handler siis ta vaatab event_handler,
    # aga kui sa paned lic self siis ta vaatab seda classi, kus sa parasjagu oled.

    def initialize_event_handler(self):
        self.event_handler = Event_handler(self.camera, self.vision, self.inv, self.player, self.terrain_data,
                                           self.loot, self.menu_states_tuple, self.variables)

    def initialize_map(self):
        # FIXME: Playerit ei liiguta, aga collision v ghost liigutab siis ei update pilte ära ja on veits fucked up
        self.map_data = MapData(self.terrain_data, self.camera, self.variables, self.CLOSED_DOOR_IDS)

        # Blade maze
        self.maze_blades = Blades(self.terrain_data, self.essentials, self.variables)

        # FIXME: Day/Night - Uksed lahti/kinni

        # for i in range(len(self.terrain_data)):
        #    for j in range(len(self.terrain_data[i])):
        #        if self.terrain_data[i][j] == 933:
        #            self.terrain_data[i - 1][j] = 98

    def initialize_attack(self):
        self.attack_entity = AttackEntity(self.inv, self.player_update, self.entity, self.variables)
        self.attack_object = AttackObject(self.terrain_data, self.inv, self.variables, self.object_management)
        self.attack = Attack(self.camera, self.attack_entity, self.attack_object, self.player_update,
                             self.object_management, self.variables)

    def initialize_audio(self):
        self.player_audio = Player_audio(self.terrain_data, self.player, self.py_mixer, self.variables)
        self.tile_sounds = Tile_Sounds(self.py_mixer, self.variables)

    # def initialize_cooking(self):
    #     self.cooking = Cooking(self.inv, self.camera, self.terrain_data, self.screen)

    def initialize_player(self):
        self.player_update = PlayerUpdate(self.terrain_data, self.variables)
        self.player_update.player_rect = self.player_update.get_player_rect()

        self.player = Player(max_health=20, min_health=0,
                             max_stamina=20, min_stamina=0,
                             base_speed=6, max_speed=15, min_speed=1,
                             base_hunger=8, max_hunger=20, min_hunger=0,
                             base_thirst=12, max_thirst=20, min_thirst=0,
                             fading_text=self.fading_text, variables=self.variables)

        self.player_effect = PlayerEffect(self.player, self.variables)

    def initialize_collisions(self):
        self.collisions = Collisions(self.player, self.player_update, self.terrain_data, self.hud, self.render,
                                     self.variables, self.COLLISION_ITEMS)

    def initialize_loot(self):
        self.loot = Loot(self.camera, self.inv, self.terrain_data, self.fading_text,
                         self.object_management, self.variables, self.player_update, self.screen)

    def initialize_building(self):
        self.building = Building(self.variables, self.camera, self.terrain_data, self.player_audio,
                                 self.object_management)

    def initialize_inventory(self):
        self.inv = Inventory(self.camera, self.player_update, self.image_loader, self.fading_text, self.variables)

    def initialize_essentials(self):
        self.framerate = Framerate(self.variables)
        self.essentials = EssentialsUpdate(self.font, self.framerate, self.variables)

    def initialize_vision(self):
        self.vision = Vision(self.screen, self.terrain_data, self.essentials.daylight_strength, self.variables, self.RENDER_RANGE_SMALL)

    def initialize_maze_changes(self):
        self.maze_changes = MazeChanges(self.essentials.day_night_text, self.variables)

    def initialize_entity(self):
        self.entity = Entity(self.terrain_data, self.camera, self.player_update, self.essentials, self.player,
                             self.player_effect, self.inv, self.image_loader, self.object_management, self.variables, self.ALL_THE_DOORS, self.GLADE_ITEMS)

    def initialize_item_func(self):
        self.item_func = ItemFunctionality(self.terrain_data, self.entity, self.player, self.player_audio,
                                           self.player_update, self.camera, self.inv, self.fading_text,
                                           self.object_management, self.variables, self.CLOSED_DOOR_IDS, self.functions)

    def initialize_interactions(self):
        self.interaction = Interaction(self.player_update, self.player_audio, self.tile_sounds, self.terrain_data,
                                       self.camera, self.inv, self.essentials, self.map_data, self.fading_text,
                                       self.maze_addition, self.object_management, self.variables, self.CLOSED_DOOR_IDS,
                                       self.loot)

    def initialize_drop(self):
        self.drop = Drop(self.player_update, self.inv, self.image_loader, self.object_management, self.variables)

    def initialize_hud(self):
        self.hud = HUD_class(self.player, self.image_loader, self.variables)

    def initialize_image_loader(self):
        self.image_loader = ImageLoader(self.variables)

    def initialize_final_maze(self):
        self.final_maze = Final_Maze(self.terrain_data, self.tile_sounds, self.render, self.variables)

    def initialize_render(self):
        self.render = RenderPictures(self.player_update, self.image_loader, self.camera, self.terrain_data,
                                    self.click_tuple, self.tile_set, self.variables, self.GROUND_IMAGE, self.MAZE_GROUND_IMAGE, self.COLLISION_ITEMS,
                                    self.FARMLAND_IMAGE, self.OBJECT_RENDER_ORDER, self.WHEAT_STAGES, self.CARROT_STAGES, self.CORN_STAGES, self.POTATO_STAGES, self.FARMABLES)

    def initialize_object_creation(self):
        self.object_creation = ObjectCreation(self.render, self.image_loader, self.terrain_data, self.variables, self.COLLISION_ITEMS, self.INTERACTABLE_ITEMS)

    def initialize_fading_text(self):
        self.fading_text = Fading_text(self.screen, self.variables)

    def initialize_tile_set(self):
        self.tile_set = TileSet(self.image_loader, self.terrain_data)

    def initialize_maze_addition(self):
        self.maze_addition = AddingMazeAtPosition(self.fading_text, self.map_data, self.terrain_data, self.inv,
                                                  self.camera, self.object_management, self.variables)

    def initialize_object_management(self):
        self.object_management = ObjectManagement(self.inv, self.fading_text, self.player_audio, self.terrain_data,
                                                  self.variables, self.COOKING_STATIONS)

    def initialize_variables(self):
        self.variables = UniversalVariables()
        
        self.initialize_config()
        
    def initialize_config(self):
        self.OBJECT_RENDER_ORDER = GameConfig.OBJECT_RENDER_ORDER
        self.RANDOM_PLACEMENT = GameConfig.RANDOM_PLACEMENT
        self.INITIAL_GLADE_ITEMS = GameConfig.INITIAL_GLADE_ITEMS
        self.FARMABLES = GameConfig.FARMABLES
        self.WHEAT_STAGES = GameConfig.WHEAT_STAGES
        self.CARROT_STAGES = GameConfig.CARROT_STAGES
        self.CORN_STAGES = GameConfig.CORN_STAGES
        self.POTATO_STAGES = GameConfig.POTATO_STAGES
        self.FARMABLE_STAGES = GameConfig.FARMABLE_STAGES
        self.FARMLAND_IMAGE = GameConfig.FARMLAND_IMAGE
        self.GROUND_IMAGE = GameConfig.GROUND_IMAGE
        self.MAZE_GROUND_IMAGE = GameConfig.MAZE_GROUND_IMAGE
        self.OPEN_DOOR_IDS = GameConfig.OPEN_DOOR_IDS
        self.CLOSED_DOOR_IDS = GameConfig.CLOSED_DOOR_IDS
        self.ALL_THE_DOORS = GameConfig.ALL_THE_DOORS
        self.GLADE_ITEMS = GameConfig.GLADE_ITEMS
        self.ABND_GLADE_ITEMS = GameConfig.ABND_GLADE_ITEMS
        self.BERRY_ITEMS = GameConfig.BERRY_ITEMS
        self.INTERACTABLE_ITEMS = GameConfig.INTERACTABLE_ITEMS
        self.COLLISION_ITEMS = GameConfig.COLLISION_ITEMS
        self.RENDER_RANGE_SMALL = GameConfig.RENDER_RANGE_SMALL
        self.COOKING_STATIONS = GameConfig.COOKING_STATIONS

    def initialize_menus(self):
        self.menu = Menu(self.variables)
        self.pmenu = PauseMenu(self.variables)

    def initialize_functions(self):
        self.functions = UniversalFunctions(self.terrain_data, self.variables)


    def event_game_state(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def events(self):
        for event in pygame.event.get():
            self.event_game_state(event)
            self.event_handler.handle_mouse_events(event)
            self.event_handler.handle_keyboard_events(event)

    def render_boxes(self):
        if self.variables.render_boxes_counter:
            self.object_management.render_interaction_box(self.variables.object_list, self.variables.screen)
            self.object_management.render_collision_box(self.variables.collision_boxes)
            self.drop.display_all_floating_pouch_hitboxes()

    def check_for_update(self):
        def hash_matrix(matrix):
            return hashlib.md5(str(matrix).encode()).hexdigest()

        if hash_matrix(self.terrain_data) != hash_matrix(self.old_terrain_data):
            self.variables.update_view = True
            self.old_terrain_data = [row[:] for row in self.terrain_data]
            # self.variables.buffer_collision = []

    def call_technical(self):
        self.player_update.update_player(self.player)  # Update player position and attributes
        self.camera.box_target_camera(self.player_update.player_rect)  # Camera follow

        self.object_creation.creating_lists()  # CREATE SOME FUCKING BITCHES FUCKING COLLISION BOX LIST AND OBJCET LIST

        self.collisions.collison_terrain_types()  # CHECK TERRAIN AND WATER
        self.interaction.objects()  # CHECK TERRAIN AND WATER
        self.maze_changes.change_maze()

        self.entity.update()
        self.player_audio.player_audio_update()
        self.maze_blades.change_blades()
        self.player_effect.update()
        self.item_func.update()

    def call_visuals(self):
        self.render.map_render()
        self.variables.screen.blit(self.variables.buffer_collision, (0, 0))

        self.render.object_render()

        self.drop.update()
        self.render_boxes()  # et visual boxid oleksid objektide peal, peab see oleme renderitud p2rast object_renderit.

        self.entity.spawn()

        # Cooking.cooking.update(self)

        self.essentials.calculate_daylight_strength()

        # ******************** # ↑ Kõik, mis on  visioni all ↑ # ******************** #

        self.vision.update(self.player_update.player_rect.center)

        # ******************** # ↓ Kõik, mis on visioni peal ↓ # ******************** #

        if self.inv.crafting_menu_open and not self.variables.cooking_menu:
            self.inv.render_craftable_items()
            if not self.inv.craftable_items_display_rects and self.inv.crafting_menu_open:
                self.fading_text.re_display_fading_text("Nothing to craft.")
                self.inv.crafting_menu_open = False

        self.attack.update()

        self.drop.open_pouch(self.drop.pouch_position)

        self.essentials.render_general()  # Render other elements
        self.hud.update()

        self.inv.render_equipped_slot(self.variables.current_equipped_item)  # Equipped item slot
        # self.building.update()

        self.check_for_update()  # Callida viimase asjana, muidu ei update map'pi ära
    def check_keys(self):
        self.event_handler.check_pressed_keys()  # Check pressed keys

    def reset_lists(self):
        self.variables.text_sequence = []
        self.variables.blits_sequence_collision = []
        self.variables.blits_sequence_objects = []

    def refresh_loop(self):
        self.interaction.keylock = 0
        self.add_counts()  # lisa countid juure uue loopi alguse puhul

        current_fps = self.clock.get_fps()
        if current_fps > 0:  # To avoid adding 0 FPS values
            self.variables.fps_list.append(current_fps)
            if len(self.variables.fps_list) > self.variables.fps_list_max_size:
                self.variables.fps_list.pop(0)  # Remove the oldest FPS value if we exceed max size

        if self.variables.fps_lock:
            FPS = 60
        else: FPS = self.variables.FPS
        self.clock.tick(FPS)

    def add_counts(self):
        if self.variables.interaction_delay <= self.variables.interaction_delay_max:
            self.variables.interaction_delay += 1

    def custom_addition(self):
        if self.variables.debug_mode:
            if not self.restrict_looping:
                self.object_management.add_object_from_inv("Maze_Key", 30)
                # ObajectManagement.add_object_from_inv("Bandage", 100)
                self.restrict_looping = True

    def logic(self):
        self.reset_lists()
        self.call_technical()
        self.call_visuals()
        self.refresh_loop()

        self.inv.call()

        self.final_maze.update()
        self.fading_text.update()
        self.player.update()

        self.check_keys()  # Toggle hitbox / vision
        self.custom_addition()

        self.camera.reset_clicks()  # LOOPi lopus reset clicks
        pygame.display.update()

        # ******************** DEBUG MODE ******************** #
        if self.variables.debug_mode:
            self.variables.ui_elements.append("!        Debug mode - True        !")
            self.player.speed.base_speed = 20

            # self.variables.player_x, self.variables.player_y = 2800, 8600  # FPS'side testimiseks
            # print(self.player)


    def state(self):

        # Vaatab kas mäng on tööle pandud või mitte
        if self.menu.game_state:
            self.menu.main_menu()
            return True

        # Vaatab kas mäng on pausi peale pandud või mitte
        if self.pmenu.game_paused:
            self.pmenu.settings_menu()
            return True

        return False


    def run(self):
        while True:
            self.events()
            if self.state() == True:  
                continue
            self.logic()
