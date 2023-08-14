import pygame
import sys
import random
import time

pygame.init()
screen = pygame.display.set_mode((1000, 750))
pygame.display.set_caption("GA")  # Window nimi
set_framerate = pygame.time.Clock()  # framerate


###

# playeri suurused
player_x = 50
player_y = 50

# Minimaalse ruudu summa arvutamine
Ymax = 1000 // player_y
Xmax = 750 // player_x

terrain_data = [[0 for _ in range(Ymax)] for _ in range(Xmax)]  # Ehitab 2D matrixi 0idest.

# terrain_data = []  # see kood on praeguse terrain_data lihtsamini kirjutatult.
#for _ in range(Xmin):
#    row = []
#    for _ in range(Ymin):
#        row.append(0)
#    terrain_data.append(row)


# mapi keskosa arvutamine
center_x = Xmax // 2
center_y = Ymax // 2

max_distance = min(center_x, center_y)

# Koostab islandi
for x in range(Xmax):
    for y in range(Ymax):
        distance_to_center = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5  # Euclidean forumla
        normalized_distance = distance_to_center / max_distance  # Output 0 kuni 1
        land_probability = 1 - (normalized_distance ** 2)  # Suurendasin terraini (1) v6imalust tekkida mapi keskele.
        if random.random() < land_probability:  # random.random output = [0, 1]
            terrain_data[x][y] = 1

###

# GAME LOOP
while True:

    # Checkib kas user quitib v6i ei
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  # Kui seda ei oleks, runniks kood edasi, kuid pygame windowi enam ei ole. Tekib error.

    # Liikumine
    keys = pygame.key.get_pressed()

    class Player():
        def __init__(self, speed):
            self.speed = speed

    # Kalkuleerib gridilt kus mängija seisab
    player_col = player_x // 50
    player_row = player_y // 50

    # Mis blocki peal seisab
    try:
        player_terrain_value = terrain_data[player_row][player_col]
        if player_terrain_value == 0:  # Standing on water (0)
            user = Player(speed=1)
        if player_terrain_value == 1:  # Standing on terrain (1)
            user = Player(speed=4)
    except IndexError:  # tra seda try, excepti pole vaja aga just l2ks vaja niiet idk
        print("Indexerror - Out of range: player_terrain_value = terrain_data[player_row][player_col]")

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
    if player_x <= -50: player_x += 50

    if player_x >= 1000: player_x -= 50

    if player_y <= -50: player_y += 50

    if player_y >= 750: player_y -= 50 
    
    screen.fill('gray')  # K6ige alumine layer

    # v2rvib 2ra teatud ruudud || 1 = roheline, 0 = sinine
    for i in range(len(terrain_data)):
        for j in range(len(terrain_data[i])):
            cell_color = 'green' if terrain_data[i][j] == 1 else 'blue'
            pygame.draw.rect(screen, cell_color, (j * 50, i * 50, 50, 50))

    player_rect = pygame.Rect(player_x, player_y, 50, 50)  # Playeri koordinaadid visuaalseks v2ljatoomiseks
    pygame.draw.rect(screen, 'YELLOW', player_rect)  # Visuaalselt playeri v2ljatoomine

    # Et mängija saaks mapist (mapist mitte ekraanist) välja mina - Et mäng ei crashiks
    if player_col < 0:
        player_col = Ymax - 1
    elif player_col >= Ymax:
        player_col = 0

    if player_row < 0:
        player_row = Xmax - 1
    elif player_row >= Xmax:
        player_row = 0

    set_framerate.tick(60)  # fps limit
    pygame.display.update()

    # print statementid
    print(f"Grid coordinates: {player_col, player_row}")
    print(f"Location coordinates: {new_player_x, new_player_y}")
    print(f"Columns: {Ymax}, Rows: {Xmax}")
    print(f"Player speed: {user.speed}")
    print('\n') # new line et terminalist oleks lihtsam lugeda

 