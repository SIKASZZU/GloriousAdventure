import pygame

from variables import UniversalVariables, GameConfig
from camera import Camera
from entity import Enemy
from audio import Player_audio
from items import search_item_from_items, ObjectItem, find_item_by_id

class Attack:
    def update(self):

        if not self.click_position:
            return

        enemy_click = Camera.click_on_screen(self)  # x, y (Coords)
        object_click = self.click_position[0], self.click_position[1]  # x, y (Coords)

        if not enemy_click and not object_click:
            return

        if enemy_click:
            AttackEnemy.update(self, enemy_click)

        if object_click:
            AttackObject.update(self, object_click)


class AttackEnemy:
    def find_enemy(self, click):
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
            Player_audio.ghost_died_audio(self)

            if UniversalVariables.debug_mode:
                print(f"Killed {enemy_name}.")
                return

            return

        Enemy.spawned_enemy_dict[enemy_name] = enemy_image, y, x, new_HP
        Player_audio.ghost_hurt_audio(self)

        if UniversalVariables.debug_mode:
            print(
                f"Attacking: {enemy_name}. HP dropped from {enemy_info[-1]} to {enemy_info[-1] - UniversalVariables.player_damage}.")
            return
        return

    def update(self, click):
        enemy_data = AttackEnemy.find_enemy(self, click)
        if enemy_data:
            enemy_name, enemy_info = enemy_data
            AttackEnemy.damage_enemy(self, enemy_name, enemy_info)

class AttackObject:
    def find_object(self, click):
        for object_info in list(UniversalVariables.object_list):

            object_id = object_info[5]
            is_valid_object = search_item_from_items(type=ObjectItem, item_name_or_id=object_id, target_attribute="Breakable")
            if not is_valid_object:
                return

            x = object_info[0]  # window x
            y = object_info[1]  # window y
            width = object_info[2]
            height = object_info[3]
            object_id = object_info[5]

            object_rect = pygame.Rect(x, y, width, height)

            if not object_rect.collidepoint(click):
                continue

            if UniversalVariables.debug_mode:
                item = find_item_by_id(object_id)
                item_name = item.name if item and hasattr(item, 'name') else 'Unknown'
                return print(f"Breaking: {item_name}"), print(), print()

            return

    def update(self, click):
        AttackObject.find_object(self, click)
