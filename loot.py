from camera import Camera
from variables import UniversalVariables
from objects import ObjectManagement  # add_object_from_inv
from collisions import reset_clicks
class Loot:
    def toggle_loot_barrel(self):
        click_position = Camera.click_on_screen(self)
        if click_position and click_position != (None, None):
            barrel_x, barrel_y = click_position
            barrel_x = int(barrel_x // UniversalVariables.block_size)
            barrel_y = int(barrel_y // UniversalVariables.block_size)
            if 0 <= barrel_x < len(self.terrain_data[0]) and 0 <= barrel_y < len(self.terrain_data):
                if self.terrain_data[barrel_y][barrel_x] == 1001:
                    self.terrain_data[barrel_y][barrel_x] = 1002
                    Loot.get_loot_from_barrel(self)
    def get_loot_from_barrel(self):
        count = UniversalVariables.loot_size

        for tuple in UniversalVariables.loot_set:
            item, amount = tuple
            ObjectManagement.add_object_from_inv(item, amount)
            count -= 1
            if count == 0:
                break
    def loot_update(self):
        Loot.toggle_loot_barrel(self)
        reset_clicks(self)
