# when my code is returning values I can't even explain (theory can only take you so far) - Robert Oppenheimer

import pygame
import sys
import os
import jurigged

jurigged.watch()  # hot reload

# Import other modules
import vision
from entity import Enemy
from variables import UniversalVariables
from camera import Camera  # box_target_camera
from render import RenderPictures, ObjectCreation  # render, creating_lists
from event_handler import Event_handler
from map import MapData  # glade_creation, map_list_to_map
from objects import ObjectManagement  # place_and_render_object
from update import EssentialsUpdate, PlayerUpdate
from inventory import Inventory  # handle_mouse_click, render_craftable_items
from collisions import Collisions  # check_collisions, collision_terrain, collision_hitbox
from audio import Player_audio  # player_audio_update
from components import Player
from blade import change_blades
from final_maze import Final_Maze
from text import Fading_text
from menu import Menu, PauseMenu
from status import PlayerStatus
from HUD import HUD_class
from equipped_items import ItemFunctionality
from building import Building
from cooking import Cooking
from maze_changes import MazeChanges
from attack import Attack
from dropping import Drop

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Glorious Adventure - BETA")
        self.clock = pygame.time.Clock()  # FPS
        self.font = pygame.font.SysFont("Verdana", 20)  # Font

        self.player = Player(max_health=20, min_health=0,
                             max_stamina=20, min_stamina=0,
                             base_speed=6, max_speed=15, min_speed=1,
                             base_hunger=8, max_hunger=20, min_hunger=0,
                             base_thirst=12, max_thirst=20, min_thirst=0)

        self.player_rect = None  # Player rect to be set in the game

        self.screen = UniversalVariables.screen
        self.game_menu_state = "main"
        self.pause_menu_state = "main"

        self.daylight_strength = 0
        self.dim_surface = pygame.Surface((UniversalVariables.screen_x, UniversalVariables.screen_y), pygame.SRCALPHA,
                                          32)

        self.print_hp = 0
        self.restrict_looping = False

        self.terrain_data = None
        self.click_position = ()
        self.click_window_x = None
        self.click_window_y = None

        self.right_click_position = ()
        self.right_click_window_x = None
        self.right_click_window_y = None

        self.player_attack_rect = None

        if not self.terrain_data:
            self.terrain_data = MapData.map_list_to_map(self)

        for i in range(len(self.terrain_data)):
            for j in range(len(self.terrain_data[i])):
                if self.terrain_data[i][j] == 933:
                    self.terrain_data[i - 1][j] = 98

        # keys
        self.g_pressed = bool  # fps lock

    def event_game_state(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def events(self):
        for event in pygame.event.get():
            self.event_game_state(event)
            Event_handler.handle_mouse_events(self, event)
            Event_handler.handle_keyboard_events(self, event)

    def load_variables(self):
        UniversalVariables()

    def render_boxes():
        if (UniversalVariables.render_boxes_counter % 2) != 0:
            ObjectManagement.render_interaction_box()
            ObjectManagement.render_collision_box()
            Drop.display_all_floating_pouch_hitboxes()

    def call_technical(self):
        PlayerUpdate.update_player(self)  # Update player position and attributes
        Camera.box_target_camera(self)  # Camera follow

        ObjectCreation.creating_lists(self)  # CREATE SOME FUCKING BITCHES FUCKING COLLISION BOX LIST AND OBJCET LIST

        Collisions.collison_terrain_types(self)  # CHECK TERRAIN AND WATER Cadwasdwa
        Collisions.change_map_data(self)  # CHECK TERRAIN AND WATER Cadwasdwa
        MazeChanges.change_maze(self)

        vision.find_boxes_in_window()

        Enemy.update(self)
        Player_audio.player_audio_update(self)
        change_blades(self)
        PlayerStatus.update(self)
        ItemFunctionality.update(self)

    def call_visuals(self):
        RenderPictures.map_render(self)
        RenderPictures.object_render(self)

        Drop.update(self)
        Game.render_boxes()  # et visual boxid oleksid objektide peal, peab see oleme renderitud p2rast object_renderit.

        Enemy.spawn(self)

        EssentialsUpdate.calculate_daylight_strength(self)
        if Inventory.crafting_menu_open and not UniversalVariables.cooking_menu:
            Inventory.render_craftable_items(self)
            if not Inventory.craftable_items_display_rects and Inventory.crafting_menu_open:
                Fading_text.re_display_fading_text("Nothing to craft.")
                Inventory.crafting_menu_open = False

        vision.draw_light_source_and_rays(self, UniversalVariables.screen, self.player_rect.center)
        Attack.update(self)

        PlayerUpdate.render_HUD(self)  # Render HUD
        Drop.open_pouch(Drop.pouch_position)

        EssentialsUpdate.render_general(self)  # Render other elements
        HUD_class.update()

        Inventory.render_equipped_slot(self, UniversalVariables.current_equipped_item)  # Equipped item slot

        Building.update(self)

    def check_keys(self):
        Event_handler.check_pressed_keys(self)  # Check pressed keys

    def reset_lists(self):
        UniversalVariables.text_sequence = []
        UniversalVariables.blits_sequence_collision = []
        UniversalVariables.blits_sequence_objects = []

    def refresh_loop(self):
        Collisions.keylock = 0
        Game.add_counts()  # lisa countid juure uue loopi alguse puhul

        current_fps = self.clock.get_fps()
        if current_fps > 0:  # To avoid adding 0 FPS values
            UniversalVariables.fps_list.append(current_fps)
            if len(UniversalVariables.fps_list) > UniversalVariables.fps_list_max_size:
                UniversalVariables.fps_list.pop(0)  # Remove the oldest FPS value if we exceed max size
        
        if UniversalVariables.fps_lock == True: 
            FPS = 60
        else: FPS = UniversalVariables.FPS 
        self.clock.tick(FPS)

    @staticmethod
    def add_counts():
        if UniversalVariables.interaction_delay < UniversalVariables.interaction_delay_max:  UniversalVariables.interaction_delay += 1
        UniversalVariables.interaction_delay += 1

    def custom_addition(self):
        if UniversalVariables.debug_mode:
            if not self.restrict_looping:
                ObjectManagement.add_object_from_inv("Maze_Key", 30)
                # ObajectManagement.add_object_from_inv("Bandage", 100)
                self.restrict_looping = True

    def game_logic(self):
        self.reset_lists()
        self.call_technical()
        self.call_visuals()
        self.refresh_loop()

        Inventory.call(self)

        Final_Maze.update(self)
        Fading_text.update(self)
        Cooking.update(self)
        Player.update(self)

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



    def run(self):
        self.load_variables()
        while True:
            self.events()
            
            # Vaatab kas mäng on tööle pandud või mitte
            if Menu.game_state:
                Menu.main_menu(self)
                continue
            
            # Vaatab kas mäng on pausi peale pandud või mitte
            if PauseMenu.game_paused:
                PauseMenu.settings_menu(self)
                continue

            self.game_logic()

if __name__ == "__main__":
    game = Game()
    game.run()
