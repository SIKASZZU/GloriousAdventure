import pygame

from variables import UniversalVariables
from items import search_item_from_items, ObjectItem, find_item_by_id
import random


class Attack:
    def __init__(self, camera, attack_entity, attack_object, player_update, object_management, variables):
        self.camera = camera
        self.attack_entity = attack_entity
        self.attack_object = attack_object
        self.player_update = player_update
        self.object_management = object_management
        self.variables = variables

        self.last_attack_cooldown_max = 100
        self.last_attack_cooldown = self.last_attack_cooldown_max

    def update(self):

        ### FIXME: Miks on cooldown kui ta ei attacki mitte midagi naq?? peale igat clicki tleb cooldown nahuii????????
        self.attack_object.update_timers()
        self.attack_object.draw_hover_rect()

        entity_pressed = self.variables.attack_key_pressed

        if self.last_attack_cooldown < self.last_attack_cooldown_max:
            self.last_attack_cooldown += 1
            entity_pressed = self.variables.attack_key_pressed = (
            False, (False, False, False, False))  # reseti uuesti, sest muidu atk 2x

            self.display_attack_cd_timer()

        elif entity_pressed[0]:  # arrow keydega hittisid entityt
            self.attack_entity.update(self, pressed=True)
            entity_pressed = self.variables.attack_key_pressed = (False, (False, False, False, False))

        else:
            
            entity_click = self.camera.right_click_on_screen(self.camera.click_position)  # x, y (Coords)
            object_click = self.camera.click_position  # x, y (Coords)  -> Tuleb EventHandlerist
            if not entity_click and not object_click:
                return False

            if entity_click and None not in entity_click:  # Check if entity_click is valid
                self.attack_entity.update(self, click=entity_click)

            if object_click and None not in object_click:  # Check if object_click is valid
                self.attack_object.update(object_click)  # Offseti asi on perses kuna muutsime camerat

    def display_attack_cd_timer(self):
        left = self.player_update.player_rect[0] - 25
        top = self.player_update.player_rect[1] - 50

        cooldown_rect = pygame.Rect(left, top, 50 + self.player_update.player_rect[2], 30)
        progress_to_width = (self.last_attack_cooldown / self.last_attack_cooldown_max) * (
                    self.player_update.player_rect[2] + 50)
        filler_rect = pygame.Rect(left, top, progress_to_width, 30)

        pygame.draw.rect(self.variables.screen, (255, 255, 255), cooldown_rect, 2, 5)
        pygame.draw.rect(self.variables.screen, (255, 255, 255), filler_rect)


class AttackEntity:
    def __init__(self, inv, player_update, entity):
        self.inv = inv
        self.player_update = player_update
        self.entity = entity 
        
        self.player_attack_rect = pygame.Rect

    def find_entity(self, click=None, pressed=False):
        for entity_name, entity_info in list(self.entity.spawned_entity_dict.items()):
            entity_rect = pygame.Rect(entity_info[1] * self.variables.block_size,
                                      entity_info[2] * self.variables.block_size, 73, 73)

            if click:
                if not entity_rect.collidepoint(click):
                    continue

                return entity_name, entity_info

            if pressed:
                # converted to window size coord
                entity_rect_converted: pygame.Rect = pygame.Rect(
                    entity_rect[0] + self.variables.offset_x, entity_rect[1] + self.variables.offset_y,
                    entity_rect[2], entity_rect[3]
                )
                
                if self.player_attack_rect is not None and self.player_attack_rect.colliderect(entity_rect_converted):
                    return entity_name, entity_info
                else:
                    continue

    def attack_rect(self, keys):
        """ Return and visualize player's attack rect. """
        
        len_of_attack_box = 3 * self.player_update.player_rect[2]  # self.player_update.player_rect[2] LAIUS, self.player_update.player_rect[3] K6RGUS

        if keys[0]:  # up
            start_x, start_y = self.player_update.player_rect[0] - len_of_attack_box, self.player_update.player_rect[1] - len_of_attack_box * 1.5
            end_x_width, end_y_height = len_of_attack_box * 2 + self.player_update.player_rect[2], len_of_attack_box * 1.5

        elif keys[1]:  # down
            start_x, start_y = self.player_update.player_rect[0] - len_of_attack_box, self.player_update.player_rect[1] + self.player_update.player_rect[3]
            end_x_width, end_y_height = len_of_attack_box * 2 + self.player_update.player_rect[2], len_of_attack_box * 1.5

        elif keys[2]:  # left
            start_x, start_y = self.player_update.player_rect[0] - len_of_attack_box * 1.5, self.player_update.player_rect[1] - len_of_attack_box
            end_x_width, end_y_height = len_of_attack_box * 1.5, len_of_attack_box * 2 + self.player_update.player_rect[3]

        elif keys[3]:  # right
            start_x, start_y = self.player_update.player_rect[0] + self.player_update.player_rect[2], self.player_update.player_rect[1] - len_of_attack_box
            end_x_width, end_y_height = len_of_attack_box * 1.5, len_of_attack_box * 2 + self.player_update.player_rect[3]

        self.player_attack_rect = pygame.Rect(start_x, start_y, end_x_width, end_y_height)
        pygame.draw.rect(self.variables.screen, (255, 255, 0), self.player_attack_rect, 6)  # visuaal
        
        return self.player_attack_rect  # return player_attack_rect
        

    def calculate_entity_knockback(self, x, y):
        player_grid_y = self.variables.player_y // self.variables.block_size
        player_grid_x = self.variables.player_x // self.variables.block_size
        xdx, ydx = int(x), int(y)
        knockback_stenght = 2
        attack_key_tuple = self.variables.attack_key_pressed[1]

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
        new_HP = HP - self.variables.player_damage

        if new_HP <= 0:

            # add entity to dead entity list
            self.entity.dead_entity_list[entity_name] = (x, y, False)
            have_geiger = 'Geiger' in self.inv.inventory
            if random.random() < 0.05 or have_geiger == False:  # 5% chance
                self.entity.dead_entity_list[entity_name] = (x, y, True)

            del self.entity.path[entity_name]
            del self.entity.spawned_entity_dict[entity_name]
            # Player_audio.ghost_died_audio(self)

            if self.variables.debug_mode:
                print(f"Killed {entity_name}.")
                return

            return

        # # Add knockback to entity
        x, y = self.calculate_entity_knockback(x, y)
        self.entity.spawned_entity_dict[entity_name] = entity_image, x, y, new_HP
        # Player_audio.ghost_hurt_audio(self)

        if self.variables.debug_mode:
            print(
                f"Attacking: {entity_name}. HP dropped from {entity_info[-1]} to {entity_info[-1] - self.variables.player_damage}.")
            return
        return

    def update(self, atk_cls, click=False, pressed=False):
        if click:
            entity_data = self.find_entity(click=click)
            if entity_data:
                print(entity_data)
                entity_name, entity_info = entity_data
                self.damage_entity(entity_name, entity_info)
                atk_cls.last_attack_cooldown = 0

        if pressed:
            _, keys = self.variables.attack_key_pressed
            self.attack_rect(keys)  # Siin tekib self.player_attack_rect
            
            entity_data = self.find_entity(pressed=pressed)  # find_entity vajab self.player_attack_recti
            if entity_data:
                entity_name, entity_info = entity_data
                self.damage_entity(entity_name, entity_info)
                atk_cls.last_attack_cooldown = 0



