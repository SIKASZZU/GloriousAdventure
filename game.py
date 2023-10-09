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
from camera import box_target_camera
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
    terrain_data = Map_information.map_data_generator(10)  # argument seed, default seed=None
    block_size: int = 100
    generated_ground_images: dict = {}
    generated_water_images: dict = {}
    hit_boxes: list = []

    dimensions: list[int, ...] = []

    screen_x: int = 1000
    screen_y: int = 750
    screen = pygame.display.set_mode((screen_x, screen_y))

    terrain_data_minerals: int = 0
    display_hit_box_decay: int = 0
    stamina_bar_decay: int = 0
    render_range: int = 0
    index: int = 0

    def __init__(self):
        # ******** FPS counter ******** #
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 20)

        # ******** Player stuff ******** #
        self.player = player_stats

        self.player_height = self.block_size * 0.75
        self.player_width = self.block_size * 0.6

        self.inventory = {}  # Terve inv (prindi seda ja saad teada mis invis on)
        self.inv_count: int = 0  # Otsustab, kas renderida inv v6i mitte

        self.render_inv: bool = False  # Inventory renderminmine
        self.tab_pressed: bool = False  # Keep track of whether Tab was pressed

        self.player_x: int = random.randint(0, 5000)
        self.player_y: int = random.randint(0, 5000)

        self.player_rect = pygame.Rect(self.player_x, self.player_y, self.player_height, self.player_width)

        # Vajalik teadmiseks kas player renderida enne v6i p2rast objekte
        self.render_after = bool

        # Vajalik, et pickup delay oleks.
        self.pickup_timer = 0
        self.pickup_delay = 2  # 2 seconds delay for picking up objects
        self.can_pickup = True

        # ******** Camera stuff ******** #
        self.offset_x: int = 0
        self.offset_y: int = 0
        self.camera_borders = {'left': 250, 'right': 250, 'top': 200, 'bottom': 200}
        l: int = self.camera_borders['left']
        t: int = self.camera_borders['top']
        w: int = self.screen.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h: int = self.screen.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)

        # ******** Inventory ******** #
        self.inventory_display_rects = []

        # ******** Stamina bar ******** #
        self.stamina_bar_decay: int = 0

        self.stamina_bar_size: int = 200
        self.stamina_bar_size_bg: int = 200
        self.stamina_bar_size_border: int = 200
        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y))
        self.half_w = self.screen.get_size()[0] // 2
        self.ratio = self.stamina_bar_size // 20  # 200 // 20 = 10
        self.stamina_rect_bg = pygame.Rect(self.half_w - (self.stamina_bar_size_bg / 2) - 6, self.screen_y - 25,
                                           self.stamina_bar_size_bg + 12,
                                           15)  # Kui staminat kulub, ss on background taga
        self.stamina_rect_border = pygame.Rect(self.half_w - (self.stamina_bar_size_border / 2) - 6, self.screen_y - 25,
                                               self.stamina_bar_size_border + 12,
                                               15)  # K6igi stamina baride ymber border
        self.stamina_rect = pygame.Rect(self.half_w - (self.stamina_bar_size / 2) - 6, self.screen_y - 25,
                                        self.stamina_bar_size + 12, 15)

        # ******** Animation stuff ******** #
        self.sprite_sheets, self.animations = load_sprite_sheets([
            'images/Player/Left.png',
            'images/Player/Right.png',
            'images/Player/Up.png',
            'images/Player/Down.png'
        ])

        self.sprite_sheets_idle, self.animations_idle = load_sprite_sheets([
            'images/Player/Idle_Left.png',
            'images/Player/Idle_Right.png',
            'images/Player/Idle_Up.png',
            'images/Player/Idle_Down.png'
        ])

        self.animation_speeds = [10, 10, 10, 10]

        # Teeb idle ja mitte idle animatsioone
        self.animation_manager = AnimationManager(self.sprite_sheets, self.animations, self.animation_speeds)
        self.idle_animation_manager = AnimationManager(self.sprite_sheets_idle, self.animations_idle,
                                                       self.animation_speeds)


    def run(self) -> None:
        while True:
            #print(self.terrain_data)
            self.handle_events()  # Paneb mängu õigesti kinni
            box_target_camera(self)  # Kaamera
            Game_update.update_player(self)  # Uuendab mängija asukohta, ja muid asju

            StaminaComponent.stamina_bar_update(self)  # Stamina bar

            # collision things
            Collisions.collison_terrain(self)
            Collisions.check_collisions(self)  # Vaatab mängija kokkup6rkeid objecktidega

            Render_Checker.object_list_creation(self)  # Creatib self.hit_boxes
            Render_Checker.map_render(self)  # Renderib terraini

            if self.render_after == True:  # Renderib objectid peale playerit. Illusioon et player on objecti taga.
                Object_Management.place_and_render_object(self)  # Renderib objektid
                Game_update.render_player(self)  # Renderib playeri (+ tema recti)
            else:  # self.render_after == False
                Game_update.render_player(self)
                Object_Management.place_and_render_object(self)  # Renderib objektid

            Inventory.handle_mouse_click(self)  # Inventorisse clickimise systeem
            Game_update.render(self)  # inventory, stamina bari, fps counteri


if __name__ == "__main__":
    game = Game()
    game.run()
