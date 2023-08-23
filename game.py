import pygame
import sys
import random

from game_entities import Player


class Game:

    @staticmethod
    def handle_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 750))
        pygame.display.set_caption("GA")
        self.set_frame_rate = pygame.time.Clock()

        self.player = Player(
            max_health=20, min_health=0,
            max_stamina=20, min_stamina=0,
            health_regeneration_rate=0.5,
            base_speed=4, max_speed=10, min_speed=0.5
        )

        # Game-related attributes
        self.block_size = 25
        self.player_color = 'red'
        self.REGENERATION_DELAY = 2
        self.stamina_regeneration_timer = 0
        self.base_speed = 4

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

        self.stamina_rect_bg = pygame.Rect(self.half_w - (self.stamina_bar_size_bg / 2) - 6, 725, self.stamina_bar_size_bg + 12, 15)  # Kui staminat kulub, ss on background taga
        self.stamina_rect_border = pygame.Rect(self.half_w - (self.stamina_bar_size_border / 2) - 6, 725, self.stamina_bar_size_border + 12, 15)  # K6igi stamina baride ymber border
        self.stamina_rect = pygame.Rect(self.half_w - (self.stamina_bar_size / 2) - 6, 725, self.stamina_bar_size + 12, 15)

    def stamina_bar_update(self):
        if self.stamina_bar_decay == 120:
            self.stamina_rect_bg = pygame.Rect(0, 0, 0, 0)
            self.stamina_rect = pygame.Rect(0, 0, 0, 0)
            self.stamina_rect_border = pygame.Rect(0, 0, 0, 0)

        if self.player.stamina.current_stamina >= self.player.stamina.max_stamina:
            self.stamina_bar_decay += 1
        else:
            self.stamina_bar_size = self.player.stamina.current_stamina * self.ratio  # arvutab stamina bari laiuse
            self.stamina_rect_bg = pygame.Rect(self.half_w - (self.stamina_bar_size_bg / 2) - 6,725, self.stamina_bar_size_bg + 12, 15)  # Kui staminat kulub, ss on background taga
            self.stamina_rect_border = pygame.Rect(self.half_w - (self.stamina_bar_size_border / 2) - 6, 725, self.stamina_bar_size_border + 12, 15)  # K6igi stamina baride ymber border
            self.stamina_rect = pygame.Rect(self.half_w - (self.stamina_bar_size / 2) - 6, 725, self.stamina_bar_size + 12, 15)

    # Koostab islandi
    def new_island(self, seed):

        # Mapile tekib seed nagu Minecraftis vms
        random.seed(seed)
        for x in range(self.X_max):
            for y in range(self.Y_max):
                distance_to_center = ((x - self.center_x) ** 2 + (y - self.center_y) ** 2) ** 0.5  # Euclidean forumla
                normalized_distance = distance_to_center / self.max_distance  # Output 0 kuni 1
                land_probability = 1 - (normalized_distance ** 213)  # Suurendab (1) v6imalust tekkida mapi keskele.
                if random.random() < land_probability:  # random.random output = [0, 1]
                    self.terrain_data[x][y] = 1

        for i in range(len(self.terrain_data)):
            for j in range(len(self.terrain_data[i])):
                if self.terrain_data[i][j] == 1 and random.random() < 0.03:
                    self.terrain_data[i][j] = 2

    def update_player(self):
        keys = pygame.key.get_pressed()
        new_player_x = self.player_x
        new_player_y = self.player_y

        if keys[pygame.K_a]:
            new_player_x = self.player_x - self.player.speed
        if keys[pygame.K_d]:
            new_player_x = self.player_x + self.player.speed
        if keys[pygame.K_w]:
            new_player_y = self.player_y - self.player.speed
        if keys[pygame.K_s]:
            new_player_y = self.player_y + self.player.speed

        # Update player's position and stamina
        self.player_x = new_player_x
        self.player_y = new_player_y
        self.player.speed = 4

        # Kui hoitakse all Shifti ja a, d, w, s:
        # Muudetakse playeri speedi ja võetakse staminat.
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
                self.stamina_bar_decay = 0
                self.player.speed = 20
                self.player.stamina.use_stamina(0.05)

            # Kui stamina on 0 siis playeri speed läheb sama
            # kiireks kui enne shifti vajutamist oli.
            if self.player.stamina.current_stamina == 0:
                self.player.speed = self.base_speed
            else:
                self.player.stamina.stamina_regenerate(0.025)

        # Kui ei hoia shifti all siis regeneb staminat
        if not keys[pygame.K_LSHIFT] and not keys[pygame.K_RSHIFT]:
            self.player.stamina.stamina_regenerate(0.025)
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

    # värvib ära teatud ruudud || 2 = rock, 1 = terrain (muru), 0 = water
    def render(self):
        self.screen.fill('blue')  # Teeb ülejäänud ala siniseks

        for i in range(len(self.terrain_data)):
            for j in range(len(self.terrain_data[i])):
                if self.terrain_data[i][j] == 1:
                    cell_color = 'green'
                if self.terrain_data[i][j] == 2:
                    cell_color = 'gray'
                elif self.terrain_data[i][j] == 0:
                    cell_color = 'blue'

                terrain_rect = pygame.Rect(
                    j * self.block_size + self.offset_x,
                    i * self.block_size + self.offset_y,
                    self.block_size,
                    self.block_size
                )

                pygame.draw.rect(self.screen, cell_color, terrain_rect)

        player_rect_adjusted = pygame.Rect(
            self.player_rect.left + self.offset_x,
            self.player_rect.top + self.offset_y,
            self.block_size,
            self.block_size,
        )

        if self.stamina_bar_decay < 50:
            pygame.draw.rect(self.screen, '#F7F7F6', self.stamina_rect_bg, 0, 7)
            pygame.draw.rect(self.screen, 'black', self.stamina_rect_border, 2, 7)
            pygame.draw.rect(self.screen, '#4169E1', self.stamina_rect, 0, 7)

        pygame.draw.rect(self.screen, self.player_color, player_rect_adjusted)

        pygame.display.flip()
        self.set_frame_rate.tick(60)

    def run(self):
        while True:
            self.handle_events()  # Paneb mängu õigesti kinni
            self.update_player()
            self.check_collisions()  # Vaatab mängija ja maastiku kokkupõrkeid
            self.box_target_camera()
            self.stamina_bar_update()
            self.render()  # värvib ära teatud ruudud || 2 = rock, 1 = terrain (muru), 0 = water
            # print(self.player_x,
            #       self.player_y)


if __name__ == "__main__":
    game = Game()
    game.run()
