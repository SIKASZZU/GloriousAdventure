# when my code is returning values I can't even explain (theory can only take you so far) - Robert Oppenheimer

# Built-in, downloaded modules
import pygame
import sys
import os
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
from cooking import Cooking
from dropping import Drop
from entity import Entity
from equipped_items import ItemFunctionality
from event_handler import Event_handler
from final_maze import Final_Maze
from HUD import HUD_class
from interactions import Interaction
from inventory import Inventory
from loot import Loot
from map import MapData, glade_creation
from maze_changes import MazeChanges
from menu import Menu, PauseMenu
from objects import ObjectManagement
from render import RenderPictures, ObjectCreation
from status import PlayerEffect
from text import Fading_text
from update import EssentialsUpdate, PlayerUpdate, Framerate
from variables import UniversalVariables
from vision import Vision


jurigged.watch()  # hot reload


class Game:
    def __init__(self):
        self.game_menu_state = "main"
        self.pause_menu_state = "main"

        self.menu_states_tuple = (self.game_menu_state, self.pause_menu_state)

        self.dim_surface = pygame.Surface((UniversalVariables.screen_x, UniversalVariables.screen_y), pygame.SRCALPHA,
                                          32)

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

        self.player_attack_rect = None

        # initialize #
        self.initialize_pygame()  # Alati 1.
        self.terrain_data = glade_creation()

        self.initialize_player()
        self.initialize_building()
        self.initialize_essentials()
        self.initialize_camera()
        self.initialize_inventory()
        self.initialize_map()

        self.initialize_audio()
        self.initialize_collisons()
        self.initialize_vision()
        self.initialize_loot()

        # self.initialize_cooking()

        self.initialize_event_handler()

        self.initialize_attack()
        # FIXME: Cooking, Building -> Ei tööta

    def initialize_pygame(self):
        pygame.display.set_caption("Glorious Adventure - BETA")
        pygame.font.init()
        pygame.init()

        self.font = pygame.font.SysFont("Verdana", 20)
        self.screen = UniversalVariables.screen
        self.clock = pygame.time.Clock()  # FPS

        # audio #
        self.py_mixer = pygame.mixer.init()

    def initialize_camera(self):
        self.camera = Camera(self.screen, self.click_tuple, self.terrain_data, self.player_update)

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
        self.event_handler = Event_handler(self.click_tuple, self.camera, self.vision, self.inv, self.player, self.camera_click_tuple, self.terrain_data, self.loot, self.menu_states_tuple)

    def initialize_map(self):
        # FIXME: Playerit ei liiguta, aga collision v ghost liigutab siis ei update pilte ära ja on veits fucked up
        self.map_data = MapData(self.terrain_data, self.click_position, self.camera)

        # Blade maze
        self.maze_blades = Blades(self.terrain_data)

        # FIXME: Day/Night - Uksed lahti/kinni

        # for i in range(len(self.terrain_data)):
        #    for j in range(len(self.terrain_data[i])):
        #        if self.terrain_data[i][j] == 933:
        #            self.terrain_data[i - 1][j] = 98

    def initialize_attack(self):
        self.attack_entity = AttackEntity(self.inv, self.player_update)  # + self.entity
        self.attack_object = AttackObject(self.terrain_data, self.inv)
        self.attack = Attack(self.camera, self.attack_entity, self.attack_object, self.player_update)

    def initialize_audio(self):
        self.player_audio = Player_audio(self.terrain_data, self.player, self.py_mixer)
        self.tile_sounds = Tile_Sounds(self.py_mixer)

    # def initialize_cooking(self):
    #     self.cooking = Cooking(self.inv, self.camera, self.terrain_data, self.screen)

    def initialize_player(self):
        self.player_update = PlayerUpdate(self.terrain_data)
        self.player_update.player_rect = self.player_update.get_player_rect()

        self.player = Player(max_health=20, min_health=0,
                             max_stamina=20, min_stamina=0,
                             base_speed=6, max_speed=15, min_speed=1,
                             base_hunger=8, max_hunger=20, min_hunger=0,
                             base_thirst=12, max_thirst=20, min_thirst=0
                             )

        self.player_effect = PlayerEffect(self.player)

    def initialize_collisons(self):
        self.collisions = Collisions(self.player, self.player_update, self.terrain_data)

    def initialize_loot(self):
        self.loot = Loot(self.camera, self.inv, self.terrain_data, self.click_tuple)

    def initialize_building(self):
        self.building = Building()

    def initialize_inventory(self):
        self.inv = Inventory(self.camera, self.player_update)

    def initialize_essentials(self):
        self.framerate = Framerate()
        self.essentials = EssentialsUpdate(self.font, self.framerate)

    def initialize_vision(self):
        self.vision = Vision(self.screen, self.terrain_data, self.essentials.daylight_strength)

    def event_game_state(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def events(self):
        for event in pygame.event.get():
            self.event_game_state(event)
            self.event_handler.handle_mouse_events(event)
            self.event_handler.handle_keyboard_events(event)

    def load_variables(self):
        UniversalVariables()

    def render_boxes(self):
        if UniversalVariables.render_boxes_counter:
            ObjectManagement.render_interaction_box()
            ObjectManagement.render_collision_box()
            Drop.display_all_floating_pouch_hitboxes()

    def check_for_update(self):

        def hash_matrix(matrix):
            return hashlib.md5(str(matrix).encode()).hexdigest()

        if hash_matrix(self.terrain_data) != hash_matrix(self.old_terrain_data):
            UniversalVariables.update_view = True
            self.old_terrain_data = [row[:] for row in self.terrain_data]

    def call_technical(self):

        self.player_update.update_player(self.player)  # Update player position and attributes
        self.camera.box_target_camera(self.player_update.player_rect)  # Camera follow

        ObjectCreation.creating_lists(self)  # CREATE SOME FUCKING BITCHES FUCKING COLLISION BOX LIST AND OBJCET LIST

        self.collisions.collison_terrain_types()  # CHECK TERRAIN AND WATER Cadwasdwa
        Interaction.objects(self)  # CHECK TERRAIN AND WATER Cadwasdwa
        # MazeChanges.change_maze(self)

        Entity.update(self)
        Player_audio.player_audio_update(self)
        # change_blades(self)
        PlayerEffect.update(self)
        ItemFunctionality.update(self)

    def call_visuals(self):
        Game.check_for_update(self)
        RenderPictures.map_render(self)
        UniversalVariables.screen.blit(UniversalVariables.buffer_collision, (0, 0))

        RenderPictures.object_render(self)

        Drop.update(self)
        Game.render_boxes(self)  # et visual boxid oleksid objektide peal, peab see oleme renderitud p2rast object_renderit.

        Entity.spawn(self)

        # Cooking.cooking.update(self)

        self.essentials.calculate_daylight_strength()

        # ******************** # ↑ Kõik, mis on  visioni all ↑ # ******************** #

        self.vision.update(self.player_update.player_rect.center)

        # ******************** # ↓ Kõik, mis on visioni peal ↓ # ******************** #

        if self.inv.crafting_menu_open and not UniversalVariables.cooking_menu:
            self.inv.render_craftable_items()
            if not self.inv.craftable_items_display_rects and self.inv.crafting_menu_open:
                Fading_text.re_display_fading_text("Nothing to craft.")
                self.inv.crafting_menu_open = False

        self.attack.update()

        PlayerUpdate.render_HUD(self)  # Render HUD
        Drop.open_pouch(Drop.pouch_position)

        self.essentials.render_general()  # Render other elements
        HUD_class.update()

        self.inv.render_equipped_slot(UniversalVariables.current_equipped_item)  # Equipped item slot

        # self.building.update()

    def check_keys(self):
        Event_handler.check_pressed_keys(self)  # Check pressed keys

    def reset_lists(self):
        UniversalVariables.text_sequence = []
        UniversalVariables.blits_sequence_collision = []
        UniversalVariables.blits_sequence_objects = []

    def refresh_loop(self):
        Interaction.keylock = 0
        Game.add_counts()  # lisa countid juure uue loopi alguse puhul

        current_fps = self.clock.get_fps()
        if current_fps > 0:  # To avoid adding 0 FPS values
            UniversalVariables.fps_list.append(current_fps)
            if len(UniversalVariables.fps_list) > UniversalVariables.fps_list_max_size:
                UniversalVariables.fps_list.pop(0)  # Remove the oldest FPS value if we exceed max size

        if UniversalVariables.fps_lock:
            FPS = 60
        else: FPS = UniversalVariables.FPS
        self.clock.tick(FPS)

    @staticmethod
    def add_counts():
        if UniversalVariables.interaction_delay <= UniversalVariables.interaction_delay_max:
            UniversalVariables.interaction_delay += 1

    def custom_addition(self):
        if UniversalVariables.debug_mode:
            if not self.restrict_looping:
                ObjectManagement.add_object_from_inv(self, "Maze_Key", 30)
                # ObajectManagement.add_object_from_inv("Bandage", 100)
                self.restrict_looping = True

    def logic(self):
        self.reset_lists()
        self.call_technical()
        self.call_visuals()
        self.refresh_loop()

        self.inv.call()

        Final_Maze.update(self)
        Fading_text.update(self)
        self.player.update()

        self.check_keys()  # Toggle hitbox / vision
        self.custom_addition()

        self.click_position = ()
        pygame.display.update()

        # ******************** DEBUG MODE ******************** #
        if UniversalVariables.debug_mode:
            UniversalVariables.ui_elements.append("!        Debug mode - True        !")
            self.player.speed.base_speed = 20

            # UniversalVariables.player_x, UniversalVariables.player_y = 2800, 8600  # FPS'side testimiseks
            # print(self.player)


    def state(self):

        # Vaatab kas mäng on tööle pandud või mitte
        if Menu.game_state:
            Menu.main_menu(self)
            return True

        # Vaatab kas mäng on pausi peale pandud või mitte
        if PauseMenu.game_paused:
            PauseMenu.settings_menu(self)
            return True

        return False


    def run(self):
        self.load_variables()
        while True:
            self.events()

            if self.state() == True:  continue

            self.logic()
