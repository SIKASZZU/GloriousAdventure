import pygame
import sys
import random

from sprite import SpriteSheet
from map_generator import new_island
from images import item_images
from game_entities import Player
from camera import Camera
import stamina
import inventory

class Game:

    @staticmethod
    def handle_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def __init__(self):
        self.offset_y = None
        self.offset_x = None
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

        self.X_max = 1500 // self.block_size
        self.Y_max = 1500 // self.block_size
        self.center_x = self.X_max // 2
        self.center_y = self.Y_max // 2
        self.max_distance = min(self.center_x, self.center_y)

        self.terrain_data = [[0 for _ in range(self.Y_max)] for _ in range(self.X_max)]

        new_island(self, 64)

        self.player_x = random.randint(400, 600)
        self.player_y = random.randint(200, 550)
        self.player_rect = pygame.Rect(self.player_x, self.player_y, self.block_size, self.block_size)

        # interaction box
        self.interaction_rect = pygame.Rect(0, 0, 0, 0)

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



        self.sprite_sheet_left = pygame.image.load('images/Player/Left.png').convert_alpha()
        self.sprite_sheet_right = pygame.image.load('images/Player/Right.png').convert_alpha()
        self.sprite_sheet_up = pygame.image.load('images/Player/Up.png').convert_alpha()
        self.sprite_sheet_down = pygame.image.load('images/Player/Down.png').convert_alpha()

        self.sprite_idle_left = pygame.image.load('images/Player/Idle_Left.png').convert_alpha()
        self.sprite_idle_right = pygame.image.load('images/Player/Idle_Right.png').convert_alpha()
        self.sprite_idle_up = pygame.image.load('images/Player/Idle_Up.png').convert_alpha()
        self.sprite_idle_down = pygame.image.load('images/Player/Idle_Down.png').convert_alpha()

        self.sprite_sheets = [self.sprite_sheet_left, self.sprite_sheet_right, self.sprite_sheet_up, self.sprite_sheet_down]
        self.sprite_sheets_idle = [self.sprite_idle_left, self.sprite_idle_right, self.sprite_idle_up, self.sprite_idle_down]

        self.animations = [
            [(0, 0), (65, 65)],
            [(0, 0), (65, 65)],
            [(0, 0), (65, 65)],
            [(0, 0), (65, 65)]
        ]

        self.animations_idle = [
            [(0, 0), (65, 65)],
            [(0, 0), (65, 65)],
            [(0, 0), (65, 65)],
            [(0, 0), (65, 65)]
        ]

        self.animation_index = 0  # Start with left animation
        self.frame_index = 0
        self.idle_frame_index = 0
        self.frame_delay = 10  # Adjust the delay based on animation speed
        self.idle_frame_delay = 5  # Adjust the delay for idle animation

        self.clock = pygame.time.Clock()

