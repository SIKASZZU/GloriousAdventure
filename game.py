# Pythoni inbuilt/downloaded files
import time

import numpy as np
import pygame
import sys

from map import MapData

# Oma enda failid
from menu import Menu, PauseMenu
#from vision import LightSource
from camera import Camera  # box_target_camera
from inventory import Inventory
from update import PlayerUpdate  # update_player, render_player
from render import RenderPictures  # map_render
from collisions import Collisions  # check_collisions, collison_terrain, collision_hitbox
from objects import ObjectManagement
from render import CreateCollisionBoxes  # object_list_creation
from components import StaminaComponent
from variables import UniversalVariables


class Game:
    pygame.init()
    pygame.display.set_caption("Glorious Adventure - BETA")

    # ******************** PLAYER *******ds************* #
    player_rect = None  # seda ei pea olema, aga mdea, suht perses. Code settib r2igelt self argumente, mida ei eksisteeri

    # ******************** FPS, FONT ******************** #
    clock = pygame.time.Clock()  # fps
    font = pygame.font.SysFont("Verdana", 20)  # font

    # ******************** MENU ******************** #
    screen = UniversalVariables.screen

    game_menu_state = "main"
    pause_menu_state = "main"

    def __init__(self):
        glade_data = None
        self.terrain_data = None

        if not glade_data:
            glade_data = MapData.glade_creation()  # glade data

        if not self.terrain_data:
            self.terrain_data = MapData.map_creation()

    def run(self) -> None:
        while True:
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
                    else:  # self.render_after == False
                        PlayerUpdate.render_player(self)
                        ObjectManagement.place_and_render_object(self)  # Renderib objektid

                    Inventory.handle_mouse_click(self)  # Inventorisse clickimise systeem

                    if Inventory.render_inv:
                        Inventory.render_craftable_items(self)

                    #light_source.x, light_source.y = UniversalVariables.player_x, UniversalVariables.player_y
                    PlayerUpdate.render_HUD(self)  # Render HUD_class (health- ,food- ,stamina bar)
                    PlayerUpdate.render_general(self)  # inventory, fps counteri
                    #Vision.find_walls()  # eksperiment
                    Collisions.keylock = 0
                else:
                    PauseMenu.settings_menu(self)
                    pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
