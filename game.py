# Pythoni inbuilt/downloaded files
import pygame
import sys


# Oma enda failid
from variables import UniversalVariables
from camera import Camera  # box_target_camera
from render import RenderPictures  # map_render
from map import MapData  # glade_creation, map_list_to_map
from components import StaminaComponent  # stamina_bar_update
from objects import ObjectManagement  # place_and_render_object
from render import CreateCollisionBoxes  # object_list_creation
import vision  # find_boxes_in_window, draw_light_source_and_rays
from menu import Menu, PauseMenu  # main_menu, PauseMenu: settings_menu
from update import EssentsialsUpdate  # check_pressed_keys, render_general
from update import PlayerUpdate  # update_player, render_player, render_HUD
from inventory import Inventory  # handle_mouse_click, render_craftable_items
from collisions import Collisions  # check_collisions, collison_terrain, collision_hitbox


### TODO: hitboxid on paremal ja all collectimisel perses

### TODO: Kui kell on mingi t2pne aeg, l2hevad mzei uksed kinni, mis on gladei juures

### TODO: monsterite tegemine, enemy

### TODO: lisada vilja asemel maze'is mingi võtmed

### TODO: kui kolm võtit on käes, siis saab alles avada ukse
    # avades ukse võtab playerilt kõik kolm võtit ära

### TODO: Mingid lambised juhtivad tekstid ekraanile
    # Esimese võtme leidmisel näiteks "Hmm, what can this be used for? What sort of a door needs this?"
    # Kui leiab ukse ja üritab avada "There are three keyholes"
    # vb midagi kui esimest korda mazei enterib "What a cold and eerie place. I better escape this place"

### TODO: Jooksmise asemel luuramine, aeglasem speed. 
    # m6te selles, et kui enemy on kuskil, ss ta ei kuuleks
    # mingi indikaator v6i heli tuleks kui enemy l2hedal

### TODO: Outside map on k6ik shadow


class Game:
    pygame.init()
    pygame.display.set_caption("Glorious Adventure - BETA")

    # ******************** PLAYER *******ds************* #
    player_rect = None  # seda ei pea olema, aga mdea, suht perses. Code settib r2igelt self argumente, mida ei eksisteeri

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

    def run(self) -> None:
        while True:
            UniversalVariables.text_sequence = []
            UniversalVariables.blits_sequence = []

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

                    # Võtab clicki positsiooni
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.click_position = event.pos

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


            # Vaatab kas mäng on tööle pandud või mitte
            if Menu.game_state:
                Menu.main_menu(self)
                pygame.display.update()

            # Kui mäng pandakse tööle
            if not Menu.game_state:

                # Vaatab kas mäng on pausi peale pandud või mitte
                if not PauseMenu.game_paused:
                    UniversalVariables()
                    PlayerUpdate.update_player(self)  # Uuendab mängija asukohta, ja muid asju
                    Camera.box_target_camera(self)  # Kaamera
                    StaminaComponent.stamina_bar_update(self)  # Stamina bar

                    # collision things
                    Collisions.collison_terrain(self)
                    Collisions.check_collisions(self)  # Vaatab mängija kokkup6rkeid objecktidega

                    CreateCollisionBoxes.object_list_creation(self)  # Creatib UniversalVariables.collision_boxes
                    RenderPictures.map_render(self)  # Renderib terraini

                    # Renderib objectid peale playerit. Illusioon et player on objecti taga.
                    if Collisions.render_after == True:
                        ObjectManagement.place_and_render_object(self)  # Renderib objektid
                        PlayerUpdate.render_player(self)  # Renderib playeri (+ tema recti)
                    else:
                        PlayerUpdate.render_player(self)
                        ObjectManagement.place_and_render_object(self)  # Renderib objektid


                    Inventory.handle_mouse_click(self)  # Inventorisse clickimise systeem
                    # Inventory.call_inventory(self)  # arvutab, kas player on tabi vajutanud v mitte

                    vision.find_boxes_in_window()
                    vision.draw_light_source_and_rays(self, UniversalVariables.screen, self.player_rect.center, UniversalVariables.light_range)

                    PlayerUpdate.render_HUD(self)  # Render HUD_class (health- ,food- ,stamina bar)

                    EssentsialsUpdate.check_pressed_keys(self)  # vaatab, luurab vajutatud keysid
                    EssentsialsUpdate.render_general(self)  # inventory, fps counteri
                    
                    # DAYLIGHT CHANGE
                    # EssentsialsUpdate.calculate_daylight_strength(self)  # p2evavalguse tugevus

                    Collisions.keylock = 0
                    self.screen.blits(UniversalVariables.text_sequence)
                else:
                    PauseMenu.settings_menu(self)

                pygame.display.update()
                self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
