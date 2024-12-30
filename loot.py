from random import shuffle, choice, randint  # Randomized loot barrelitest

from camera import Camera
from variables import UniversalVariables
from objects import ObjectManagement
from inventory import Inventory
from audio import Player_audio
from text import Fading_text


class Loot:
    def __init__(self, camera, inv, terrain_data, click_tuple):
        self.camera = camera
        self.inv = inv
        self.terrain_data = terrain_data

        self.click_position = click_tuple[0]
        self.click_window_x = click_tuple[1]
        self.click_window_y = click_tuple[2]

        self.right_click_position = click_tuple[3]
        self.right_click_window_x = click_tuple[4]
        self.right_click_window_y = click_tuple[5]

        self.obtained_loot_list = []

    def toggle_loot_barrel(self, right_click_position, player_pressed_pick_up=False):

        count = randint(1, 3)
        inv_count = len(UniversalVariables.loot)
        if player_pressed_pick_up:
            barrel_x, barrel_y = UniversalVariables.player_x, UniversalVariables.player_y
        else:
            if not right_click_position:
                return
            barrel_x, barrel_y = right_click_position

        if not barrel_x or not barrel_y:
            return

        for item, quantity in UniversalVariables.loot:
            if item in self.inv.inventory:
                inv_count -= 1

            barrel_x = int(barrel_x // UniversalVariables.block_size)
            barrel_y = int(barrel_y // UniversalVariables.block_size)
            if 0 <= barrel_x < len(self.terrain_data[0]) and 0 <= barrel_y < len(self.terrain_data):

                if self.terrain_data[barrel_y][barrel_x] == 1001 and self.inv.total_slots >= len(self.inv.inventory) + inv_count or self.terrain_data[barrel_y][ barrel_x] == 1001 and self.inv.total_slots >= len(self.inv.inventory) + count:
                    self.terrain_data[barrel_y][barrel_x] = 1002
                    self.gather_loot(count)
                    # Player_audio.opening_a_barrel_audio(self)


                elif self.terrain_data[barrel_y][barrel_x] == 1001 and self.inv.total_slots < len(
                        self.inv.inventory) + inv_count:
                    # Player_audio.opening_a_barrel_audio(self, False)

                    Fading_text.re_display_fading_text("Not enough space in Inventory.")

                else:
                    return

    def get_random_loot(self):
        shuffle(UniversalVariables.loot)
        selected_loot = choice(UniversalVariables.loot)
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
            ObjectManagement.add_object_from_inv(self, obtained_loot, obtained_count)

    def loot_update(self, right_click_pos, player_pressed_pick_up=False):
        right_click_x, right_click_y = right_click_pos
        if right_click_x is None or right_click_y is None and player_pressed_pick_up == False:
            return

        right_click_position = right_click_x, right_click_y

        self.toggle_loot_barrel(right_click_position, player_pressed_pick_up)
        # self.camera.reset_clicks()
