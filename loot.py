from random import shuffle, choice, randint  # Randomized loot barrelitest

from camera import Camera
from variables import UniversalVariables
from objects import ObjectManagement  # add_object_from_inv
from inventory import Inventory
from audio import Player_audio
from text import Fading_text

class Loot:
    obtained_loot_list = []

    def toggle_loot_barrel(self, player_pressed_pick_up=False):
        click_position = Camera.right_click_on_screen(self)
        if click_position and click_position == (None, None) and player_pressed_pick_up == False:  # or player collision
            return
        count = randint(1, 3)
        inv_count = len(UniversalVariables.loot)
        barrel_x, barrel_y = None, None

        if player_pressed_pick_up == True:
            barrel_x, barrel_y = UniversalVariables.player_x, UniversalVariables.player_y
        else:
            if not click_position:
                return
            barrel_x, barrel_y = click_position

        if not barrel_x or not barrel_y:
            return

        for item, quantity in UniversalVariables.loot:
            if item in Inventory.inventory:
                inv_count -= 1

            barrel_x = int(barrel_x // UniversalVariables.block_size)
            barrel_y = int(barrel_y // UniversalVariables.block_size)
            if 0 <= barrel_x < len(self.terrain_data[0]) and 0 <= barrel_y < len(self.terrain_data):

                if self.terrain_data[barrel_y][barrel_x] == 1001 and Inventory.total_slots >= len(Inventory.inventory) + inv_count or self.terrain_data[barrel_y][barrel_x] == 1001 and Inventory.total_slots >= len(Inventory.inventory) + count:
                    self.terrain_data[barrel_y][barrel_x] = 1002
                    Loot.gather_loot(self, count)
                    Player_audio.opening_a_barrel_audio(self)


                elif self.terrain_data[barrel_y][barrel_x] == 1001 and Inventory.total_slots < len(Inventory.inventory) + inv_count:
                    Player_audio.opening_a_barrel_audio(self, False)

                    Fading_text.re_display_fading_text("Not enough space in Inventory.")

                else:
                    return

    def get_random_loot(self):
        shuffle(UniversalVariables.loot)
        selected_loot = choice(UniversalVariables.loot)
        Loot.obtained_loot_list.append(selected_loot)

        # Kui itemil on range näiteks (2, 5) siis ta võtab random numbri nende seast - (2, 3, 4, 5)
        if isinstance(selected_loot[1], tuple):
            a, b = selected_loot[1]
            selected_loot = (selected_loot[0], randint(a, b))
            return selected_loot

        else:
            return selected_loot

    def gather_loot(self, count):
        while count > 0:
            obtained_loot, obtained_count = Loot.get_random_loot(self)
            count -= 1
            ObjectManagement.add_object_from_inv(obtained_loot, obtained_count)

    def loot_update(self, player_pressed_pick_up=False):
        Loot.toggle_loot_barrel(self, player_pressed_pick_up)
        Camera.reset_clicks(self)
