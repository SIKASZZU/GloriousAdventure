from variables import UniversalVariables
from objects import ObjectManagement
from audio import Player_audio
from camera import Camera
from items import items_list, ObjectItem

class Building:
    def is_valid_item(self) -> tuple:
        """
        Vaatab kas equipped item on 'Placeable' või ei. Kui on siis otsib selle ID.
        Return'ib (name, object_id) if valid, else False.
        """
        name = UniversalVariables.current_equipped_item

        if not name:
            return False

        for item in items_list:
            if name == item.name:
                if isinstance(item, ObjectItem) and item.placeable:
                    return name, item.id

        return False

    def is_valid_location(self) -> tuple:
        """
        Vaatab kas valitud koht on valid.
        Return'ib (grid_x, grid_y) if valid (terrain_data[grid_y][grid_x] == 1), else False.
        """
        click_position = Camera.left_click_on_screen(self)

        if None in click_position:
            return

        terrain_x, terrain_y = click_position

        grid_x, grid_y = int(terrain_x // UniversalVariables.block_size), int(
            terrain_y // UniversalVariables.block_size)

        if 0 <= grid_x < len(self.terrain_data[0]) and 0 <= grid_y < len(self.terrain_data):
            terrain_value = self.terrain_data[grid_y][grid_x]

            if not terrain_value == 1:
                return False

            neighbors = [
                self.terrain_data[grid_y - 1][grid_x],
                self.terrain_data[grid_y - 1][grid_x - 1],
                self.terrain_data[grid_y][grid_x - 1],
            ]
            if all(value not in {4, 5} for value in neighbors):  # Et puude ja tüvede peale ei saaks midagi ehitada
                return grid_x, grid_y


    def change_terrain_value(self, name: str, id: int, grid_x: int, grid_y: int) -> bool:
        """
        Muudab valitud asukoha terrain value antud itemi valueks ja võtab selle invi'st ära.
        """
        try:
            if 0 <= grid_y < len(self.terrain_data) and 0 <= grid_x < len(self.terrain_data[0]):
                self.terrain_data[grid_y][grid_x] = id
                ObjectManagement.remove_object_from_inv(name)
                Player_audio.player_item_audio(self)
                return True
            else:
                return False
        except Exception:
            return False

    def update(self) -> bool:
        if not UniversalVariables.allow_building:
            return

        if Building.is_valid_item(self) and Building.is_valid_location(self):
            name, id = Building.is_valid_item(self)
            grid_x, grid_y = Building.is_valid_location(self)
            return Building.change_terrain_value(self, name, id, grid_x, grid_y)

        return False
