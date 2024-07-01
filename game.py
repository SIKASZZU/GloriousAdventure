# Pythoni inbuilt/downloaded files
import pygame
import sys
import os
import sys

from components import Player, HungerComponent

# Oma enda failid
import vision  # find_boxes_in_window, draw_light_source_and_rays
from entity import Enemy
from variables import UniversalVariables
from camera import Camera  # box_target_camera
from render import RenderPictures, ObjectCreation  # map_render, creating_lists
from event_handler import Event_handler
from map import MapData  # glade_creation, map_list_to_map
from objects import ObjectManagement  # place_and_render_object
import vision  # find_boxes_in_window, draw_light_source_and_rays
from update import EssentialsUpdate  # check_pressed_keys, render_general, calculate_daylight_strength
from update import PlayerUpdate  # update_player, render_player, render_HUD
from inventory import Inventory  # handle_mouse_click, render_craftable_items
from collisions import Collisions  # check_collisions, collision_terrain, collision_hitbox
from audio import Player_audio  # player_audio_update
from blade import change_blades
from final_maze import Final_Maze
from text import Fading_text
from menu import Menu, PauseMenu
from status import PlayerStatus
from HUD import HUD_class
from equipped_items import ItemFunctionality

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

        self.player = Player(max_health=20, min_health=0, max_stamina=20, min_stamina=0, base_speed=4, max_speed=8,
                             min_speed=1, base_hunger=20, max_hunger=20, min_hunger=0)
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

        glade_data = MapData.glade_creation()
        if not self.terrain_data:
            self.terrain_data = MapData.map_list_to_map(self)

        for i in range(len(self.terrain_data)):
            for j in range(len(self.terrain_data[i])):
                if self.terrain_data[i][j] == 933:
                    self.terrain_data[i - 1][j] = 98

        self.fading_text = Fading_text()

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

    def call_technical(self):
        Inventory.calculate_inventory(self, True)  # Et invi slottide kogus oleks õige

        PlayerUpdate.update_player(self)  # Update player position and attributes
        Camera.box_target_camera(self)  # Camera follow

        ObjectCreation.creating_lists(self)  # CREATE SOME FUCKING BITCHES FUCKING COLLISION BOX LIST AND OBJCET LIST

        Collisions.collison_terrain_types(self)  # CHECK TERRAIN AND WATER Cadwasdwa
        Collisions.change_map_data(self)  # CHECK TERRAIN AND WATER Cadwasdwa
        
        vision.find_boxes_in_window()

        self.player.health.check_health(self.player.hunger.current_hunger)
        Enemy.update(self)
        Player_audio.player_audio_update(self)
        change_blades(self)
        PlayerStatus.update(self)
        ItemFunctionality.update(self)

    def call_visuals(self):
        RenderPictures.map_render(self)

        if Collisions.render_after:
            RenderPictures.object_render()
            PlayerUpdate.render_player(self)
        else:
            PlayerUpdate.render_player(self)
            RenderPictures.object_render()

        ObjectManagement.render_boxes()  # et visual boxid oleksid objektide peal, peab see oleme renderitud p2rast object_renderit.

        Enemy.spawn(self)
        EssentialsUpdate.calculate_daylight_strength(self)
        if Inventory.crafting_menu_open:
            Inventory.render_craftable_items(self)
            if not Inventory.craftable_items_display_rects and Inventory.crafting_menu_open:
                text = "Nothing to craft."

                if text in Fading_text.shown_texts:
                    Fading_text.shown_texts.remove(text)

                UniversalVariables.ui_elements.append(text)
                Inventory.crafting_menu_open = False

        vision.draw_light_source_and_rays(self, UniversalVariables.screen, self.player_rect.center, UniversalVariables.light_range)
        PlayerUpdate.render_HUD(self)  # Render HUD
        EssentialsUpdate.render_general(self)  # Render other elements
        HUD_class.update()

        # Equipped item slot
        if UniversalVariables.current_equipped_item:
            item = UniversalVariables.current_equipped_item
            Inventory.render_inventory_slot(self, item)
        else:
            item = None  # TODO: kas argumendis ei saaks olla item juba None?, et siis seda ekstra line'i ei peaks siin olema
            Inventory.render_inventory_slot(self, item)

    def check_keys(self):
        EssentialsUpdate.check_pressed_keys(self)  # Check pressed keys

    def reset_lists(self):
        UniversalVariables.text_sequence = []
        UniversalVariables.blits_sequence = []

    def refresh_loop(self):
        Collisions.keylock = 0
        self.screen.blits(UniversalVariables.text_sequence)
        pygame.display.update()
        self.clock.tick(UniversalVariables.FPS)

    def printing(self):
        Camera.print_clicks(self)
        print(self.player)

    def custom_addition(self):
        if UniversalVariables.debug_mode == True:
            if not self.restrict_looping:
                ObjectManagement.add_object_from_inv("Maze_Key", 100)
                # ObjectManagement.add_object_from_inv("Bread", 100)
                # ObjectManagement.add_object_from_inv("Bad_Bread", 100)
                self.restrict_looping = True

    def game_logic(self):
        self.reset_lists()
        self.call_technical()
        self.call_visuals()

        HungerComponent.eat(self)
        Inventory.call_inventory(self)
        if Inventory.render_inv: Inventory.render_inventory(self)  # Render inventory

        Final_Maze.final_maze_update(self)
        Fading_text.render_general(self)
        Fading_text.handle_fading_texts(self)  # Render fading text after everything else

        self.refresh_loop()
        HungerComponent.decrease_hunger(self)

        # ******************** DEBUG MODE ******************** #
        if UniversalVariables.debug_mode:
            UniversalVariables.ui_elements.append("!        Debug mode - True        !")
            self.player.speed.base_speed = 20

            # neil functionitel on juba sees, et kontrolliks debug modei
            self.check_keys()  # Toggle hitbox / vision
            self.custom_addition()
            # UniversalVariables.player_x, UniversalVariables.player_y = 300, 3800   # FPS'side testimiseks
            # print(self.player)

        self.click_position = ()

    def run(self):
        self.load_variables()
        while True:
            self.events()
            # Vaatab kas mäng on tööle pandud või mitte
            if Menu.game_state:
                Menu.main_menu(self)

            # Kui mäng pandakse tööle
            if not Menu.game_state:

                # Vaatab kas mäng on pausi peale pandud või mitte
                if not PauseMenu.game_paused:
                    self.game_logic()
                else:
                    PauseMenu.settings_menu(self)

                pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()
