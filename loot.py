from random import shuffle, choice, randint  # Randomized loot barrelitest

from camera import Camera
from variables import UniversalVariables
from objects import ObjectManagement  # add_object_from_inv
from collisions import reset_clicks
from inventory import Inventory

class Loot:
    obtained_loot_list = []

    def toggle_loot_barrel(self):
        count = randint(1, 3)
        inv_count = len(UniversalVariables.loot)

        for item, quantity in UniversalVariables.loot:
            if item in Inventory.inventory:
                inv_count -= 1

        click_position = Camera.click_on_screen(self)
        if click_position and click_position != (None, None):
            barrel_x, barrel_y = click_position
            barrel_x = int(barrel_x // UniversalVariables.block_size)
            barrel_y = int(barrel_y // UniversalVariables.block_size)
            if 0 <= barrel_x < len(self.terrain_data[0]) and 0 <= barrel_y < len(self.terrain_data):

                    if self.terrain_data[barrel_y][barrel_x] == 1001 and Inventory.total_slots >= len(Inventory.inventory) + inv_count or self.terrain_data[barrel_y][barrel_x] == 1001 and Inventory.total_slots >= len(Inventory.inventory) + count:
                        self.terrain_data[barrel_y][barrel_x] = 1002
                        Loot.gather_loot(self, count)


                    elif self.terrain_data[barrel_y][barrel_x] == 1001 and Inventory.total_slots < len(Inventory.inventory) + inv_count:
                        text = "Not enough space in Inventory."
                        UniversalVariables.ui_elements.append(text)

                        if text in self.shown_texts:  # Check if the text is in the set before removing
                            self.shown_texts.remove(text)

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

    def loot_update(self):
        Loot.toggle_loot_barrel(self)
        reset_clicks(self)
