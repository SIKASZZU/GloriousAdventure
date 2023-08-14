import pygame
import sys
import random
import time

pygame.init()
screen = pygame.display.set_mode((1000, 750))
pygame.display.set_caption("GA")  # Window nimi
set_framerate = pygame.time.Clock()  # framerate

# playeri suurused
player_x = 50
player_y = 50

# Minimaalse ruudu summa arvutamine
Ymin = 1024 // player_y
Xmin = 786 // player_x

# randomized mapi tegemine
terrain_data = [[random.choice([0, 1]) for _ in range(Ymin)] for _ in range(Xmin)]  # random terrain

while True:

    # Checkib kas user quitib v6i ei
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  # Kui seda ei oleks, runniks kood edasi, kuid pygame windowi enam ei ole. Tekib error.

    # Liikumine
    keys = pygame.key.get_pressed()

    new_player_x = player_x
    new_player_y = player_y

    if keys[pygame.K_a]:  # is True, left
        new_player_x = player_x - 10
        
    if keys[pygame.K_d]:  # right
        new_player_x = player_x + 10

    if keys[pygame.K_w]:  # up
        new_player_y = player_y - 10
        
    if keys[pygame.K_s]:  # down
        new_player_y = player_y + 10
    
    player_x = new_player_x
    player_y = new_player_y 

    # Nurgad
    if player_x <= -50: player_x += 50

    if player_x >= 1024: player_x -= 50

    if player_y <= -50: player_y += 50

    if player_y >= 786: player_y -= 50 
    

    screen.fill('gray')  # K6ige alumine layer

    # v2rvib 2ra teatud ruudud || 1 = roheline, 0 = sinine
    for i in range(len(terrain_data)):
        for j in range(len(terrain_data[i])):
            cell_color = 'green' if terrain_data[i][j] == 1 else 'blue'
            pygame.draw.rect(screen, cell_color, (j * 50, i * 50, 50, 50))

    player_rect = pygame.Rect(player_x, player_y, 50, 50)  # Playeri koordinaadid visuaalseks v2ljatoomiseks
    pygame.draw.rect(screen, 'YELLOW', player_rect)  # Visuaalselt playeri v2ljatoomine

    # Kalkuleerib gridilt kus mängija seisab
    player_col = player_x // 50
    player_row = player_y // 50

    # Et mängija saaks mapist (mapist mitte ekraanist) välja mina - Et mäng ei crashiks
    if player_col < 0:
        player_col = Ymin - 1
    elif player_col >= Ymin:
        player_col = 0

    if player_row < 0:
        player_row = Xmin - 1
    elif player_row >= Xmin:
        player_row = 0

    # Mis blocki peal seisab
    player_terrain_value = terrain_data[player_row][player_col]
    if player_terrain_value == 0: print("Currently standing on: water, (0)")
    if player_terrain_value == 1: print("Currently standing on: terrain, (1)")

    set_framerate.tick(60)  # fps limit
    pygame.display.update()

    # print statementid
    #time.sleep(1)
    print(f"player_col: {player_col}, player_row: {player_row}")
    print(f"LOCATION X: {new_player_x}, LOCATION Y: {new_player_y}")
    print(f"cols: {Ymin}, rows: {Xmin}")
    print('\n') # new line et terminalist oleks lihtsam lugeda
 