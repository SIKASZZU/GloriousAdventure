import pygame
import numpy as np

from items import *
from cooking import Cooking
from variables import UniversalVariables, GameConfig

class ObjectManagement:

    def __init__(self, inv, fading_text, player_audio, terrain_data):
        self.inv = inv
        self.fading_text = fading_text
        self.player_audio = player_audio
        self.terrain_data = terrain_data

    def remove_object_at_position(self, terrain_x: int, terrain_y: int, object_id: int = None) -> None:
        """ Items cannot be picked up until they are added to the minerals list """

        # If object ID is None, skip to avoid errors
        if object_id is None:
            return False

        # Fetch the item from the dictionary
        item = find_item_by_id(object_id)

        if not item:
            return False

        # Check if item is breakable (only ObjectItem has the breakable attribute)
        if isinstance(item, ObjectItem):
            if not item.breakable:
                return False
        else:
            return False

        # Check interaction delay
        if self.variables.interaction_delay < self.variables.interaction_delay_max:
            if self.variables.debug_mode:
                print(
                    f"Don't pick up so fast: {self.variables.interaction_delay} < {self.variables.interaction_delay_max}")
            return False


        if object_id in GameConfig.COOKING_STATIONS.value:

            for key, station in Cooking.stations.items():
                raw_item, _ = station["station_raw_item"]
                cooked_item, _ = station["station_cooked_item"]

                if not raw_item == None or not cooked_item == None:
                    self.fading_text.re_display_fading_text("Aren't you forgetting something?")
                    self.variables.interaction_delay = 0
                    self.player_audio.error_audio()
                    return False


        # Handle item drops
        name = item.name
        choice = None
        amount = 1

        if isinstance(item, ObjectItem):  # object item'itel on drop attribute
            choice, probabilities, amount = item.drops
            name = np.random.choice(choice, p=probabilities)

            # Check inventory space for the dropped items
            choice_len = sum(1 for drop_item in choice if drop_item not in self.inv.inventory)

            if self.inv.total_slots >= len(self.inv.inventory) + choice_len:
                self.update_terrain_and_add_item(terrain_x, terrain_y, object_id, name, amount)
                return True
            else:
                self.inv.inventory_full_error()
            return False

        if self.inv.total_slots > len(self.inv.inventory) or name in self.inv.inventory:
            self.update_terrain_and_add_item(terrain_x, terrain_y, object_id, name, amount)
            return True
        else:
            self.inv.inventory_full_error()
            return False

    def update_terrain_and_add_item(self, terrain_x: int, terrain_y: int, object_id: int, name: str, amount: int) -> bool:
        grid_col: int = int(terrain_x // self.variables.block_size)
        grid_row: int = int(terrain_y // self.variables.block_size)

        # Ensure the coordinates are within the terrain boundaries
        if not (0 <= grid_row < len(self.terrain_data) and 0 <= grid_col < len(self.terrain_data[0])):
            return False

        terrain_update = {
            4: 5,       # Oak tree stump
            10: 98,     # Empty key slot
            12: 98,     # Empty key slot
            13: 98,     # Empty key slot
            7: 69,      # Farmland
            71: 72,      # Farmland
            74: 75,      # Farmland
            77: 78,      # Farmland

            1008: 1015,  # Berry bush - Large
            1010: 1016,  # Berry bush - Medium
            1012: 1013  # Berry bush - Small

        }
        self.terrain_data[grid_row][grid_col] = terrain_update.get(object_id, 1)  # Default to Ground

        self.add_object_from_inv(name, amount)
        # self.player_audio.player_item_audio()
        self.variables.interaction_delay = 0
        return True

    def add_object_from_inv(self, item, amount=1):
        if item in self.inv.inventory:
            # Kui ese on juba inventoris, suurendab eseme kogust
            self.inv.inventory[item] += amount

        elif self.inv.total_slots > len(self.inv.inventory):
            # Kui tegemist on uue esemega, lisab selle inventori ja annab talle koguse: amount
            self.inv.inventory[item] = amount

        else: 
            print(f'Item name: {item} not found and not added to inv!')
            return


    def remove_object_from_inv(self, item):
        if self.inv.inventory[item] > 0 :
            self.inv.inventory[item] -= 1
        
        if self.inv.inventory[item] == 0:
            del self.inv.inventory[item]

    @staticmethod
    def render_collision_box() -> None:
        for box_item in self.variables.collision_boxes:
            item_start_x, item_start_y  = box_item[0], box_item[1]
            item_width, item_height = box_item[2], box_item[3]
            obj_collision_box = pygame.Rect(item_start_x, item_start_y, item_width, item_height)
            collision_box_color = 'green'
            pygame.draw.rect(self.variables.screen, collision_box_color, obj_collision_box, 3)

    @staticmethod
    def render_interaction_box() -> None:
        # terrain_x, terrain_y, object_width, object_height, object_image, object_id
        for box_item in self.variables.object_list:
            outline_thickness = 3
            if box_item[5] in [981, 982]:
                outline_thickness = 8
            
            item_start_x, item_start_y = box_item[0], box_item[1]
            item_width, item_height = box_item[2], box_item[3]
            obj_collision_box = pygame.Rect(item_start_x, item_start_y, item_width, item_height)
            collision_box_color = 'pink'
            pygame.draw.rect(self.variables.screen, collision_box_color, obj_collision_box, outline_thickness, 5)
