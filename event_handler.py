import pygame
from variables import UniversalVariables
import items
from loot import Loot
from menu import PauseMenu
from components import Player


def update_object_dimensions():
    for item in items.items_list:
        if isinstance(item, items.WorldItem) or isinstance(item, items.ObjectItem):
            pass
        else:
            continue

        if item.width:
            item.width = int(item.width * UniversalVariables.block_size / items.block_size)
        if item.height:
            item.height = int(item.height * UniversalVariables.block_size / items.block_size)
    items.block_size = UniversalVariables.block_size


class Event_handler:
    def __init__(self, click_tuple, camera, vision, inv, player, camera_click_tuple, terrain_data, loot):
        self.click_position = click_tuple[0]
        self.click_window_x = click_tuple[1]
        self.click_window_y = click_tuple[2]

        self.right_click_position = click_tuple[3]
        self.right_click_window_x = click_tuple[4]
        self.right_click_window_y = click_tuple[5]

        self.camera = camera
        self.vision = vision
        self.inv = inv
        self.player = player

        self.camera_rect = camera_click_tuple[0]

        self.player_window_x = camera_click_tuple[1]
        self.player_window_y = camera_click_tuple[2]

        self.click_x = camera_click_tuple[3]
        self.click_y = camera_click_tuple[4]

        self.terrain_data = terrain_data
        self.loot = loot



    def handle_mouse_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.click_position = event.pos
                self.click_x, self.click_y = self.camera.left_click_on_screen(self.click_position)

            if event.button == 3:
                # TODO vaadata kuhu clickib ja selle järgi edasi minna, callida midagi

                self.right_click_position = event.pos
                self.right_click_x, self.right_click_y = self.camera.right_click_on_screen(self.right_click_position)
                self.loot.loot_update(self.right_click_x, self.right_click_y)

            if UniversalVariables.debug_mode:
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
                self.inv.crafting_menu_open = not self.inv.crafting_menu_open

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if not PauseMenu.game_paused:
                    PauseMenu.game_paused = True
                else:
                    PauseMenu.screenshot = None
                    PauseMenu.game_paused = False
                    self.pause_menu_state = "main"
                    PauseMenu.screenshot = None

    def check_pressed_keys(self):
        keys = pygame.key.get_pressed()
        arrow_keys = (keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_LEFT], keys[pygame.K_RIGHT])
        keybinds = {
            pygame.K_h: lambda: setattr(UniversalVariables, 'render_boxes_counter',
                                        not UniversalVariables.render_boxes_counter),
            pygame.K_j: lambda: setattr(self.vision, 'vision_count', not self.vision.vision_count),
            pygame.K_g: lambda: setattr(UniversalVariables, 'fps_lock', not UniversalVariables.fps_lock),
        }

        if UniversalVariables.debug_mode:
            for key, action in keybinds.items():
                key_pressed_attr = f'{key}_pressed'
                if keys[key] and not getattr(self, key_pressed_attr, False):
                    setattr(self, key_pressed_attr, True)
                    action()
                elif not keys[key]:
                    setattr(self, key_pressed_attr, False)

        if any(arrow_keys):
            UniversalVariables.attack_key_pressed = (True, arrow_keys)

            if keys[pygame.K_UP]:
                self.player.attack('up')
            elif keys[pygame.K_DOWN]:
                self.player.attack('down')
            elif keys[pygame.K_LEFT]:
                self.player.attack('left')
            elif keys[pygame.K_RIGHT]:
                self.player.attack('right')
