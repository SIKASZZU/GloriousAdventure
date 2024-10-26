import pygame
from variables import UniversalVariables
from camera import Camera
import items
from loot import Loot
from inventory import Inventory
from menu import PauseMenu
import vision
from components import Player

def update_object_dimensions():
    for item in items.items_list:
        if "Object_width" in item:
            item["Object_width"] = int(item["Object_width"] * UniversalVariables.block_size / items.block_size)
        if "Object_height" in item:
            item["Object_height"] = int(item["Object_height"] * UniversalVariables.block_size / items.block_size)

    items.block_size = UniversalVariables.block_size


class Event_handler:
    def handle_mouse_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.click_position = event.pos
                Camera.left_click_on_screen(self)
                Loot.loot_update(self)
                Camera.left_click_on_screen(self)
            if event.button == 3:
                self.right_click_position = event.pos
                Camera.right_click_on_screen(self)

            if UniversalVariables.debug_mode == True:
                if event.button == 4:  # Scroll +
                    UniversalVariables.block_size += 10
                    update_object_dimensions()

                elif event.button == 5:  # Scroll -
                    UniversalVariables.block_size -= 10
                    if UniversalVariables.block_size < 1:
                        UniversalVariables.block_size = 1
                    update_object_dimensions()

    def handle_keyboard_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                Inventory.crafting_menu_open = not Inventory.crafting_menu_open

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if PauseMenu.game_paused == False:
                    PauseMenu.game_paused = True
                else:
                    PauseMenu.screenshot = None
                    PauseMenu.game_paused = False
                    self.pause_menu_state = "main"
                    PauseMenu.screenshot = None        
                    
    def check_pressed_keys(self):
        keys = pygame.key.get_pressed()

        arrow_keys = (keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_LEFT], keys[pygame.K_RIGHT])

        if UniversalVariables.debug_mode == True:


            # H key, HITBOX SHOW
            if keys[pygame.K_h] and not self.h_pressed:
                self.h_pressed = True
                UniversalVariables.render_boxes_counter += 1
            elif not keys[pygame.K_h]: self.h_pressed = False

            # J KEY, LIGHT ON/OFF
            if keys[pygame.K_j] and not self.j_pressed:
                self.j_pressed = True
                vision.vision_count += 1
            elif not keys[pygame.K_j]: self.j_pressed = False

        # ARROW KEYS (ATTACK KEYS)

        if any(arrow_keys):
            UniversalVariables.attack_key_pressed = True
            
            if keys[pygame.K_UP]:
                Player.attack(self, 'up')
            elif keys[pygame.K_DOWN]:
                Player.attack(self, 'down')
            elif keys[pygame.K_LEFT]:
                Player.attack(self, 'left')
            elif keys[pygame.K_RIGHT]:
                Player.attack(self, 'right')