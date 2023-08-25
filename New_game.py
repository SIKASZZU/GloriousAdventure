import pygame
import sys
import random

from world_objects import minerals
from game_entities import Player


class Game:

    @staticmethod
    def handle_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def __init__(self):
        self.screen_x = 1000
        self.screen_y = 750
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y))
        pygame.display.set_caption("GA")
        self.set_frame_rate = pygame.time.Clock()

        self.player = Player(
            max_health=20, min_health=0,
            max_stamina=20, min_stamina=0,
            base_speed=4, max_speed=10, min_speed=1
        )

        # Game-related attributes
        self.block_size = 100
        self.player_color = 'red'
        self.REGENERATION_DELAY = 2
        self.stamina_regeneration_timer = 0
        self.base_speed = 4

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

        # Itemite pildid
        self.item_images = {
            "Tree": pygame.image.load("images/Tree.PNG"),
            "Stone": pygame.image.load("images/Stone.PNG"),
            "Rock": pygame.image.load("images/Rock.PNG"),
            "Water": pygame.image.load("images/Water.PNG"),
        }

        self.land_images = {"Ground_0": pygame.image.load("images/Ground/Ground_0.png"),
                            "Ground_1": pygame.image.load("images/Ground/Ground_1.png"),
                            "Ground_2": pygame.image.load("images/Ground/Ground_2.png"),
                            "Ground_3": pygame.image.load("images/Ground/Ground_3.png"),
                            "Ground_4": pygame.image.load("images/Ground/Ground_4.png"),
                            "Ground_5": pygame.image.load("images/Ground/Ground_5.png"),
                            "Ground_6": pygame.image.load("images/Ground/Ground_6.png"),
                            "Ground_7": pygame.image.load("images/Ground/Ground_7.png"),
                            "Ground_8": pygame.image.load("images/Ground/Ground_8.png"),
                            "Ground_9": pygame.image.load("images/Ground/Ground_9.png"),
                            "Ground_10": pygame.image.load("images/Ground/Ground_10.png"),
                            "Ground_11": pygame.image.load("images/Ground/Ground_11.png"),
                            "Ground_12": pygame.image.load("images/Ground/Ground_12.png"),
                            "Ground_13": pygame.image.load("images/Ground/Ground_13.png"),
                            "Ground_14": pygame.image.load("images/Ground/Ground_14.png"),
                            "Ground_15": pygame.image.load("images/Ground/Ground_15.png"),
                            "Ground_16": pygame.image.load("images/Ground/Ground_16.png"),
                            "Ground_17": pygame.image.load("images/Ground/Ground_17.png"),
                            "Ground_18": pygame.image.load("images/Ground/Ground_18.png"),
                            "Ground_19": pygame.image.load("images/Ground/Ground_19.png"),
                            }

        self.X_max = 1500 // self.block_size
        self.Y_max = 1500 // self.block_size
        self.center_x = self.X_max // 2
        self.center_y = self.Y_max // 2
        self.max_distance = min(self.center_x, self.center_y)

        self.terrain_data = [[0 for _ in range(self.Y_max)] for _ in range(self.X_max)]
        # # # # # Seed # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        self.new_island(64)

        self.player_x = random.randint(400, 600)
        self.player_y = random.randint(200, 550)

        # camera stuff
        self.camera_borders = {'left': 100, 'right': 100, 'top': 100, 'bottom': 100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.screen.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.screen.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)

        # interaction box
        self.interaction_rect = pygame.Rect(0, 0, 0, 0)

        # camera offset
        self.offset_x = 0
        self.offset_y = 0

        # stamina bar
        self.stamina_bar_size = 200
        self.stamina_bar_size_bg = 200
        self.stamina_bar_size_border = 200
        self.half_w = self.screen.get_size()[0] // 2

        self.stamina_bar_decay = 0
        self.ratio = self.stamina_bar_size // self.player.stamina.max_stamina  # 200 // 20 = 10

        self.stamina_rect_bg = pygame.Rect(self.half_w - (self.stamina_bar_size_bg / 2) - 6, self.screen_y - 25, self.stamina_bar_size_bg + 12, 15)  # Kui staminat kulub, ss on background taga
        self.stamina_rect_border = pygame.Rect(self.half_w - (self.stamina_bar_size_border / 2) - 6, self.screen_y - 25, self.stamina_bar_size_border + 12, 15)  # K6igi stamina baride ymber border
        self.stamina_rect = pygame.Rect(self.half_w - (self.stamina_bar_size / 2) - 6, self.screen_y - 25, self.stamina_bar_size + 12, 15)

    def stamina_bar_update(self):
        if self.stamina_bar_decay == 120:
            self.stamina_rect_bg = pygame.Rect(0, 0, 0, 0)
            self.stamina_rect = pygame.Rect(0, 0, 0, 0)
            self.stamina_rect_border = pygame.Rect(0, 0, 0, 0)

        if self.player.stamina.current_stamina >= self.player.stamina.max_stamina:
            self.stamina_bar_decay += 1
        else:
            self.stamina_bar_size = self.player.stamina.current_stamina * self.ratio  # arvutab stamina bari laiuse
            self.stamina_rect_bg = pygame.Rect(self.half_w - (self.stamina_bar_size_bg / 2) - 6, self.screen_y - 25, self.stamina_bar_size_bg + 12, 15)  # Kui staminat kulub, ss on background taga
            self.stamina_rect_border = pygame.Rect(self.half_w - (self.stamina_bar_size_border / 2) - 6, self.screen_y - 25, self.stamina_bar_size_border + 12, 15)  # K6igi stamina baride ymber border
            self.stamina_rect = pygame.Rect(self.half_w - (self.stamina_bar_size / 2) - 6, self.screen_y - 25, self.stamina_bar_size + 12, 15)

    def render_inventory(self):
        # Invi hall taust
        inventory_bar_rect = pygame.Rect(50, 50, 450, 50)
        pygame.draw.rect(self.screen, '#B1B1B1', inventory_bar_rect)

        # Mustad boxid itemite ümber
        for rect in self.inventory_display_rects:
            pygame.draw.rect(self.screen, 'black', rect, 2)

        for rect, (item_name, count) in zip(self.inventory_display_rects, self.inventory.items()):
            item_color = minerals.get(item_name, 'black')
            item_rect = pygame.Rect(rect.x + 3, rect.y + 3, rect.width - 6, rect.height - 6)
            pygame.draw.rect(self.screen, item_color, item_rect)

            # Paneb invile pildid
            item_image = self.item_images.get(item_name)
            if item_image is not None:
                # Resize
                item_image = pygame.transform.scale(item_image, (int(rect.width / 1.4), int(rect.height / 1.4)))

                # Paneb itembi invi boxi keskele
                item_image_rect = item_image.get_rect(center=item_rect.center)

                # Displayb resized itemit
                self.screen.blit(item_image, item_image_rect.topleft)

            font = pygame.font.Font(None, 20)
            text = font.render(str(count), True, 'White')
            text_rect = text.get_rect(center=(rect.x+10, rect.y+10))
            self.screen.blit(text, text_rect)

        inventory_bar_rect = pygame.Rect(50, 50, 450, 50)
        pygame.draw.rect(self.screen, 'black', inventory_bar_rect, 4)  # Paksem border

    # Koostab uue saare
    def new_island(self, seed):
        self.generated_ground_images = {}

        # Seadistab juhuarvu genereerija seediga
        random.seed(seed)
        for x in range(self.X_max):
            for y in range(self.Y_max):
                # Leiab kauguse keskpunktist
                distance_to_center = ((x - self.center_x) ** 2 + (y - self.center_y) ** 2) ** 0.5
                normalized_distance = distance_to_center / self.max_distance
                land_probability = 1 - (normalized_distance ** 213)

                # Määrab pinnase maapinnaks, kui juhuslik arv on väiksem kui maapinna tõenäosus
                if random.random() < land_probability:
                    self.terrain_data[x][y] = 1

                    # Määrab juhusliku pinnase pildi genereeritud maapinnatüübile
                    if not self.generated_ground_images.get((x, y)):
                        ground_image_name = f"Ground_{random.randint(0, 19)}"
                        ground_image = self.land_images.get(ground_image_name)
                        self.generated_ground_images[(x, y)] = ground_image

        # Genereerib kivid ja puud
        for i in range(len(self.terrain_data)):
            for j in range(len(self.terrain_data[i])):
                if self.terrain_data[i][j] == 1:
                    # Kontrollib, kas lahter peaks olema kivi või puu
                    if random.random() < 0.03:
                        self.terrain_data[i][j] = 2  # Kivi
                    elif random.random() < 0.04:
                        self.terrain_data[i][j] = 4  # Puu

    def update_player(self):
        keys = pygame.key.get_pressed()
        new_player_x = self.player_x
        new_player_y = self.player_y

        if keys[pygame.K_a]:
            new_player_x = self.player_x - self.player.speed
            interaction_x = self.player_rect.left + self.offset_x
            interaction_y = self.player_rect.top + self.offset_y
            self.interaction_rect = pygame.Rect(interaction_x - self.block_size * 2,
                                                interaction_y - self.block_size / 1.35,
                                                2 * self.block_size, 2 * self.block_size)

        if keys[pygame.K_d]:
            new_player_x = self.player_x + self.player.speed
            interaction_x = self.player_rect.left + self.offset_x
            interaction_y = self.player_rect.top + self.offset_y
            self.interaction_rect = pygame.Rect(interaction_x + self.block_size / 2,
                                                interaction_y - self.block_size / 1.35,
                                                2 * self.block_size, 2 * self.block_size)

        if keys[pygame.K_w]:
            new_player_y = self.player_y - self.player.speed
            interaction_x = self.player_rect.left + self.offset_x
            interaction_y = self.player_rect.top + self.offset_y
            self.interaction_rect = pygame.Rect(interaction_x - self.block_size / 1.35,
                                                interaction_y - self.block_size * 2,
                                                2 * self.block_size, 2 * self.block_size)

        if keys[pygame.K_s]:
            new_player_y = self.player_y + self.player.speed
            interaction_x = self.player_rect.left + self.offset_x
            interaction_y = self.player_rect.top + self.offset_y
            self.interaction_rect = pygame.Rect(interaction_x - self.block_size / 1.35,
                                                interaction_y + self.block_size / 2,
                                                2 * self.block_size, 2 * self.block_size)

        if keys[pygame.K_w]:
            new_player_y = self.player_y - self.player.speed
            interaction_x = self.player_rect.left + self.offset_x
            interaction_y = self.player_rect.top + self.offset_y

        # Update player's position and stamina
        self.player_x = new_player_x
        self.player_y = new_player_y
        self.player.speed = 4

        # Kui hoitakse all Shifti ja a, d, w, s:
        # Muudetakse playeri speedi ja võetakse staminat.
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
                self.stamina_bar_decay = 0  # Kui stamina bari pole siis tuleb kui player liigub
                self.player.speed = 20
                self.player.stamina.use_stamina(0.05)

            # Kui stamina on 0 siis playeri speed läheb sama
            # kiireks kui enne shifti vajutamist oli.
            if self.player.stamina.current_stamina == 0:
                self.player.speed = self.base_speed
            else:
                self.player.stamina.stamina_regenerate(0.05)

        # Kui ei hoia shifti all siis regeneb staminat
        if not keys[pygame.K_LSHIFT] and not keys[pygame.K_RSHIFT]:
            self.player.stamina.stamina_regenerate(0.05)
            self.player.speed = 4

        self.player_rect = pygame.Rect(self.player_x, self.player_y, self.block_size, self.block_size)

    def check_collisions(self):
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
                        self.player.speed = 4

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
                        item_image = self.item_images.get("Rock")
                    elif self.terrain_data[i][j] == 4:
                        item_image = self.item_images.get("Tree")
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

        # Joonistab stamina ribad ja mängija asukoha markeri
        if self.stamina_bar_decay < 50:
            pygame.draw.rect(self.screen, '#F7F7F6', self.stamina_rect_bg, 0, 7)
            pygame.draw.rect(self.screen, '#4169E1', self.stamina_rect, 0, 7)
            pygame.draw.rect(self.screen, 'black', self.stamina_rect_border, 2, 7)

        pygame.draw.rect(self.screen, 'yellow', self.interaction_rect, 2)
        pygame.draw.rect(self.screen, self.player_color, player_rect_adjusted)

        # Renderdab inventuuri
        self.render_inventory()

        # Värskendab ekraani ja hoiab mängu kiirust 60 kaadrit sekundis
        pygame.display.flip()
        self.set_frame_rate.tick(60)

    def item_interaction(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            items_found = set()  # Hoiab leitud esemed
            item_count = {}  # Hoiab leitud esemete arve

            for i in range(len(self.terrain_data)):
                for j in range(len(self.terrain_data[i])):
                    terrain_x = j * self.block_size + self.offset_x
                    terrain_y = i * self.block_size + self.offset_y
                    if self.interaction_rect.collidepoint(terrain_x, terrain_y):
                        for item_name, item_values in minerals.items():
                            if self.terrain_data[i][j] == item_values[2]:
                                items_found.add(item_name)  # Lisab leitud eseme nime

            for item_name in items_found:
                item_count[item_name] = 0  # Resetib itemi koguse kuna muidu fkupiks...

            for i in range(len(self.terrain_data)):
                for j in range(len(self.terrain_data[i])):
                    terrain_x = j * self.block_size + self.offset_x
                    terrain_y = i * self.block_size + self.offset_y
                    if self.interaction_rect.collidepoint(terrain_x, terrain_y):
                        for item_name, item_values in minerals.items():
                            if self.terrain_data[i][j] == item_values[2] and item_name in items_found:
                                item_count[item_name] += 1
                                self.terrain_data[i][j] = 1  # Muudab terraini datat et maailm muutuks
                                items_found.remove(item_name)  # Eemaldab eseme leitud hulgast

                                # Lisab eseme inventuuri dicti
                                if item_name in self.inventory:
                                    self.inventory[item_name] += 1
                                else:
                                    self.inventory[item_name] = 1

            # Prindib leitud asjad ja koguse
            print("inv:")
            for item_name, count in self.inventory.items():
                if count == 1:
                    print(f"{count} {item_name}")
                else:
                    print(f"{count} {item_name}s")
                    print(self.inventory.items())

    def run(self):
        while True:
            self.handle_events()  # Paneb mängu õigesti kinni
            self.update_player()  # Uuendab mängija asukohta, ja muid asju
            self.check_collisions()  # Vaatab mängija ja maastiku kokkupõrkeid
            self.box_target_camera()  # Box camera, et player ei saaks boxist välja minna vms
            self.stamina_bar_update()  # Stamina bar
            self.render()  # Renderib terraini
            self.item_interaction()  # Loeb ja korjab itemeid

            # print(self.player_x,
            #       self.player_y)


if __name__ == "__main__":
    game = Game()
    game.run()
