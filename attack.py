import pygame

from variables import UniversalVariables
from camera import Camera
from entity import Entity
from audio import Player_audio
from items import search_item_from_items, ObjectItem, find_item_by_id
from objects import ObjectManagement
import random


class Attack:
    def __init__(self):
        self.last_attack_cooldown_max = 100
        self.last_attack_cooldown = self.last_attack_cooldown_max

    def update(self):

        ### FIXME: Miks on cooldown kui ta ei attacki mitte midagi naq?? peale igat clicki tleb cooldown nahuii????????
        AttackObject.update_timers(self)
        AttackObject.draw_hover_rect(self)

        entity_pressed = UniversalVariables.attack_key_pressed

        if self.attack.last_attack_cooldown < self.attack.last_attack_cooldown_max:
            self.attack.last_attack_cooldown += 1
            entity_pressed = UniversalVariables.attack_key_pressed = (
            False, (False, False, False, False))  # reseti uuesti, sest muidu atk 2x

            Attack.display_attack_cd_timer(self)


        elif entity_pressed[0] == True:  # arrow keydega hittisid entityt
            AttackEntity.update(self, pressed=True)
            entity_pressed = UniversalVariables.attack_key_pressed = (False, (False, False, False, False))

        else:
            entity_click = Camera.left_click_on_screen(self)  # x, y (Coords)
            object_click = self.click_position  # x, y (Coords)

            if not entity_click and not object_click:
                return False

            if entity_click and None not in entity_click:  # Check if entity_click is valid
                AttackEntity.update(self, click=entity_click)

            if object_click and None not in object_click:  # Check if object_click is valid
                AttackObject.update(self, object_click)  # Offseti asi on perses kuna muutsime camerat

        Camera.reset_clicks(self)

    def display_attack_cd_timer(self):
        left = self.player_rect[0] - 25
        top = self.player_rect[1] - 50

        cooldown_rect = pygame.Rect(left, top, 50 + self.player_rect[2], 30)
        progress_to_width = (self.attack.last_attack_cooldown / self.attack.last_attack_cooldown_max) * (
                    self.player_rect[2] + 50)
        filler_rect = pygame.Rect(left, top, progress_to_width, 30)

        pygame.draw.rect(UniversalVariables.screen, (255, 255, 255), cooldown_rect, 2, 5)
        pygame.draw.rect(UniversalVariables.screen, (255, 255, 255), filler_rect)


class AttackEntity:
    def find_entity(self, click=False, pressed=False):
        for entity_name, entity_info in list(Entity.spawned_entity_dict.items()):
            entity_rect = pygame.Rect(entity_info[1] * UniversalVariables.block_size,
                                      entity_info[2] * UniversalVariables.block_size, 73, 73)

            if click:
                if not entity_rect.collidepoint(click):
                    continue

                return entity_name, entity_info

            if pressed:
                # converted to window size coord
                entity_rect_converted: pygame.Rect = pygame.Rect(
                    entity_rect[0] + UniversalVariables.offset_x, entity_rect[1] + UniversalVariables.offset_y,
                    entity_rect[2], entity_rect[3]
                )

                if self.player_attack_rect != None and self.player_attack_rect.colliderect(entity_rect_converted):
                    return entity_name, entity_info
                else:
                    continue

    def calculate_entity_knockback(self, x, y):
        player_grid_y = UniversalVariables.player_y // UniversalVariables.block_size
        player_grid_x = UniversalVariables.player_x // UniversalVariables.block_size
        xdx, ydx = int(x), int(y)
        knockback_stenght = 2
        attack_key_tuple = UniversalVariables.attack_key_pressed[1]

        direction_of_attack = None
        if attack_key_tuple[1]:
            direction_of_attack = 'down'
            print("Attack-calc knockback-if attack tuple perses -> direction_of_attack, vb")

        elif attack_key_tuple[2]:
            direction_of_attack = 'left'

        elif attack_key_tuple[3]:
            direction_of_attack = 'right'
        else:
            direction_of_attack = 'above'

        if direction_of_attack == 'left' or direction_of_attack == 'right':

            # if entity is to the left
            if xdx < player_grid_x:
                xdx -= knockback_stenght

            # if entity is to the right
            elif xdx > player_grid_x:
                xdx += knockback_stenght

        else:  # dir of attack > above and down

            # if entity is on top
            if ydx < player_grid_y:
                ydx -= knockback_stenght

            # if entity is below
            elif ydx > player_grid_y:
                ydx += knockback_stenght

        return xdx, ydx

    def damage_entity(self, entity_name, entity_info):
        entity_image, x, y, HP = entity_info
        new_HP = HP - UniversalVariables.player_damage

        if new_HP <= 0:

            # add entity to dead entity list
            Entity.dead_entity_list[entity_name] = (x, y, False)
            have_geiger = 'Geiger' in self.inv.inventory
            if random.random() < 0.05 or have_geiger == False:  # 5% chance
                Entity.dead_entity_list[entity_name] = (x, y, True)

            del Entity.path[entity_name]
            del Entity.spawned_entity_dict[entity_name]
            Player_audio.ghost_died_audio(self)

            if UniversalVariables.debug_mode:
                print(f"Killed {entity_name}.")
                return

            return

        # # Add knockback to entity
        x, y = AttackEntity.calculate_entity_knockback(self, x, y)
        Entity.spawned_entity_dict[entity_name] = entity_image, x, y, new_HP
        Player_audio.ghost_hurt_audio(self)

        if UniversalVariables.debug_mode:
            print(
                f"Attacking: {entity_name}. HP dropped from {entity_info[-1]} to {entity_info[-1] - UniversalVariables.player_damage}.")
            return
        return

    def update(self, click=False, pressed=False):

        if click:
            entity_data = AttackEntity.find_entity(self, click=click)
            if entity_data:
                entity_name, entity_info = entity_data
                AttackEntity.damage_entity(self, entity_name, entity_info)
                self.attack.last_attack_cooldown = 0

        if pressed:
            entity_data = AttackEntity.find_entity(self, pressed=pressed)
            if entity_data:
                entity_name, entity_info = entity_data
                AttackEntity.damage_entity(self, entity_name, entity_info)
                self.attack.last_attack_cooldown = 0


