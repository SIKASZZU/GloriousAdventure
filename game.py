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
            health_regeneration_rate=0.5, stamina_regeneration_rate=0.5, stamina_degeneration_rate=0.05,
            base_speed=0.5, max_speed=10, min_speed=0.5
        )

        # Game-related attributes
        self.block_size = 25
        # self.hit_box_width =
        # self.hit_box_height =
        self.player_color = 'red'
        self.REGENERATION_DELAY = 2
        self.stamina_regeneration_timer = 0

        self.X_max = 1000 // self.block_size
        self.Y_max = 750 // self.block_size
        self.center_x = self.X_max // 2
        self.center_y = self.Y_max // 2
        self.max_distance = min(self.center_x, self.center_y)

        self.terrain_data = [[0 for _ in range(self.Y_max)] for _ in range(self.X_max)]
        self.new_island(69)

        self.player_x = random.randint(0, 1000)
        self.player_y = random.randint(0, 750)

    def new_island(self, seed):
        # Koostab islandi

        # Mapile tekib seed nagu Minecraftis vms
        random.seed(seed)
        for x in range(self.X_max):
            for y in range(self.Y_max):
                distance_to_center = ((x - self.center_x) ** 2 + (y - self.center_y) ** 2) ** 0.5  # Euclidean forumla
                normalized_distance = distance_to_center / self.max_distance  # Output 0 kuni 1
                land_probability = 1 - (normalized_distance ** 4)  # Suurendasin terraini (1) v6imalust tekkida mapi keskele.
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

        if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
            self.player.stamina.use_stamina(0.05)
            self.stamina_regeneration_timer = 0
        else:
            self.stamina_regeneration_timer += 1

            if self.stamina_regeneration_timer >= self.REGENERATION_DELAY:
                elapsed_time = 1.0 / 60.0  # Assuming 60 FPS
                self.player.stamina.stamina_regenerate(elapsed_time)
                self.stamina_regeneration_timer = 0

        if self.player.stamina.current_stamina == 0:
            self.player.speed = 1  # Set the speed directly
            print(self.player.speed)
        else:
            self.player.speed = 4

        print(self.player.stamina.current_stamina)


        # Update the player's rectangle
        self.player_rect = pygame.Rect(self.player_x, self.player_y, self.block_size, self.block_size)

    def check_collisions(self):
        for i in range(len(self.terrain_data)):
            for j in range(len(self.terrain_data[i])):
                terrain_rect = pygame.Rect(
                    j * self.block_size, i * self.block_size,
                    self.block_size, self.block_size
                )

                if self.player_rect.colliderect(terrain_rect):
                    in_water = any(
                        self.terrain_data[row][col] == 0
                        for row in range(i, i - 1, -1)
                        for col in range(j, j - 1, -1)
                    )

                    if in_water:
                        self.player.speed = 1

    # värvib ära teatud ruudud || 2 = rock, 1 = terrain (muru), 0 = water
    def render(self, offset_x, offset_y):
        self.screen.fill('white')  # Clear the screen with a black color

        for i in range(len(self.terrain_data)):
            for j in range(len(self.terrain_data[i])):
                if self.terrain_data[i][j] == 1:
                    cell_color = 'green'
                if self.terrain_data[i][j] == 2:
                    cell_color = 'gray'
                elif self.terrain_data[i][j] == 0:
                    cell_color = 'blue'

                terrain_rect = pygame.Rect(
                    j * self.block_size + offset_x,
                    i * self.block_size + offset_y,
                    self.block_size, 
                    self.block_size
                )

                pygame.draw.rect(self.screen, cell_color, terrain_rect)

        pygame.draw.rect(self.screen, self.player_color, self.player_rect)  # Draw the player rectangle
        pygame.display.flip()

        self.set_frame_rate.tick(60)

    def run(self):
        while True:
            self.handle_events()  # Paneb mängu õigesti kinni
            self.update_player()
            self.check_collisions()  # Vaatab mängija ja maastiku kokkupõrkeid
            self.render(50,50)  # värvib ära teatud ruudud || 2 = rock, 1 = terrain (muru), 0 = water
            # print(self.player_x,
            #       self.player_y)
if __name__ == "__main__":
    game = Game()
    game.run()