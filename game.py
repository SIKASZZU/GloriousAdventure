# Pythoni inbuilt/downloaded files
import pygame
import sys
import random
import time

# Oma enda failid
from sprite import load_sprite_sheets, AnimationManager
from game_entities import Player
from stamina import StaminaComponent
from map_generator import map_data_generator
from render import Collision_Checker
from collisions import check_collisions, collison_terrain
from inventory import render_inventory, call_inventory
from camera import box_target_camera


class Game:

    @staticmethod
    def handle_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    pygame.init()
    pygame.display.set_caption("Glorious Adventure - BETA")

    def __init__(self):
        self.collided_with = ()
        self.terrain_data_minerals = 0
        self.display_hit_box_decay = 0
        self.screen_x = 1000
        self.screen_y = 750
        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y))
        self.set_frame_rate = pygame.time.Clock()
        self.stamina_bar_decay = 0

        self.player = Player(
            max_health=20, min_health=0,
            max_stamina=20, min_stamina=0,
            base_speed=4, max_speed=10, min_speed=1
        )

        # Game-related attributes
        self.block_size = 100
        self.player_color = 'red'
        self.base_speed = 4
        self.generated_ground_images = {}
        self.grab_decay = 0

        self.inventory = {}  # Terve inv (prindi seda ja saad teada mis invis on)

        self.hit_boxes = []  # Objects data

        self.X_max = 1500 // self.block_size
        self.Y_max = 1500 // self.block_size
        self.center_x = self.X_max // 2
        self.center_y = self.Y_max // 2
        self.max_distance = min(self.center_x, self.center_y)
        self.terrain_data = map_data_generator(10)  # argument seed, default seed=None

        self.player_x = random.randint(500, 500)
        self.player_y = random.randint(375, 375)
        self.player_rect = pygame.Rect(self.player_x, self.player_y, self.block_size * 0.6, self.block_size * 0.75)
        # camera stuff
        self.camera_borders = {'left': 250, 'right': 250, 'top': 200, 'bottom': 200}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.screen.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.screen.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)

        # camera offset
        self.offset_x = 0
        self.offset_y = 0

        # *************** visual stuff ***************

        # stamina
        self.stamina_bar_decay = 0

        # stamina bar
        self.stamina_bar_size = 200
        self.stamina_bar_size_bg = 200
        self.stamina_bar_size_border = 200
        self.screen_x = 1000
        self.screen_y = 750
        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y))
        self.half_w = self.screen.get_size()[0] // 2
        self.ratio = self.stamina_bar_size // 20  # 200 // 20 = 10
        self.stamina_rect_bg = pygame.Rect(self.half_w - (self.stamina_bar_size_bg / 2) - 6, self.screen_y - 25, self.stamina_bar_size_bg + 12, 15)  # Kui staminat kulub, ss on background taga
        self.stamina_rect_border = pygame.Rect(self.half_w - (self.stamina_bar_size_border / 2) - 6, self.screen_y - 25, self.stamina_bar_size_border + 12, 15)  # K6igi stamina baride ymber border
        self.stamina_rect = pygame.Rect(self.half_w - (self.stamina_bar_size / 2) - 6, self.screen_y - 25, self.stamina_bar_size + 12, 15)

        # Animation shit
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

        # Set animation speeds
        self.animation_speeds = [10, 10, 10, 10]  # Example speeds, adjust as needed

        # Create AnimationManagers for both regular and idle animations
        self.animation_manager = AnimationManager(self.sprite_sheets, self.animations, self.animation_speeds)
        self.idle_animation_manager = AnimationManager(self.sprite_sheets_idle, self.animations_idle,
                                                       self.animation_speeds)

        self.render_inv = False  # Inventory renderminmine
        self.inv_count = 0  # Otsustab, kas renderida inv v6i mitte
        self.tab_pressed = False  # Keep track of whether Tab was pressed

        self.render_rect = pygame.Rect(0,0,0,0)


    # Uuendab player datat ja laseb tal liikuda
    def update_player(self):
        keys = pygame.key.get_pressed()  # Jälgib keyboard inputte

        # Teeb uue player x/y, algne x ja y tuleb playeri maailma panekuga (randint)
        new_player_x = self.player_x
        new_player_y = self.player_y

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

        if keys[pygame.K_a]:
            new_player_x = self.player_x - self.player.speed

        if keys[pygame.K_d]:
            new_player_x = self.player_x + self.player.speed

        if keys[pygame.K_w]:
            new_player_y = self.player_y - self.player.speed

        if keys[pygame.K_s]:
            new_player_y = self.player_y + self.player.speed

        # Kui seda pole siis player ei liigu mapi peal
        # Uuendab playeri asukohta vastavalt keyboard inputile
        self.player_x = new_player_x
        self.player_y = new_player_y
        self.player_rect = pygame.Rect(self.player_x, self.player_y, self.block_size * 0.6, self.block_size * 0.75)

        # Kui player seisab (Animationi jaoks - IDLE)
        is_idle = not (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s] or keys[
            pygame.K_e])

        if is_idle:
            self.frame = self.idle_animation_manager.update_animation(keys, is_idle)
        else:
            self.frame = self.animation_manager.update_animation(keys, is_idle)

        if self.frame is not None:
            self.sprite_rect = self.screen.blit(self.frame, (self.player_x, self.player_y))


    def render(self):

        # Muudab playeri asukohta vastavalt kaamera asukohale / paiknemisele
        player_position_adjusted = (self.player_x + self.offset_x, self.player_y + self.offset_y)
        if self.render_inv: # == True
            render_inventory(self)  # renderib inventory

        self.screen.blit(self.frame, player_position_adjusted)  # Renderib playeri animatsioni

        # Renderib stamina-bari
        if self.stamina_bar_decay < 50:
            pygame.draw.rect(self.screen, '#F7F7F6', self.stamina_rect_bg, 0, 7)
            pygame.draw.rect(self.screen, '#4169E1', self.stamina_rect, 0, 7)
            pygame.draw.rect(self.screen, 'black', self.stamina_rect_border, 2, 7)

        # Uuendab displaid ja fps cap 60
        pygame.display.flip()
        self.set_frame_rate.tick(60)


    def run(self):
        while True:
            self.handle_events()  # Paneb mängu õigesti kinni
            box_target_camera(self)  # Kaamera
            call_inventory(self)  # update playeri osa()
            self.update_player()  # Uuendab mängija asukohta, ja muid asju
            collison_terrain(self)  # Vaatab m2ngija kokkup6rkeid terrainiga
            check_collisions(self)  # Vaatab mängija kokkup6rkeid objecktidega
            StaminaComponent.stamina_bar_update(self)  # Stamina bar
            Collision_Checker.map_render(self)  # Renderib terraini
            Collision_Checker.object_render(self)  # Renderib objektid
            self.render()

if __name__ == "__main__":
    game = Game()
    game.run()