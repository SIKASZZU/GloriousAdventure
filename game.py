# Pythoni inbuilt/downloaded files
import pygame
import sys
import random

# Oma enda failid
from sprite import load_sprite_sheets, AnimationManager
from game_settings import player_stats
from stamina import StaminaComponent
from map_generator import map_data_generator
from render import Render_Checker  # map_render, object_list_creation
from collisions import Collisions  # check_collisions, collison_terrain, collision_hitbox
from inventory import Inventory  # render_inventory, call_inventory
from camera import box_target_camera
from objects import Object_Management

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
    terrain_data = map_data_generator(10)  # argument seed, default seed=None
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

        # Player stuff
        self.player = player_stats
        print(self.player, 'player_stats')

        self.player_height = self.block_size * 0.75
        self.player_width = self.block_size * 0.6

        self.inventory = {}  # Terve inv (prindi seda ja saad teada mis invis on)
        self.inv_count: int = 0  # Otsustab, kas renderida inv v6i mitte

        self.render_inv: bool = False  # Inventory renderminmine
        self.tab_pressed: bool = False  # Keep track of whether Tab was pressed

        self.player_x: int = random.randint(0, 5000)
        self.player_y: int = random.randint(0, 5000)

        self.player_rect = pygame.Rect(self.player_x, self.player_y, self.block_size * 0.6, self.block_size * 0.75)

        # Vajalik teadmiseks kas player renderida enne v6i p2rast objekte
        self.render_after = bool
        self.hit_box_halfpoint: int = 0

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

    # Uuendab player datat ja laseb tal liikuda
    def update_player(self) -> None:
        keys = pygame.key.get_pressed()  # Jälgib keyboard inputte

        # Teeb uue player x/y, algne x ja y tuleb playeri maailma panekuga (randint)
        new_player_x: int = self.player_x
        new_player_y: int = self.player_y

        if keys[pygame.K_LSHIFT]:
            self.frame_delay = 10  # Adjust running speed
        else:
            self.frame_delay = 7  # Default walking speed

        if keys[pygame.K_a]:
            self.animation_index = 0  # Left animation
        elif keys[pygame.K_d]:
            self.animation_index = 1  # Right animation
        elif keys[pygame.K_w]:
            self.animation_index = 2  # Up animation
        elif keys[pygame.K_s]:
            self.animation_index = 3  # Down animation

        # Diagonaali speedi fiximine
        if keys[pygame.K_a] and keys[pygame.K_w]:
            new_player_x = self.player_x - self.player.speed.current_speed / 1.5
            new_player_y = self.player_y - self.player.speed.current_speed / 1.5
        elif keys[pygame.K_a] and keys[pygame.K_s]:
            new_player_x = self.player_x - self.player.speed.current_speed / 1.5
            new_player_y = self.player_y + self.player.speed.current_speed / 1.5
        elif keys[pygame.K_d] and keys[pygame.K_w]:
            new_player_x = self.player_x + self.player.speed.current_speed / 1.5
            new_player_y = self.player_y - self.player.speed.current_speed / 1.5
        elif keys[pygame.K_d] and keys[pygame.K_s]:
            new_player_x = self.player_x + self.player.speed.current_speed / 1.5
            new_player_y = self.player_y + self.player.speed.current_speed / 1.5

        # Tavaline player speed (Verikaalselt, horisontaalselt)
        elif keys[pygame.K_a]:
            new_player_x = self.player_x - self.player.speed.current_speed
        elif keys[pygame.K_d]:
            new_player_x = self.player_x + self.player.speed.current_speed
        elif keys[pygame.K_w]:
            new_player_y = self.player_y - self.player.speed.current_speed
        elif keys[pygame.K_s]:
            new_player_y = self.player_y + self.player.speed.current_speed

        # Kui seda pole siis player ei liigu mapi peal
        # Uuendab playeri asukohta vastavalt keyboard inputile
        self.player_x: int = new_player_x
        self.player_y: int = new_player_y
        self.player_rect = pygame.Rect(self.player_x, self.player_y, self.block_size * 0.6, self.block_size * 0.75)

        # Kui player seisab (Animationi jaoks - IDLE)
        is_idle = not (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_e])

        if is_idle:
            self.frame = self.idle_animation_manager.update_animation(keys, is_idle)
        else:
            self.frame = self.animation_manager.update_animation(keys, is_idle)
        if self.frame is not None: self.sprite_rect = self.screen.blit(self.frame, (self.player_x, self.player_y))

    # Renderib ainuyksi playeri
    def render_player(self) -> None:
        # Muudab playeri asukohta vastavalt kaamera asukohale / paiknemisele
        player_position_adjusted: tuple[int, int] = (self.player_x + self.offset_x, self.player_y + self.offset_y)
        self.screen.blit(self.frame, player_position_adjusted)  # Renderib playeri animatsioni

        # Draw a red rectangle around the player
        player_rect = pygame.Rect(player_position_adjusted[0], player_position_adjusted[1], 60, 75)
        pygame.draw.rect(self.screen, (255, 0, 0), player_rect, 2)

    def render(self) -> None:
        if self.render_inv: Inventory.render_inventory(self)  # renderib inventory

        # Renderib stamina-bari
        if self.stamina_bar_decay < 50:
            pygame.draw.rect(self.screen, '#F7F7F6', self.stamina_rect_bg, 0, 7)
            pygame.draw.rect(self.screen, '#4169E1', self.stamina_rect, 0, 7)
            pygame.draw.rect(self.screen, 'black', self.stamina_rect_border, 2, 7)

        # Uuendab displaid ja fps cap 60
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 0, 0))
        self.screen.blit(fps_text, (100, 150))  # Adjust the position as needed

        pygame.display.update()

        # Limit the frame rate to 60 FPS
        self.clock.tick(60)

    def run(self) -> None:
        while True:
            self.handle_events()  # Paneb mängu õigesti kinni
            box_target_camera(self)  # Kaamera
            Inventory.call_inventory(self)  # update playeri osa()
            self.update_player()  # Uuendab mängija asukohta, ja muid asju

            StaminaComponent.stamina_bar_update(self)  # Stamina bar

            # collision things
            Collisions.collison_terrain(self)
            Collisions.check_collisions(self)  # Vaatab mängija kokkup6rkeid objecktidega

            Render_Checker.object_list_creation(self)  # Creatib self.hit_boxes
            Render_Checker.map_render(self)  # Renderib terraini

            if self.render_after == True:  # Renderib objectid peale playerit. Illusioon et player on objecti taga.
                Object_Management.place_and_render_object(self)  # Renderib objektid
                self.render_player()  # Renderib playeri (+ tema recti)
            else:  # self.render_after == False
                self.render_player()
                Object_Management.place_and_render_object(self)  # Renderib objektid

            self.render()  # inventory, stamina bari, fps counteri


if __name__ == "__main__":
    game = Game()
    game.run()
