# Pythoni inbuilt/downloaded files
import pygame
import sys

from components import Player, StaminaComponent

# Oma enda failid
from entity import Enemy
from variables import UniversalVariables
from camera import Camera  # box_target_camera
from render import RenderPictures  # map_render
from mbd import event_mousebuttondown
from map import MapData  # glade_creation, map_list_to_map
from objects import ObjectManagement  # place_and_render_object
from render import CreateCollisionBoxes  # object_list_creation
import vision  # find_boxes_in_window, draw_light_source_and_rays
from menu import Menu, PauseMenu  # main_menu, PauseMenu: settings_menu
from update import EssentsialsUpdate  # check_pressed_keys, render_general
from update import PlayerUpdate  # update_player, render_player, render_HUD
from inventory import Inventory  # handle_mouse_click, render_craftable_items
from collisions import Collisions  # check_collisions, collison_terrain, collision_hitbox
from audio import Player_audio  # player_audio_update

class Game:
    pygame.init()
    pygame.display.set_caption("Glorious Adventure - BETA")

    # ******************** PLAYER *******ds************* #
    player_rect = None  # seda ei pea olema, aga mdea, suht perses. Code settib r2igelt self argumente, mida ei eksisteeri
    player = Player(max_health=20, min_health=0, max_stamina=20, min_stamina=0, base_speed=40, max_speed=10, min_speed=1)

    # ******************** FPS, FONT ******************** #w
    clock = pygame.time.Clock()  # fps
    font = pygame.font.SysFont("Verdana", 20)  # font

    # ******************** MENU ******************** #
    screen = UniversalVariables.screen

    game_menu_state = "main"
    pause_menu_state = "main"

    # ******************** NIGHT/DAY LIGHTNING ******************** #
    daylight_strength = 0
    dim_surface = pygame.Surface((UniversalVariables.screen_x, UniversalVariables.screen_y), pygame.SRCALPHA, 32)
    dim_surface = dim_surface.convert_alpha()
    
    # ******************** RANDOM/DEBUG ******************** #
    print__hp = 0
    restrict_looping = False

    def __init__(self):
        glade_data = None
        self.terrain_data = None

        self.click_position: tuple[int, int] = ()
        self.click_window_x: int = None
        self.click_window_y: int = None

        if not glade_data:
            glade_data = MapData.glade_creation()  # glade data

        if not self.terrain_data:
            self.terrain_data = MapData.map_list_to_map(self)

        for i in range(len(self.terrain_data)):
            for j in range(len(self.terrain_data[i])):
                if self.terrain_data[i][j] == 933:
                    self.terrain_data[i - 1][j] = 98

    def event_game_state(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def events(self):
        for event in pygame.event.get():
            Game.event_game_state(self, event)
            event_mousebuttondown(self, event)
        

    def load_variables(self): UniversalVariables()

    def call_technical(self):
        PlayerUpdate.update_player(self)  # Uuendab mängija asukohta, ja muid asju
        Camera.box_target_camera(self)  # Kaamera

        # collision things
        Collisions.collison_terrain(self)
        Collisions.check_collisions(self)  # Vaatwab mängija kokkup6rkeid objecktidega
        
        CreateCollisionBoxes.object_list_creation(self)  # Creatib UniversalVariables.collision_boxes
        vision.find_boxes_in_window()

        self.player.health.check_health()
        Enemy.update(self)
        # Inventory.call_inventory(self)  # doesn't visualize, just calculates

        Player_audio.player_audio_update(self)

    def call_visuals(self):
        RenderPictures.map_render(self)  # Renderib terraini
        
        if Collisions.render_after == True:
            ObjectManagement.place_and_render_object(self)  # Renderib objektid
            PlayerUpdate.render_player(self)  # Renderib playeri (+ tema recti)
        else:
            PlayerUpdate.render_player(self)
            ObjectManagement.place_and_render_object(self)  # Renderib objektid
        
        Enemy.spawn(self)
        vision.draw_light_source_and_rays(self, UniversalVariables.screen, self.player_rect.center, UniversalVariables.light_range)
        PlayerUpdate.render_HUD(self)  # Render HUD_class (health- ,food- ,stamina bar)
        EssentsialsUpdate.render_general(self)  # render inv, display text
        # EssentsialsUpdate.calculate_daylight_strength(self)  # DAYLIGHT CHANGE

    def check_keys(self):
        """ Check for which keys are pressed. """

        EssentsialsUpdate.check_pressed_keys(self)  # vaatab, luurab vajutatud keysid

    def reset_lists(self):
        ''' Before new loop, reset image sequences. '''

        UniversalVariables.text_sequence = []
        UniversalVariables.blits_sequence = []

    def refresh_loop(self):
        """ Set and reset stuff for new loop. """
        
        Collisions.keylock = 0
        self.screen.blits(UniversalVariables.text_sequence)

        pygame.display.update()
        self.clock.tick(UniversalVariables.FPS)
    
    def printing(self):
        Inventory.print_inventory()
        Camera.print_clicks(self)
        self.player.health.print_health()

    def custom_addition():
        if Game.restrict_looping == False:
            ObjectManagement.add_object_from_inv("Maze_Key", 1000)
            Game.restrict_looping = True
            
    def run(self):
        xxx = 0
        while True:
            Game.events(self)
            Game.load_variables(self)
            Game.reset_lists(self)
            
            Game.call_technical(self)
            Game.call_visuals(self)
            Game.check_keys(self)
            Game.refresh_loop(self)

            Game.printing(self)
            Game.custom_addition()
            xxx += 1

            if UniversalVariables.portal_frame_rect:

                if UniversalVariables.portal_frame_rect.colliderect(self.player_rect):
                    UniversalVariables.cutscene = True
                    xxx = 0

                    UniversalVariables.portal_frame_rect = None
                    UniversalVariables.portal_list = []

                pygame.display.flip()

            if xxx == 100:
                UniversalVariables.cutscene = False

if __name__ == "__main__":
    game = Game()
    game.run()

