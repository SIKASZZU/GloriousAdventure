import pygame

from variables import UniversalVariables, GameConfig
from camera import Camera
from entity import Enemy
from audio import Player_audio
from items import search_item_from_items, ObjectItem, find_item_by_id
from objects import ObjectManagement


class Attack:
    last_attack_cooldown_max = 100
    last_attack_cooldown = last_attack_cooldown_max

    def update(self):
        AttackObject.update_timers(self)


        enemy_pressed = UniversalVariables.attack_key_pressed

        if Attack.last_attack_cooldown < Attack.last_attack_cooldown_max:
            Attack.last_attack_cooldown += 2
            enemy_pressed = UniversalVariables.attack_key_pressed = False  # panen siia ka muidu mingi double attack jamps, kui liiga kaua peal hoiad

        elif self.click_position:
            enemy_click = Camera.click_on_screen(self)  # x, y (Coords)
            object_click = self.click_position[0], self.click_position[1]  # x, y (Coords)

            if not enemy_click and not object_click:
                return

            if enemy_click:  # klikkisid hiirega enemy peale.
                AttackEnemy.update(self, click=enemy_click)
                Attack.last_attack_cooldown = 0

            if object_click:
                AttackObject.update(self, object_click)

        elif enemy_pressed:  # arrow keydega hittisid enemyt
            AttackEnemy.update(self, pressed=True)
            enemy_pressed = UniversalVariables.attack_key_pressed = False
            Attack.last_attack_cooldown = 0

        Camera.reset_clicks(self)


class AttackEnemy:
    def find_enemy(self, click=False, pressed=False):
        for enemy_name, enemy_info in list(Enemy.spawned_enemy_dict.items()):
            enemy_rect = pygame.Rect(enemy_info[1] * UniversalVariables.block_size,
                                     enemy_info[2] * UniversalVariables.block_size, 73, 73)
            
            if click:
                if not enemy_rect.collidepoint(click):
                    continue

                return enemy_name, enemy_info

            if pressed:
                # converted to window size coord
                enemy_rect_converted: pygame.Rect = pygame.Rect(
                    enemy_rect[0] + UniversalVariables.offset_x, enemy_rect[1] + UniversalVariables.offset_y,
                    enemy_rect[2], enemy_rect[3]
                )

                if self.player_attack_rect != None and self.player_attack_rect.colliderect(enemy_rect_converted):
                    return enemy_name, enemy_info
                else:
                    continue

    def calculate_enemy_knockback(self, y,x):
        player_grid_y = UniversalVariables.player_y // UniversalVariables.block_size
        player_grid_x = UniversalVariables.player_x // UniversalVariables.block_size
        xdx, ydx = x, y
        knockback_stenght = 0.55

        # if enemy is to the left
        if x < player_grid_x:
            xdx -= knockback_stenght
        # if enemy is on top
        if y < player_grid_y:
            ydx -= knockback_stenght
        # if enemy is to the right
        if x > player_grid_x:
            xdx += knockback_stenght
        # if enemy is below
        if y > player_grid_y:
            ydx += knockback_stenght

        return ydx, xdx

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

        # # Add knockback to enemy
        y, x = AttackEnemy.calculate_enemy_knockback(self, y,x)
        Enemy.spawned_enemy_dict[enemy_name] = enemy_image, y, x, new_HP
        Player_audio.ghost_hurt_audio(self)

        if UniversalVariables.debug_mode:
            print(
                f"Attacking: {enemy_name}. HP dropped from {enemy_info[-1]} to {enemy_info[-1] - UniversalVariables.player_damage}.")
            return
        return

    def update(self, click=False, pressed=False):

        if click:
            enemy_data = AttackEnemy.find_enemy(self, click=click)
            if enemy_data:
                enemy_name, enemy_info = enemy_data
                _, y, x, _ = enemy_info
                # AttackEnemy.saved_enemy_x, AttackEnemy.saved_enemy_y = y
                AttackEnemy.damage_enemy(self, enemy_name, enemy_info)
        if pressed:
            enemy_data = AttackEnemy.find_enemy(self, pressed=pressed)
            if enemy_data:
                enemy_name, enemy_info = enemy_data
                AttackEnemy.damage_enemy(self, enemy_name, enemy_info)


class AttackObject:

    def find_object(self, click: tuple[int, int]) -> bool:
        for object_info in list(UniversalVariables.object_list):
            object_id: int = object_info[5]
            is_valid_object: bool = search_item_from_items(type=ObjectItem, item_name_or_id=object_id,
                                                     target_attribute="Breakable")

            if not is_valid_object:
                continue

            x, y, width, height = object_info[:4]
            object_rect = pygame.Rect(x, y, width, height)

            if not object_rect.collidepoint(click):
                continue

            # Ei saa listi salvestada vale offsetiga, võtab praegu ära ja liidab hiljem juurde
            x_minus_offset: float = y - UniversalVariables.offset_y
            y_minus_offset: float = x - UniversalVariables.offset_x

            rect_key: tuple = x_minus_offset, y_minus_offset, width, height

            item: dict[str, any] = find_item_by_id(object_id)
            if rect_key not in UniversalVariables.object_hp_dict:
                hp: float = item['hp'] if isinstance(item, dict) else item.hp if item and hasattr(item, 'hp') else 3
                UniversalVariables.object_hp_dict[rect_key] = {'hp': hp, 'id': object_id, 'timer': UniversalVariables.object_reset_timer}

            # Resetib timerit iga kord, kui objectit attackid
            else:
                UniversalVariables.object_hp_dict[rect_key]['timer'] = UniversalVariables.object_reset_timer

            AttackObject.deal_damage(self, rect_key)

            if UniversalVariables.debug_mode:
                item_name = item.name if item and hasattr(item, 'name') else 'Unknown'
                return True

            return True

    def deal_damage(self, rect_key: tuple[float, float, int, int]) -> None:
        object_data: dict[str, any] = UniversalVariables.object_hp_dict.get(rect_key)

        if not object_data:
            return

        current_hp: float = object_data['hp']
        new_hp: float = current_hp - UniversalVariables.player_damage

        if new_hp < 0:
            new_hp = 0

        object_data['hp'] = new_hp

        x_minus_offset, y_minus_offset, _, _ = rect_key

        if new_hp <= 0:
            # X ja Y peavad olema vastupidi --> grid asi
            was_removed = ObjectManagement.remove_object_at_position(self, y_minus_offset, x_minus_offset, object_data['id'])
            if was_removed:
                del UniversalVariables.object_hp_dict[rect_key]

            # Kui inv oli täis ja itemit ülesse ei saanud võtta siis jätab objecti 'HP'ks 1
            else:
                new_hp = 1
                object_data['hp'] = new_hp

        print('New HP:', new_hp)

    def update_timers(self) -> None:
        for rect_key in list(UniversalVariables.object_hp_dict.keys()):
            object_data = UniversalVariables.object_hp_dict[rect_key]
            object_data['timer'] -= 1

            if object_data['timer'] <= 0:
                del UniversalVariables.object_hp_dict[rect_key]

    def update(self, click: tuple[int, int]) -> None:
        valid: bool = AttackObject.find_object(self, click)
        if valid:
            ...

