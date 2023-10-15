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

    # ******** Map data stuff ******** #
    terrain_data = Map_information.glade_creation()
    
    # universal sitt - peab mingisse faili minema
    block_size: int = 100
    hit_boxes: list = []
    screen_x: int = 1000
    screen_y: int = 750
    screen = pygame.display.set_mode((screen_x, screen_y))
    # universal sitt l6ppeb siin, muud pole testinud
    
    stamina_bar_decay: int = 0
    
    # ******** FPS counter ******** #
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Verdana", 20)

    # ******** Player stuff ******** #
    player = player_stats
    player_height = block_size * 0.65
    player_width = block_size * 0.45

    # Muudab player hitboxi asukoha õigeks, punane kast, 09.10.2023 see oli update.py line 79
    player_hitbox_offset_x = 29
    player_hitbox_offset_y = 22

    player_x: int = random.randint(400, 400)
    player_y: int = random.randint(400, 400)

    # ******** Animation stuff ******** #
    sprite_sheets, animations = load_sprite_sheets([
        'images/Player/Left.png',
        'images/Player/Right.png',
        'images/Player/Up.png',
        'images/Player/Down.png'
    ])

    sprite_sheets_idle, animations_idle = load_sprite_sheets([
        'images/Player/Idle_Left.png',
        'images/Player/Idle_Right.png',
        'images/Player/Idle_Up.png',
        'images/Player/Idle_Down.png'
    ])

    animation_speeds = [10, 10, 10, 10]

    # Teeb idle ja mitte idle animatsioone
    animation_manager = AnimationManager(sprite_sheets, animations, animation_speeds)
    idle_animation_manager = AnimationManager(sprite_sheets_idle, animations_idle,
                                                    animation_speeds)


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
