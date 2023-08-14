import pygame
import sys
import random
import time

pygame.init()
screen = pygame.display.set_mode((1000, 750))
pygame.display.set_caption("GA")  # Window nimi
set_framerate = pygame.time.Clock()  # framerate

##################
##################

# Mängija suurus
player_size = 25


# Hitboxi suurus
hitbox_width = player_size
hitbox_height = player_size

player_color = "yellow"  # Default värv

##################
##################

# Minimaalse ruudu summa arvutamine
Ymax = 1000 // player_size
Xmax = 750 // player_size

terrain_data = [
    [0 for _ in range(Ymax)] for _ in range(Xmax)
]  # Ehitab 2D matrixi 0idest.

# mapi keskosa arvutamine
center_x = Xmax // 2
center_y = Ymax // 2

max_distance = min(center_x, center_y)

# Koostab islandi
for x in range(Xmax):
    for y in range(Ymax):
        distance_to_center = (
            (x - center_x) ** 2 + (y - center_y) ** 2
        ) ** 0.5  # Euclidean forumla
        normalized_distance = distance_to_center / max_distance  # Output 0 kuni 1
        land_probability = 1 - (
            normalized_distance**4
        )  # Suurendasin terraini (1) v6imalust tekkida mapi keskele.
        if random.random() < land_probability:  # random.random output = [0, 1]
            terrain_data[x][y] = 1

for i in range(len(terrain_data)):
    for j in range(len(terrain_data[i])):
        if terrain_data[i][j] == 1 and random.random() < 0.03:
            terrain_data[i][j] = 2

# Spawnib suvalisse kohta
player_x = random.randint(0, 1000)
player_y = random.randint(0, 750)


class Player:
    def __init__(self, health, stamina, speed):
        self.health = health
        self.stamina = stamina
        self.speed = speed


user = Player(health=10, stamina=10, speed=4)

# GAME LOOP
while True:
    # Checkib kas user quitib v6i ei
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  # Kui seda ei oleks, runniks kood edasi, kuid pygame windowi enam ei ole. Tekib error.

    # Liikumine
    keys = pygame.key.get_pressed()

    # Kalkuleerib gridilt kus mängija seisab
    player_col = player_x // 50
    player_row = player_y // 50

    new_player_x = player_x
    new_player_y = player_y

    if keys[pygame.K_a]:  # is True, left
        new_player_x = player_x - user.speed

    if keys[pygame.K_d]:  # right
        new_player_x = player_x + user.speed

    if keys[pygame.K_w]:  # up
        new_player_y = player_y - user.speed

    if keys[pygame.K_s]:  # down
        new_player_y = player_y + user.speed

    player_x = new_player_x
    player_y = new_player_y

    # Nurgad
    if player_x <= -player_size:
        player_x += player_size
    if player_x >= 1000:
        player_x -= player_size
    if player_y <= -player_size:
        player_y += player_size
    if player_y >= 750:
        player_y -= player_size

    screen.fill('white')  # K6ige alumine layer

    player_rect = pygame.Rect(
        new_player_x, new_player_y, hitbox_width, hitbox_height
    )  # Playeri koordinaadid visuaalseks v2ljatoomiseks

    # v2rvib 2ra teatud ruudud || 2 = rock, 1 = terrain (muru), 0 = water
    for i in range(len(terrain_data)):
        for j in range(len(terrain_data[i])):
            if terrain_data[i][j] == 1:
                cell_color = 'green'
            if terrain_data[i][j] == 2:
                cell_color = 'gray'
            elif terrain_data[i][j] == 0:
                cell_color = 'blue'
            # cell_color = 'green' if terrain_data[i][j] == 1 else 'blue'
            terrain_rect = pygame.draw.rect(screen, cell_color, (j * player_size, i * player_size, player_size, player_size))

            pygame.draw.rect(screen, cell_color, terrain_rect)

            # Check for collision with terrain cell
            if player_rect.colliderect(terrain_rect):
                print(
                    f"Collision with {terrain_data[i][j]} at grid coordinates: ({j}, {i})"
                )

                in_water = False

                if terrain_data[i][j] == 0:
                    in_water = True

                elif terrain_data[i - 1][j] == 0:
                    in_water = True

                elif terrain_data[i][j - 1] == 0:
                    in_water = True

                elif terrain_data[i - 1][j - 1] == 0:
                    in_water = True

                else:
                    player_color = "yellow"
                    user.speed = 4
                    in_water = False

                if in_water == True:
                    player_color = "red"
                    user.speed = 1

    # Hitboxi suuruse muutmiseks
    player_col = (player_x + hitbox_width // 2) // player_size
    player_row = (player_y + hitbox_height // 2) // player_size

    pygame.draw.rect(screen, player_color, player_rect)

    set_framerate.tick(60)
    pygame.display.flip()  # Update the entire display

    # print statementidd
    print(f"Grid coordinates: {player_col, player_row}")
    print(f"Location coordinates: {new_player_x, new_player_y}")
    print(f"Columns: {Ymax}, Rows: {Xmax}")
    print(f"Player speed: {user.speed}")
    print("\n")  # new line et terminalist oleks lihtsam lugeda
