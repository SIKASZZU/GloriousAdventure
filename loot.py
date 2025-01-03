from random import shuffle, choice, randint  # Randomized loot barrelitest
import pygame

class Loot:
    def __init__(self, camera, inv, terrain_data, fading_text, o_management, variables, player_update, screen):
        self.camera = camera
        self.inv = inv
        self.terrain_data = terrain_data
        self.fading_text = fading_text
        self.object_management = o_management
        self.variables = variables
        self.screen = screen

        self.player_update = player_update

        self.obtained_loot_list = []

    def toggle_loot_barrel(self, right_click_position=None, player_pressed_pick_up=None):
        barrel_x = barrel_y = None
        count = randint(1, 3)
        inv_count = len(self.variables.loot)


        if player_pressed_pick_up:
            for item in self.variables.object_list:
                if item[5] in [1001]:  # Barrel
                    x = item[0] - self.variables.offset_x
                    y = item[1] - self.variables.offset_y
                    barrel_rect = pygame.Rect(x, y, item[2], item[3])

                    intersection = self.player_update.player_rect.clip(barrel_rect)
                    if intersection.width > 0 and intersection.height > 0:
                        barrel_x, barrel_y = x, y
                        break

        if right_click_position:
            for item in self.variables.object_list:
                if item[5] in [1001]:  # Barrel
                    x = item[0] - self.variables.offset_x
                    y = item[1] - self.variables.offset_y
                    barrel_rect = pygame.Rect(x, y, item[2], item[3])
                    if barrel_rect.collidepoint(right_click_position):
                        barrel_x, barrel_y = x, y
                        break

        if not barrel_x or not barrel_y:
            return

        for item, quantity in self.variables.loot:
            if item in self.inv.inventory:
                inv_count -= 1

            barrel_x = int(barrel_x // self.variables.block_size)
            barrel_y = int(barrel_y // self.variables.block_size)

            if 0 <= barrel_x < len(self.terrain_data[0]) and 0 <= barrel_y < len(self.terrain_data):
                if self.terrain_data[barrel_y][barrel_x] == 1001 and self.inv.total_slots >= len(
                        self.inv.inventory) + inv_count or self.terrain_data[barrel_y][
                    barrel_x] == 1001 and self.inv.total_slots >= len(self.inv.inventory) + count:
                    self.terrain_data[barrel_y][barrel_x] = 1002
                    self.gather_loot(count)
                    # Player_audio.opening_a_barrel_audio(self)


                elif self.terrain_data[barrel_y][barrel_x] == 1001 and self.inv.total_slots < len(
                        self.inv.inventory) + inv_count:
                    # Player_audio.opening_a_barrel_audio(self, False)

                    self.fading_text.re_display_fading_text("Not enough space in Inventory.")

                else:
                    return

    def get_random_loot(self):
        shuffle(self.variables.loot)
        selected_loot = choice(self.variables.loot)
        self.obtained_loot_list.append(selected_loot)

        # Kui itemil on range näiteks (2, 5) siis ta võtab random numbri nende seast - (2, 3, 4, 5)
        if isinstance(selected_loot[1], tuple):
            a, b = selected_loot[1]
            selected_loot = (selected_loot[0], randint(a, b))
            return selected_loot

        else:
            return selected_loot

    def gather_loot(self, count):
        while count > 0:
            obtained_loot, obtained_count = self.get_random_loot()
            count -= 1

            # TODO: ObjectManagement -> self.object_management.add_object_from_inv(obtained_loot, obtained_count)
            self.object_management.add_object_from_inv(obtained_loot, obtained_count)

    def loot_update(self, right_click_pos=None, player_pressed_pick_up=None):
        if right_click_pos is not None:
            self.toggle_loot_barrel(right_click_position=right_click_pos)

        elif player_pressed_pick_up:
            self.toggle_loot_barrel(player_pressed_pick_up=player_pressed_pick_up)