class AttackObject:
    def __init__(self, terrain_data, inv):
        self.terrain_data = terrain_data
        self.inv = inv

        self.default_color = 255, 120, 20, 150
        self.click_color = 255, 0, 0, 255

    def find_object(self, click: tuple[int, int]) -> bool:
        for object_info in list(self.variables.object_list):
            object_id: int = object_info[5]
            is_valid_object: bool = search_item_from_items(type=ObjectItem, item_name_or_id=object_id,
                                                           target_attribute="Breakable")

            if not is_valid_object:
                continue

            x, y, width, height = object_info[:4]
            object_rect: pygame.Rect = pygame.Rect(x, y, width, height)

            if not object_rect.collidepoint(click):
                continue

            # Ei saa listi salvestada vale offsetiga, võtab praegu ära ja liidab hiljem juurde
            x_minus_offset: float = y - self.variables.offset_y
            y_minus_offset: float = x - self.variables.offset_x

            rect_key: tuple = x_minus_offset, y_minus_offset, width, height

            item: dict[str, any] = find_item_by_id(object_id)
            if rect_key not in self.variables.object_hp_dict:
                hp: float = item['hp'] if isinstance(item, dict) else item.hp if item and hasattr(item, 'hp') else 3
                self.variables.object_hp_dict[rect_key] = {'hp': hp, 'id': object_id,
                                                               'timer': self.variables.object_reset_timer}

            # Resetib timerit iga kord, kui objectit attackid
            else:
                self.variables.object_hp_dict[rect_key]['timer'] = self.variables.object_reset_timer

            self.deal_damage(rect_key, object_rect)

            return True

    def deal_damage(self, rect_key: tuple[float, float, int, int],
                    object_rect) -> None:
        object_data: dict[str, any] = self.variables.object_hp_dict.get(rect_key)

        if not object_data:
            return

        current_hp: float = object_data['hp']
        new_hp: float = current_hp - self.variables.player_damage

        if new_hp < 0:
            new_hp = 0

        object_data['hp'] = new_hp

        x_minus_offset, y_minus_offset, _, _ = rect_key

        if new_hp <= 0:
            # X ja Y peavad olema vastupidi --> grid asi
            was_removed = self.object_management.remove_object_at_position(y_minus_offset, x_minus_offset, object_data['id'])
            if was_removed:
                del self.variables.object_hp_dict[rect_key]

            # Kui inv oli täis ja itemit ülesse ei saanud võtta siis jätab objecti 'HP'ks 1
            else:
                new_hp = 1
                object_data['hp'] = new_hp

        transparent_surface = pygame.Surface((self.variables.screen_x, self.variables.screen_y),
                                             pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, self.click_color, object_rect, 3)

        self.variables.screen.blit(transparent_surface, (0, 0))

        self.variables.interaction_delay = 0

    def update_timers(self) -> None:
        for rect_key in list(self.variables.object_hp_dict.keys()):
            object_data = self.variables.object_hp_dict[rect_key]
            object_data['timer'] -= 1

            if object_data['timer'] <= 0:
                del self.variables.object_hp_dict[rect_key]

    def draw_hover_rect(self) -> None:
        mouse_pos = pygame.mouse.get_pos()

        transparent_surface = pygame.Surface((self.variables.screen_x, self.variables.screen_y),
                                             pygame.SRCALPHA)

        for object_info in list(self.variables.object_list):
            object_id: int = object_info[5]
            is_valid_object: bool = search_item_from_items(type=ObjectItem, item_name_or_id=object_id,
                                                           target_attribute="Breakable")

            if not is_valid_object:
                continue

            x, y, width, height = object_info[:4]
            object_rect = pygame.Rect(x, y, width, height)

            if object_rect.collidepoint(mouse_pos):
                pygame.draw.rect(transparent_surface, self.default_color, object_rect, 2)

                self.variables.screen.blit(transparent_surface, (0, 0))
                return

        return

    def update(self, click: tuple[int, int]) -> None:
        if self.variables.interaction_delay >= self.variables.interaction_delay_max:
            self.find_object(click)
