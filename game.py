# Pythoni inbuilt/downloaded files
import pygame
import sys

# Oma enda failid
from camera import Camera  # box_target_camera
from inventory import Inventory
from update import PlayerUpdate  # update_player, render_player
from render import RenderPictures  # map_render
from collisions import Collisions  # check_collisions, collison_terrain, collision_hitbox
from objects import ObjectManagement
from render import CreateCollisionBoxes  # object_list_creation
from components import StaminaComponent


class Game:

    @staticmethod
    def handle_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    pygame.init()
    pygame.display.set_caption("Glorious Adventure - BETA")
    
    # ******************** PLAYER ******************** # 
    player_rect = None  # seda ei pea olema, aga mdea, suht perses. Code settib r2igelt self argumente, mida ei eksisteeri

    # ******************** FPS, FONT ******************** # 
    clock = pygame.time.Clock()  # fps
    font = pygame.font.SysFont("Verdana", 20)  # font

    def run(self) -> None:
        while True:
            #print(UniversalVariables.terrain_data)
            self.handle_events()  # Paneb mängu õigesti kinni
            PlayerUpdate.update_player(self)  # Uuendab mängija asukohta, ja muid asju
            Camera.box_target_camera(self)  # Kaamera

            StaminaComponent.stamina_bar_update(self)  # Stamina bar

            # collision things
            Collisions.collison_terrain(self)
            Collisions.check_collisions(self)  # Vaatab mängija kokkup6rkeid objecktidega

            CreateCollisionBoxes.object_list_creation(self)  # Creatib UniversalVariables.collision_boxes
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
