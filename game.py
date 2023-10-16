# Pythoni inbuilt/downloaded files
import pygame
import sys
import random

# Oma enda failid
from sprite import load_sprite_sheets, AnimationManager
from game_settings import player_stats
from stamina import StaminaComponent
from map import Map_information  # map_data_generator
from render import Render_Checker  # map_render, object_list_creation
from collisions import Collisions  # check_collisions, collison_terrain, collision_hitbox
from camera import Camera  # box_target_camera
from objects import Object_Management
from update import Game_update  # update_player, render_player
from inventory import Inventory

clock = pygame.time.Clock()


class Game:

    @staticmethod
    def handle_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    pygame.init()
    pygame.display.set_caption("Glorious Adventure - BETA")

    # universal sitt - peab mingisse faili minema
    terrain_data = Map_information.glade_creation()
    block_size: int = 100
    hit_boxes: list = []
    screen_x: int = 1000
    screen_y: int = 750
    screen = pygame.display.set_mode((screen_x, screen_y))
    player = player_stats  # load in game_settings
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Verdana", 20)
    player_height = block_size * 0.65
    player_width = block_size * 0.45
    player_x: int = random.randint(400, 400)
    player_y: int = random.randint(400, 400)
    # universal sitt l6ppeb siin, muud pole testinud


    def run(self) -> None:
        while True:
            #print(self.terrain_data)
            self.handle_events()  # Paneb mängu õigesti kinni
            Game_update.update_player(self)  # Uuendab mängija asukohta, ja muid asju
            Camera.box_target_camera(self)  # Kaamera

            StaminaComponent.stamina_bar_update(self)  # Stamina bar

            # collision things
            Collisions.collison_terrain(self)
            Collisions.check_collisions(self)  # Vaatab mängija kokkup6rkeid objecktidega

            Render_Checker.object_list_creation(self)  # Creatib self.hit_boxes
            Render_Checker.map_render(self)  # Renderib terraini
            
            if Collisions.render_after == True:  # Renderib objectid peale playerit. Illusioon et player on objecti taga.
                Object_Management.place_and_render_object(self)  # Renderib objektid
                Game_update.render_player(self)  # Renderib playeri (+ tema recti)
            else:  # self.render_after == False
                Game_update.render_player(self)
                Object_Management.place_and_render_object(self)  # Renderib objektid

            Inventory.handle_mouse_click(self)  # Inventorisse clickimise systeem
            Game_update.render_hud(self)  # Render HUD_class (health- ,food- ,stamina bar)
            Game_update.render(self)  # inventory, fps counteri

if __name__ == "__main__":
    game = Game()
    game.run()
