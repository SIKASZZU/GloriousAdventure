from variables import UniversalVariables
from objects import ObjectManagement
from audio import Player_audio
from camera import Camera
from items import items_list

class Building:
    def is_valid_item(self) -> tuple:
        """
        Vaatab kas equipped item on 'Placeable' või ei. Kui on siis otsib selle ID.
        Return'ib (item_name, object_id) if valid, else False.
        """
        if not UniversalVariables.current_equipped_item:
            return False

        item_name = UniversalVariables.current_equipped_item

        for item in items_list:
            if item_name == item.get("Name"):
                item_id = item["ID"]

                if not item.get("Placeable", False):
                    return False

                return item_name, item_id

        return False

    def is_valid_location(self) -> tuple:
        """
        Vaatab kas valitud koht on valid.
        Return'ib (grid_x, grid_y) if valid (terrain_data[grid_y][grid_x] == 1), else False.
        """
        click_position = Camera.click_on_screen(self)

        if click_position:
            terrain_x, terrain_y = click_position
            grid_x, grid_y = int(terrain_x // UniversalVariables.block_size), int(
                terrain_y // UniversalVariables.block_size)

            if 0 <= grid_x < len(self.terrain_data[0]) and 0 <= grid_y < len(self.terrain_data):
                terrain_value = self.terrain_data[grid_y][grid_x]

                if terrain_value == 1:
                    neighbors = [
                        self.terrain_data[grid_y - 1][grid_x],
                        self.terrain_data[grid_y - 1][grid_x - 1],
                        self.terrain_data[grid_y][grid_x - 1],
                    ]
                    if all(value not in {4, 5} for value in neighbors):  # Et puude ja tüvede peale ei saaks midagi ehitada
                        return grid_x, grid_y

        return False

    def change_terrain_value(self, item_name: str, item_id: int, grid_x: int, grid_y: int) -> bool:
        """
        Muudab valitud asukoha terrain value antud itemi valueks ja võtab selle invi'st ära.
        """
        try:
            if 0 <= grid_y < len(self.terrain_data) and 0 <= grid_x < len(self.terrain_data[0]):
                self.terrain_data[grid_y][grid_x] = item_id
                ObjectManagement.remove_object_from_inv(item_name)
                Player_audio.player_item_audio(self)
                return True
            else:
                return False
        except Exception:
            return False

    def update(self) -> bool:
        if Building.is_valid_item(self) and Building.is_valid_location(self):
            item_name, item_id = Building.is_valid_item(self)
            grid_x, grid_y = Building.is_valid_location(self)
            return Building.change_terrain_value(self, item_name, item_id, grid_x, grid_y)

        return False