# Uuendab player datat ja laseb tal liikuda
    def update_player(self):
        # Jälgib keyboard inputte
        keys = pygame.key.get_pressed()


        # Teeb uue player x/y, algne x ja y tuleb playeri maailma panekuga (randint)
        new_player_x = self.player_x
        new_player_y = self.player_y

        # Playeri itemite korjamise kast
        interaction_x = self.player_rect.left + self.offset_x
        interaction_y = self.player_rect.top + self.offset_y

        # Kui player korjab midagi ülesse (Animationi jaoks - GRABBING)
        # 20 fps cooldown
        if keys[pygame.K_e]:
            if self.grab_decay >= 20:
                inventory.item_interaction(self) # Loeb ja korjab itemeid

            else:
                self.grab_decay += 1

        # Kui player seisab (Animationi jaoks - IDLE)
        if not (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_e]):
            sprite_sheet_idle = SpriteSheet(self.sprite_sheets_idle[self.animation_index])
            x, y = self.animations_idle[self.animation_index][0]
            width, height = self.animations_idle[self.animation_index][1]
            self.frame = sprite_sheet_idle.get_image(x + self.idle_frame_index * width, y, width, height)
            self.idle_frame_index = (self.idle_frame_index + 1) % 2  # Assuming 2 frames for idle animation
            self.frame_delay = self.idle_frame_delay

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
            # Animation VASAKULE + animationi kiirus (in fps)

        if keys[pygame.K_d]:
            new_player_x = self.player_x + self.player.speed
            self.interaction_rect = pygame.Rect(interaction_x + self.block_size / 2, interaction_y - self.block_size / 1.35, 2 * self.block_size, 2 * self.block_size)
            # Animation PAREMALE + animationi kiirus (in fps)

        if keys[pygame.K_w]:
            new_player_y = self.player_y - self.player.speed
            self.interaction_rect = pygame.Rect(interaction_x - self.block_size / 1.35, interaction_y - self.block_size * 2, 2 * self.block_size, 2 * self.block_size)
            # Animation ÜLESSE + animationi kiirus (in fps)

        if keys[pygame.K_s]:
            new_player_y = self.player_y + self.player.speed
            self.interaction_rect = pygame.Rect(interaction_x - self.block_size / 1.35, interaction_y + self.block_size / 2, 2 * self.block_size, 2 * self.block_size)
            # Animation ALLA + animationi kiirus (in fps)

        # Kui hoitakse all Shifti ja a, d, w, s:
        # Muudetakse playeri speedi ja võetakse staminat.
        if keys[pygame.K_LSHIFT]:
            if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
                self.stamina_bar_decay = 0  # Kui stamina bari pole siis tuleb kui player liigub
                self.player.speed = self.base_speed * 5
                self.player.stamina.use_stamina(0.05)

                # Kiirendab animationi - näeb välja nagu jookseks
                # animationi kiirus * 2 (in fps)

            # stamina = 0 --- playeri speed = base speed
            if self.player.stamina.current_stamina == 0:
                self.player.speed = self.base_speed
                self.player.stamina.stamina_regenerate(0.05)

        # Kui ei hoia shifti all siis regeneb staminat
        if not keys[pygame.K_LSHIFT]:
            self.player.stamina.stamina_regenerate(0.05)
            self.player.speed = self.base_speed

        # Kui seda pole siis player ei liigu mapi peal
        # Uuendab playeri asukohta vastavalt keyboard inputile
        self.player_x = new_player_x
        self.player_y = new_player_y
        self.player_rect = pygame.Rect(self.player_x, self.player_y, self.block_size, self.block_size)

        sprite_sheet = SpriteSheet(self.sprite_sheets[self.animation_index])
        x, y = self.animations[self.animation_index][0]
        width, height = self.animations[self.animation_index][1]
        self.frame = sprite_sheet.get_image(x + self.frame_index * width, y, width, height)
        self.frame_index = (self.frame_index + 1) % 4  # Assuming 4 frames per animation

        self.screen.blit(self.frame, (self.player_x, self.player_y))

    def check_collisions(self):
        keys = pygame.key.get_pressed()
        for i in range(len(self.terrain_data)):
            for j in range(len(self.terrain_data[i])):
                terrain_rect = pygame.Rect(
                    j * self.block_size,
                    i * self.block_size,
                    self.block_size,
                    self.block_size
                )

                if self.player_rect.colliderect(terrain_rect):
                    in_water = any(
                        self.terrain_data[row][col] == 0
                        for row in range(i, i - 1, -1)
                        for col in range(j, j - 1, -1)
                    )

                    if in_water:
                        if keys[pygame.K_LSHIFT]:
                            self.player.speed = self.base_speed

                        else:
                            self.player.speed = self.base_speed / 2

    def render(self):
        # Tühjendab ekraani siniseks
        self.screen.fill('blue')

        # Joonistab maastiku
        for i in range(len(self.terrain_data)):
            for j in range(len(self.terrain_data[i])):
                terrain_x = j * self.block_size + self.offset_x
                terrain_y = i * self.block_size + self.offset_y

                # Joonistab maapinna
                ground_image = self.generated_ground_images.get((i, j))
                if ground_image:
                    ground_image = pygame.transform.scale(ground_image, (self.block_size, self.block_size))
                    self.screen.blit(ground_image, (terrain_x, terrain_y))

                # Joonistab objekte, kui andmetel pole väärtus 0 (vesi)
                if self.terrain_data[i][j] != 0:
                    item_image = None
                    if self.terrain_data[i][j] == 2:
                        item_image = item_images.get("Rock")
                    elif self.terrain_data[i][j] == 4:
                        item_image = item_images.get("Tree")
                        if item_image:
                            # Suurendab puu suurust
                            item_image = pygame.transform.scale(item_image, (self.block_size * 2, self.block_size * 2))
                            self.screen.blit(item_image, (terrain_x - self.block_size, terrain_y - self.block_size))
                            continue  # Jätkab järgmise ploki renderdamist, kui puu on suurendatud

                    if item_image is not None:
                        item_image = pygame.transform.scale(item_image, (self.block_size, self.block_size))
                        self.screen.blit(item_image, (terrain_x, terrain_y))

        # Korrigeerib mängija suurust ja asukohta vastavalt kaamerale
        player_rect_adjusted = pygame.Rect(
            self.player_rect.left + self.offset_x,
            self.player_rect.top + self.offset_y,
            self.block_size / 2,
            self.block_size / 2,
        )

        # Korrigeerib mängija suurust ja asukohta vastavalt kaamerale
        player_position_adjusted = (
            self.player_x + self.offset_x,
            self.player_y + self.offset_y
        )

        # Joonistab stamina ribad ja mängija asukoha markeri
        if self.stamina_bar_decay < 50:
            pygame.draw.rect(self.screen, '#F7F7F6', self.stamina_rect_bg, 0, 7)
            pygame.draw.rect(self.screen, '#4169E1', self.stamina_rect, 0, 7)
            pygame.draw.rect(self.screen, 'black', self.stamina_rect_border, 2, 7)

        pygame.draw.rect(self.screen, 'yellow', self.interaction_rect, 2)
        pygame.draw.rect(self.screen, self.player_color, player_rect_adjusted)

        # Renderdab inventuuri
        inventory.render_inventory(self)

        # Blit the animation frame at the player's current position
        self.screen.blit(self.frame, player_position_adjusted)

        # Värskendab ekraani ja hoiab mängu kiirust 60 kaadrit sekundis
        pygame.display.flip()
        self.set_frame_rate.tick(60)


    def run(self):
        while True:
            self.handle_events()  # Paneb mängu õigesti kinni
            Camera.box_target_camera(self)  # Box camera, et player ei saaks boxist välja minna vms
            self.update_player()  # Uuendab mängija asukohta, ja muid asju
            self.check_collisions()  # Vaatab mängija ja maastiku kokkupõrkeidW
            stamina.stamina_bar_update(self)  # Stamina bar
            self.render()  # Renderib terraini

if __name__ == "__main__":
    game = Game()
    game.run()
