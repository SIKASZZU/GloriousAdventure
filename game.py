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

        self.X_max = 2000 // self.block_size
        self.Y_max = 1500 // self.block_size
        self.center_x = self.X_max // 2
        self.center_y = self.Y_max // 2
        self.max_distance = min(self.center_x, self.center_y)

        self.terrain_data = [[0 for _ in range(self.Y_max)] for _ in range(self.X_max)]
        self.new_island(69)

        self.player_x = random.randint(400, 600)
        self.player_y = random.randint(200, 550)

        # camera stuff
        self.camera_borders = {'left': 200, 'right': 200, 'top': 100, 'bottom': 100}
        l = self.camera_borders['left'] 
        t = self.camera_borders['top']
        w = self.screen.get_size()[0]  - (self.camera_borders['left'] + self.camera_borders['right'])  # width
        h = self.screen.get_size()[1]  - (self.camera_borders['top'] + self.camera_borders['bottom'])  # height
        print(l, t, w, h)
        self.camera_rect = pygame.Rect(l,t,w,h)
        
        ## camera offset
        self.offset_x = 0
        self.offset_y = 0

        #self.terrain_offset = pygame.math.Vector2()
        #self.half_w = self.screen.get_size()[0] // 2
        #self.half_h = self.screen.get_size()[1] // 2


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
            self.player.speed = 10  # Set the speed directly
            print(self.player.speed)
        else:
            self.player.speed = 10

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
                        self.player.speed = 10


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

        print(f"self.offset_x: {self.offset_x} = {self.camera_borders['left']} - {self.camera_rect.left}")
        print(f"self.offset_y: {self.offset_y} = {self.camera_borders['top']} - {self.camera_rect.top}")


    # värvib ära teatud ruudud || 2 = rock, 1 = terrain (muru), 0 = water
    def render(self):
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
                    j * self.block_size + self.offset_x,
                    i * self.block_size + self.offset_y,
                    self.block_size, 
                    self.block_size
                )

                pygame.draw.rect(self.screen, cell_color, terrain_rect)

        pygame.draw.rect(self.screen, self.player_color, self.player_rect)  # Draw the player rectangle
        pygame.draw.rect(self.screen, 'yellow', self.camera_rect, 5)
        pygame.display.flip()

        self.set_frame_rate.tick(60)

    def run(self):
        while True:
            self.handle_events()  # Paneb mängu õigesti kinni
            self.update_player()
            self.check_collisions()  # Vaatab mängija ja maastiku kokkupõrkeid
            self.render()  # värvib ära teatud ruudud || 2 = rock, 1 = terrain (muru), 0 = water
            self.box_target_camera()
            # print(self.player_x,
            #       self.player_y)
if __name__ == "__main__":
    game = Game()
    game.run()