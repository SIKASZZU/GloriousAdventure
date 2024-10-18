import pygame

from variables import UniversalVariables, GameConfig
from camera import Camera
from entity import Enemy
from audio import Player_audio

class Attack:
    def detect_item(self):
        click = Camera.click_on_screen(self)  # x, y (Coords)

        if not click:
            return

        for enemy_name, enemy_info in list(Enemy.spawned_enemy_dict.items()):
            enemy_rect = pygame.Rect(enemy_info[1] * UniversalVariables.block_size,
                                     enemy_info[2] * UniversalVariables.block_size, 73, 73)

            if not enemy_rect.collidepoint(click):
                continue

            print(f"Clicked at {enemy_name}")

        # for object_info in list(UniversalVariables.object_list):
        #     object_rect = pygame.Rect(object_info[1], object_info[0], object_info[1] + object_info[2], object_info[0] + object_info[3])
        #     object_id = object_info[5]
        #
        #     if not object_rect.collidepoint(click):
        #         continue
        #
        #     print(f"Clicked at {object_id}")


class AttackEnemy:
    def find_enemy(self):
        click = Camera.click_on_screen(self)  # x, y (Coords)

        if not click:
            return

        for enemy_name, enemy_info in list(Enemy.spawned_enemy_dict.items()):
            enemy_rect = pygame.Rect(enemy_info[1] * UniversalVariables.block_size,
                                     enemy_info[2] * UniversalVariables.block_size, 73, 73)

            if not enemy_rect.collidepoint(click):
                continue

            return enemy_name, enemy_info

    def damage_enemy(self, enemy_name, enemy_info):
        enemy_image, y, x, HP = enemy_info
        new_HP = HP - UniversalVariables.player_damage

        if new_HP <= 0:
            del Enemy.path[enemy_name]
            del Enemy.spawned_enemy_dict[enemy_name]
            print(f"Killed {enemy_name}.")
            Player_audio.ghost_died_audio(self)

            return

        Enemy.spawned_enemy_dict[enemy_name] = enemy_image, y, x, new_HP
        Player_audio.ghost_hurt_audio(self)

    def update(self):
        enemy_data = AttackEnemy.find_enemy(self)
        if enemy_data:
            enemy_name, enemy_info = enemy_data

            print(f"Attacking: {enemy_name}. HP dropped from {enemy_info[-1]} to {enemy_info[-1] - UniversalVariables.player_damage}.")

            AttackEnemy.damage_enemy(self, enemy_name, enemy_info)

            print("attack.py -> AttackEnemy -> update() -> if enemy_data")
            print()


class AttackObject:
    def __init__(self):
        super().__init__(Attack)
        ...
        # Kui objectit pole >5 sekki hititud siis reset hp.
