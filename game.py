# Pythoni inbuilt/downloaded files
import pygame
import sys
import random

# Oma enda failid
from map import MapData  # map_data_generator
from camera import Camera  # box_target_camera
from update import PlayerUpdate  # update_player, render_player
from inventory import Inventory
from collisions import Collisions  # check_collisions, collison_terrain, collision_hitbox
from render import RenderPictures  # map_render
from render import CreateHitboxes  # object_list_creation
from stamina import StaminaComponent
from objects import ObjectManagement
from game_settings import player_stats  # erinevad settingud, speed jms

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

    # universal sitt - peab mingisse faili minema (game_settings.py)
    terrain_data = MapData.glade_creation()
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
            PlayerUpdate.update_player(self)  # Uuendab mängija asukohta, ja muid asju
            Camera.box_target_camera(self)  # Kaamera

            StaminaComponent.stamina_bar_update(self)  # Stamina bar

            # collision things
            Collisions.collison_terrain(self)
            Collisions.check_collisions(self)  # Vaatab mängija kokkup6rkeid objecktidega

            CreateHitboxes.object_list_creation(self)  # Creatib self.hit_boxes
            RenderPictures.map_render(self)  # Renderib terraini
            
            if Collisions.render_after == True:  # Renderib objectid peale playerit. Illusioon et player on objecti taga.
                ObjectManagement.place_and_render_object(self)  # Renderib objektid
                PlayerUpdate.render_player(self)  # Renderib playeri (+ tema recti)
            else:  # self.render_after == False
                PlayerUpdate.render_player(self)
                ObjectManagement.place_and_render_object(self)  # Renderib objektid

            Inventory.handle_mouse_click(self)  # Inventorisse clickimise systeem
            PlayerUpdate.render_HUD(self)  # Render HUD_class (health- ,food- ,stamina bar)
            PlayerUpdate.render_general(self)  # inventory, fps counteri

if __name__ == "__main__":
    game = Game()
    game.run()
