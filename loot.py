from random import shuffle, choice, randint  # Randomized loot barrelitest

from camera import Camera
from variables import UniversalVariables
from objects import ObjectManagement  # add_object_from_inv
from collisions import reset_clicks


class Loot:
    obtained_loot_list = []

    def toggle_loot_barrel(self):
        click_position = Camera.click_on_screen(self)
        if click_position and click_position != (None, None):
            barrel_x, barrel_y = click_position
            barrel_x = int(barrel_x // UniversalVariables.block_size)
            barrel_y = int(barrel_y // UniversalVariables.block_size)
            if 0 <= barrel_x < len(self.terrain_data[0]) and 0 <= barrel_y < len(self.terrain_data):
                if self.terrain_data[barrel_y][barrel_x] == 1001:
                    self.terrain_data[barrel_y][barrel_x] = 1002
                    Loot.gather_loot(self)

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

    def gather_loot(self):
        count = randint(0, 3)
        while count > 0:
            obtained_loot, obtained_count = Loot.get_random_loot(self)
            count -= 1
            ObjectManagement.add_object_from_inv(obtained_loot, obtained_count)

    def loot_update(self):
        Loot.toggle_loot_barrel(self)
        reset_clicks(self)
