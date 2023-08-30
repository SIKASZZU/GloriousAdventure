# Pythoni inbuilt/downloaded files
import pygame
import sys
import random
import time

# Oma enda failid
from sprite import load_sprite_sheets, AnimationManager
from map_generator import new_island
from images import item_images
from game_entities import Player
from stamina import StaminaComponent
from world_objects import minerals
import inventory
import collisions
#import camera

class Game:

    @staticmethod
    def handle_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def __init__(self):
        self.collided_with = ()
        self.terrain_data_minerals = 0
        self.display_hit_box_decay = 0
        self.screen_x = 1000
        self.screen_y = 750
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y))
        pygame.display.set_caption("GA")
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
        self.generated_ground_images = None
        self.grab_decay = 0

        # Inventory display settings
        self.inventory_display_rects = [
            pygame.Rect(50, 50, 50, 50),
            pygame.Rect(100, 50, 50, 50),
            pygame.Rect(150, 50, 50, 50),
            pygame.Rect(200, 50, 50, 50),
            pygame.Rect(250, 50, 50, 50),
            pygame.Rect(300, 50, 50, 50),
            pygame.Rect(350, 50, 50, 50),
            pygame.Rect(400, 50, 50, 50),
            pygame.Rect(450, 50, 50, 50),
        ]

        self.inventory = {}  # Terve inv (prindi seda ja saad teada mis invis on)

        # Objects data
        self.hit_boxes = []

        self.X_max = 1500 // self.block_size
        self.Y_max = 1500 // self.block_size
        self.center_x = self.X_max // 2
        self.center_y = self.Y_max // 2
        self.max_distance = min(self.center_x, self.center_y)
        self.terrain_data = [[0 for _ in range(self.Y_max)] for _ in range(self.X_max)]
        new_island(self, 64)

        self.player_x = random.randint(500, 500)
        self.player_y = random.randint(375, 375)
        self.player_rect = pygame.Rect(self.player_x, self.player_y, self.block_size * 0.6, self.block_size * 0.75)

        # interaction box
        self.interaction_rect = pygame.Rect(0, 0, 0, 0)

        # camera stuff
        self.camera_borders = {'left': 100, 'right': 100, 'top': 100, 'bottom': 100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.screen.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.screen.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)

        # camera offset
        self.offset_x = 0
        self.offset_y = 0

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

    # Teeb boxi, kui minna sellele vastu, siis liigub kaamera
    def box_target_camera(self):
        if self.player_rect.left < self.camera_rect.left:
            self.camera_rect.left = self.player_rect.left

        if self.player_rect.right > self.camera_rect.right:
            self.camera_rect.right = self.player_rect.right

        if self.player_rect.top < self.camera_rect.top:
            self.camera_rect.top = self.player_rect.top

        if self.player_rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = self.player_rect.bottom

        self.offset_x = self.camera_borders['left'] - self.camera_rect.left
        self.offset_y = self.camera_borders['top'] - self.camera_rect.top

    # Uuendab player datat ja laseb tal liikuda
    def update_player(self):
        keys = pygame.key.get_pressed()  # Jälgib keyboard inputte

        # Teeb uue player x/y, algne x ja y tuleb playeri maailma panekuga (randint)
        new_player_x = self.player_x
        new_player_y = self.player_y

        # Playeri itemite korjamise kast
        interaction_x = self.player_rect.left + self.offset_x
        interaction_y = self.player_rect.top + self.offset_y

        if keys[pygame.K_TAB] and not self.tab_pressed:  # double locked, yks alati true aga teine mitte
            self.tab_pressed = True

            self.inv_count += 1
            print('self.inv_count', self.inv_count)

            if (self.inv_count % 2) == 0:
                self.render_inv = False
                print('Render inv false')
            else:
                self.render_inv = True
                print('Render inv true')

            print('inv_count', self.inv_count)

        elif not keys[pygame.K_TAB]:
            self.tab_pressed = False

        else:
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
            self.interaction_rect = pygame.Rect(interaction_x - self.block_size * 2, interaction_y - self.block_size / 1.35, 2 * self.block_size, 2 * self.block_size)

        if keys[pygame.K_d]:
            new_player_x = self.player_x + self.player.speed
            self.interaction_rect = pygame.Rect(interaction_x + self.block_size / 2, interaction_y - self.block_size / 1.35, 2 * self.block_size, 2 * self.block_size)

        if keys[pygame.K_w]:
            new_player_y = self.player_y - self.player.speed
            self.interaction_rect = pygame.Rect(interaction_x - self.block_size / 1.35, interaction_y - self.block_size * 2, 2 * self.block_size, 2 * self.block_size)

        if keys[pygame.K_s]:
            new_player_y = self.player_y + self.player.speed
            self.interaction_rect = pygame.Rect(interaction_x - self.block_size / 1.35, interaction_y + self.block_size / 2, 2 * self.block_size, 2 * self.block_size)

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

    def get_object_id_at_position(self, x, y):
        terrain_x = x - self.offset_x
        terrain_y = y - self.offset_y
        grid_col = terrain_x // self.block_size
        grid_row = terrain_y // self.block_size
        return self.terrain_data[grid_row][grid_col]

    # eemaldab objekti ning lisab selle inventory
    def remove_object_at_position(self, x, y, terrain_x, terrain_y, obj_hit_box, object_id=None):
        items_found = set()  # Hoiab leitud esemed
        item_count = {}  # Hoiab leitud esemete arve
        
        # itemi eemaldamine visuaalselt
        grid_col = terrain_x // self.block_size
        grid_row = terrain_y // self.block_size

        if 0 <= grid_row < len(self.terrain_data) and 0 <= grid_col < len(self.terrain_data[0]):
            grid_col = int(terrain_x //self.block_size)
            grid_row = int(terrain_y //self.block_size)

            if object_id == 4: 
                grid_col += 1
                grid_row += 1
            self.terrain_data[grid_row][grid_col] = 1

            # itemi lisamine playeri inventorisse
            for item_name, item_values in minerals.items():
                if object_id == item_values[2]:
                    print(object_id, item_values[2])
                    items_found.add(item_name)

            try:
                for item_name in items_found:
                    item_count[item_name] = 0  # Resetib itemi koguse kuna muidu fkupiks...

                    for item_name, item_values in minerals.items():
                        if object_id == item_values[2] and item_name in items_found:
                            item_count[item_name] += 1
                            items_found.remove(item_name)  # Eemaldab eseme leitud hulgast

                            # Lisab eseme inventuuri dicti
                            if item_name in self.inventory:
                                self.inventory[item_name] += 1
                            else:
                                self.inventory[item_name] = 1

                            self.grab_decay = 0        
            except RuntimeError:
                print('RuntimeError')

        else:
            print("Invalid grid indices:", grid_row, grid_col)

        index = self.hit_boxes.index(obj_hit_box)
        self.hit_boxes.pop(index)



    def place_and_render_object(self, object_id, obj_image, obj_x, obj_y,
                                 obj_width, obj_height, hit_box_color,
                                 hit_box_x, hit_box_y, hit_box_width, hit_box_height):
        if obj_image:
            # Kui mineral on puu siis annab eraldi koordinaadid
            if object_id == 4:
                # Render object image
                scaled_obj_image = pygame.transform.scale(obj_image, (obj_width, obj_height))
                self.screen.blit(scaled_obj_image, (obj_x - self.block_size / 2, obj_y - self.block_size))

                # Draw hit box
                obj_hit_box = pygame.Rect(hit_box_x - self.block_size / 2, hit_box_y - self.block_size, hit_box_width, hit_box_height)
                pygame.draw.rect(self.screen, hit_box_color, obj_hit_box, 2)

            else:
                # Render object image
                scaled_obj_image = pygame.transform.scale(obj_image, (obj_width, obj_height))
                self.screen.blit(scaled_obj_image, (obj_x, obj_y))

                # Draw hit box
                obj_hit_box = pygame.Rect(hit_box_x, hit_box_y, hit_box_width, hit_box_height)
                pygame.draw.rect(self.screen, hit_box_color, obj_hit_box, 2)

    def render(self):
        self.screen.fill('blue')

        # Loopib läbi terrain data ja saab x ja y ja renerib vee ja maa
        for i in range(len(self.terrain_data)):
            for j in range(len(self.terrain_data[i])):
                terrain_x = j * self.block_size + self.offset_x
                terrain_y = i * self.block_size + self.offset_y

                # Renderib GROUND pildid
                ground_image = self.generated_ground_images.get((i, j))
                if ground_image:
                    ground_image = pygame.transform.scale(ground_image, (self.block_size, self.block_size))
                    self.screen.blit(ground_image, (terrain_x, terrain_y))

        # Loopib läbi terrain data ja saab x ja y
        for i in range(len(self.terrain_data)):
            for j in range(len(self.terrain_data[i])):
                terrain_x = j * self.block_size + self.offset_x
                terrain_y = i * self.block_size + self.offset_y

                if self.terrain_data[i][j] == 2 or self.terrain_data[i][j] == 4:
                    self.terrain_data_minerals += 1

                # Jätab muud blockid välja millele pole hit boxe vaja
                if self.terrain_data[i][j] != 0:

                    # Peavad olema muidu järgnevates if statementides tulevad errorid
                    object_id = self.terrain_data[i][j]
                    obj_image = None
                    obj_width = 0
                    obj_height = 0
                    hit_box_width = 0
                    hit_box_height = 0
                    hit_box_color = ''
                    hit_box_offset_x = 0
                    hit_box_offset_y = 0

                    # Vaatab kas terrain data on kivi
                    if object_id == 2:
                        obj_image = item_images.get("Rock")
                        hit_box_color = 'green'

                        obj_width = int(self.block_size * 1)
                        obj_height = int(self.block_size * 0.8)

                        # Pane TOP-LEFT otsa järgi paika
                        # ja siis muuda - palju lihtsam
                        hit_box_width = int(obj_width * 0.5)
                        hit_box_height = int(obj_height * 0.5)
                        hit_box_offset_x = int(obj_width * 0.3)
                        hit_box_offset_y = int(obj_height * 0.25)

                    # Vaatab kas terrain data on puu
                    elif object_id == 4:
                        obj_image = item_images.get("Tree")
                        hit_box_color = 'green'

                        # Pane TOP-LEFT otsa järgi paika
                        # ja siis muuda - palju lihtsam
                        obj_width = int(self.block_size * 2)
                        obj_height = int(self.block_size * 2)
                        hit_box_width = int(obj_width * 0.25)
                        hit_box_height = int(obj_height * 0.65)

                        hit_box_offset_x = int(obj_width * 0.4)
                        hit_box_offset_y = int(obj_height * 0.2)

                    # Arvutab hit boxi positsiooni
                    # Default hit box on terrain_x ja terrain_y
                    hit_box_x = terrain_x + hit_box_offset_x
                    hit_box_y = terrain_y + hit_box_offset_y

                    if object_id != 0:
                        if object_id != 1:
                            if self.display_hit_box_decay <= self.terrain_data_minerals:

                                self.hit_boxes.append((hit_box_x, hit_box_y, hit_box_width, hit_box_height, object_id,

                                                       # Et saada terrain_x/y def remove_object_at_position():'s
                                                       hit_box_offset_x, hit_box_offset_y))

                                self.display_hit_box_decay += 1


                            self.place_and_render_object(object_id, obj_image, terrain_x, terrain_y,
                                                         obj_width, obj_height, hit_box_color,
                                                         hit_box_x, hit_box_y, hit_box_width, hit_box_height)

        self.terrain_data_minerals = 0

        # Muudab playeri asukohta vastavalt kaamera asukohale / paiknemisele
        player_position_adjusted = (
            self.player_x + self.offset_x,
            self.player_y + self.offset_y
        )

        if self.render_inv: # == True
            inventory.render_inventory(self)


        # Renderib playeri animatsioni
        self.screen.blit(self.frame, player_position_adjusted)

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
            self.box_target_camera()
            self.update_player()  # Uuendab mängija asukohta, ja muid asju
            collisions.check_collisions(self)  # Vaatab mängija ja maastiku kokkupõrkeidW
            StaminaComponent.stamina_bar_update(self)  # Stamina bar
            self.render()  # Renderib terraini

if __name__ == "__main__":
    game = Game()
    game.run()