class AttackObject:
    def __init__(self, terrain_data):
        self.terrain_data = terrain_data

        self.default_color = 255, 120, 20, 150
        self.click_color = 255, 0, 0, 255

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
                UniversalVariables.object_hp_dict[rect_key] = {'hp': hp, 'id': object_id,
                                                               'timer': UniversalVariables.object_reset_timer}

            # Resetib timerit iga kord, kui objectit attackid
            else:
                UniversalVariables.object_hp_dict[rect_key]['timer'] = UniversalVariables.object_reset_timer

            AttackObject.deal_damage(self, rect_key, object_rect)

            return True

    def deal_damage(self, rect_key: tuple[float, float, int, int],
                    object_rect: tuple[float, float, float, float]) -> None:
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
            was_removed = ObjectManagement.remove_object_at_position(self, y_minus_offset, x_minus_offset,
                                                                     object_data['id'])
            if was_removed:
                del UniversalVariables.object_hp_dict[rect_key]

            # Kui inv oli täis ja itemit ülesse ei saanud võtta siis jätab objecti 'HP'ks 1
            else:
                new_hp = 1
                object_data['hp'] = new_hp

        transparent_surface = pygame.Surface((UniversalVariables.screen_x, UniversalVariables.screen_y),
                                             pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, self.attack_object.click_color, object_rect, 3)

        UniversalVariables.screen.blit(transparent_surface, (0, 0))

        UniversalVariables.interaction_delay = 0

    def update_timers(self) -> None:
        for rect_key in list(UniversalVariables.object_hp_dict.keys()):
            object_data = UniversalVariables.object_hp_dict[rect_key]
            object_data['timer'] -= 1

            if object_data['timer'] <= 0:
                del UniversalVariables.object_hp_dict[rect_key]

    def draw_hover_rect(self) -> None:
        mouse_pos = pygame.mouse.get_pos()

        transparent_surface = pygame.Surface((UniversalVariables.screen_x, UniversalVariables.screen_y),
                                             pygame.SRCALPHA)

        for object_info in list(UniversalVariables.object_list):
            object_id: int = object_info[5]
            is_valid_object: bool = search_item_from_items(type=ObjectItem, item_name_or_id=object_id,
                                                           target_attribute="Breakable")

            if not is_valid_object:
                continue

            x, y, width, height = object_info[:4]
            object_rect = pygame.Rect(x, y, width, height)

            if object_rect.collidepoint(mouse_pos):
                pygame.draw.rect(transparent_surface, self.attack_object.default_color, object_rect, 2)

                UniversalVariables.screen.blit(transparent_surface, (0, 0))
                return

        return

    def update(self, click: tuple[int, int]) -> None:
        if UniversalVariables.interaction_delay >= UniversalVariables.interaction_delay_max:
            AttackObject.find_object(self, click)
