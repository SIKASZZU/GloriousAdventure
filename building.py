from items import items_list, ObjectItem


class Building:
    def __init__(self, variables, camera, terrain_data, player_audio, obm):
        self.variables = variables
        self.camera = camera
        self.terrain_data = terrain_data
        self.player_audio = player_audio
        self.object_management = obm

    def is_valid_item(self) -> tuple[any, int] | None:
        """
        Vaatab kas equipped item on 'Placeable' või ei. Kui on siis otsib selle ID.
        Return'ib (name, object_id) if valid, else False.
        """
        name = self.variables.current_equipped_item

        if not name:
            return

        for item in items_list:
            if name == item.name:
                if isinstance(item, ObjectItem) and item.placeable:
                    return name, item.id


    def is_valid_location(self) -> None | bool | tuple[int, int]:
        """
        Vaatab kas valitud koht on valid.
        Return'ib (grid_x, grid_y) if valid (terrain_data[grid_y][grid_x] == 1), else False.
        """
        click_position = self.camera.left_click_on_screen(self.camera.click_position)

        if None in click_position:
            return

        terrain_x, terrain_y = click_position

        grid_x, grid_y = int(terrain_x // self.variables.block_size), int(
            terrain_y // self.variables.block_size)

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
                self.object_management.remove_object_from_inv(name)
                self.player_audio.player_item_audio()
                return True
            else:
                return False
        except Exception:
            return False

    def update(self) -> bool | None:
        if not self.variables.allow_building:
            return

        if self.is_valid_item() and self.is_valid_location():
            name, id = self.is_valid_item()
            grid_x, grid_y = self.is_valid_location()
            return self.change_terrain_value(name, id, grid_x, grid_y)

        return
