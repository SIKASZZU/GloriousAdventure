# Pythoni inbuilt/downloaded files
import pygame
import sys

from components import Player, StaminaComponent

# Oma enda failid
from entity import Enemy
from variables import UniversalVariables
from camera import Camera  # box_target_camera
from render import RenderPictures  # map_render
from map import MapData  # glade_creation, map_list_to_map
from objects import ObjectManagement  # place_and_render_object
from render import CreateCollisionBoxes  # object_list_creation
import vision  # find_boxes_in_window, draw_light_source_and_rays
from menu import Menu, PauseMenu  # main_menu, PauseMenu: settings_menu
from update import EssentsialsUpdate  # check_pressed_keys, render_general
from update import PlayerUpdate  # update_player, render_player, render_HUD
from inventory import Inventory  # handle_mouse_click, render_craftable_items
from collisions import Collisions  # check_collisions, collison_terrain, collision_hitbox


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
        
    def game_state_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not Menu.game_state:               
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if PauseMenu.game_paused == False:
                        PauseMenu.game_paused = True
                    else:
                        PauseMenu.screenshot = None
                        PauseMenu.game_paused = False
                        self.pause_menu_state = "main"
                        PauseMenu.screenshot = None
        
    def check_state_menu(self):
        if Menu.game_state:
            Menu.main_menu(self)
            pygame.display.update()
        else:
            if PauseMenu.game_paused:
                PauseMenu.settings_menu(self)

    def check_event_buttons(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll +
                    UniversalVariables.block_size += 10  # Increase block_size

                    UniversalVariables.player_height: int = UniversalVariables.block_size * 0.65
                    UniversalVariables.player_width: int = UniversalVariables.block_size * 0.65

                    UniversalVariables.player_hitbox_offset_x = 0.29 * UniversalVariables.player_height
                    UniversalVariables.player_hitbox_offset_y = 0.22 * UniversalVariables.player_width

                elif event.button == 5:  # Scroll -
                    UniversalVariables.block_size -= 10  # Decrease block_size
                    if UniversalVariables.block_size < 1:  # Prevent block_size from being less than 1
                        UniversalVariables.block_size = 1

                    UniversalVariables.player_height: int = UniversalVariables.block_size * 0.65
                    UniversalVariables.player_width: int = UniversalVariables.block_size * 0.65

                    UniversalVariables.player_hitbox_offset_x = 0.29 * UniversalVariables.player_height
                    UniversalVariables.player_hitbox_offset_y = 0.22 * UniversalVariables.player_width

    def events(self):
        Game.game_state_events(self)
        Game.check_state_menu(self)
        Game.check_event_buttons(self)

    def call_visuals(self):
        RenderPictures.map_render(self)  # Renderib terraini
        
        if Collisions.render_after == True:
            ObjectManagement.place_and_render_object(self)  # Renderib objektid
            PlayerUpdate.render_player(self)  # Renderib playeri (+ tema recti)
        else:
            PlayerUpdate.render_player(self)
            ObjectManagement.place_and_render_object(self)  # Renderib objektid
        
        vision.draw_light_source_and_rays(self, UniversalVariables.screen, self.player_rect.center, UniversalVariables.light_range)
        PlayerUpdate.render_HUD(self)  # Render HUD_class (health- ,food- ,stamina bar)
        EssentsialsUpdate.render_general(self)  # render inv, display text

            
        # DAYLIGHT CHANGE
        # EssentsialsUpdate.calculate_daylight_strength(self)  # p2evavalguse tugevus


    def call_technical(self):
        PlayerUpdate.update_player(self)  # Uuendab mängija asukohta, ja muid asju
        Camera.box_target_camera(self)  # Kaamera
        StaminaComponent.stamina_bar_update(self)  # Stamina bar

        # collision things
        Collisions.collison_terrain(self)
        Collisions.check_collisions(self)  # Vaatab mängija kokkup6rkeid objecktidega
    
        CreateCollisionBoxes.object_list_creation(self)  # Creatib UniversalVariables.collision_boxes

        self.player.health.check_health()

        Enemy.update(self)

        vision.find_boxes_in_window()

    def check_keys(self):

        # *** inventory check *** #
        Inventory.handle_mouse_click(self)  # Inventorisse clickimise systeem
        # Inventory.call_inventory(self)  # calculates inv coordinates and stuff, doesn't visualize

        EssentsialsUpdate.check_pressed_keys(self)  # vaatab, luurab vajutatud keysid

    
        
    def reset_lists():
        ''' Before new loop, reset image sequences. '''

        UniversalVariables.text_sequence = []
        UniversalVariables.blits_sequence = []

    def update(self):
        
        Collisions.keylock = 0
        self.screen.blits(UniversalVariables.text_sequence)

        pygame.display.update()
        self.clock.tick(600)

    def run(self):
        while True:
            Game.reset_lists()
            
            UniversalVariables()
            
            # Game.events(self)
            Game.call_technical(self)
            Game.call_visuals(self)
            Game.check_keys(self)
            Game.update(self)

if __name__ == "__main__":
    game = Game()
    game.run()

