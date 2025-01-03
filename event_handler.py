import pygame
import items
from menu import PauseMenu


def update_object_dimensions(self):
    for item in items.items_list:
        if isinstance(item, items.WorldItem) or isinstance(item, items.ObjectItem):
            pass
        else:
            continue

        if item.width:
            item.width = int(item.width * self.variables.block_size / items.block_size)
        if item.height:
            item.height = int(item.height * self.variables.block_size / items.block_size)
    items.block_size = self.variables.block_size


class Event_handler:
    def __init__(
            self, camera, vision, inv, player,
            terrain_data, loot, menu_states_tuples, variables
            ) -> None:

        self.camera = camera
        self.vision = vision
        self.inv = inv
        self.player = player

        self.terrain_data = terrain_data
        self.loot = loot

        self.game_menu_state = menu_states_tuples[0]
        self.pause_menu_state = menu_states_tuples[1]

        self.variables = variables

    def handle_mouse_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.camera.click_position = event.pos
                self.camera.click_x, self.camera.click_y = self.camera.left_click_on_screen(self.camera.click_position)

            if event.button == 3:
                self.camera.right_click_position = event.pos
                self.loot.loot_update(right_click_pos=self.camera.right_click_on_screen())

            if self.variables.debug_mode:
                if event.button == 4:  # Scroll +
                    self.variables.block_size += 10
                    update_object_dimensions(self)

                elif event.button == 5:  # Scroll -
                    self.variables.block_size -= 10
                    if self.variables.block_size < 1:
                        self.variables.block_size = 1
                    update_object_dimensions(self)

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
            pygame.K_h: lambda: setattr(self.variables, 'render_boxes_counter',
                                        not self.variables.render_boxes_counter),
            pygame.K_j: lambda: setattr(self.vision, 'vision_count', not self.vision.vision_count),
            pygame.K_g: lambda: setattr(self.variables, 'fps_lock', not self.variables.fps_lock),
        }

        if self.variables.debug_mode:
            for key, action in keybinds.items():
                key_pressed_attr = f'{key}_pressed'
                if keys[key] and not getattr(self, key_pressed_attr, False):
                    setattr(self, key_pressed_attr, True)
                    action()
                elif not keys[key]:
                    setattr(self, key_pressed_attr, False)

        if any(arrow_keys):
            self.variables.attack_key_pressed = (True, arrow_keys)

            # if keys[pygame.K_UP]:
            #     self.attack_entity.attack_rect('up')
            # elif keys[pygame.K_DOWN]:
            #     self.attack_entity.attack_rect('down')
            # elif keys[pygame.K_LEFT]:
            #     self.attack_entity.attack_rect('left')
            # elif keys[pygame.K_RIGHT]:
            #     self.attack_entity.attack_rect('right')
