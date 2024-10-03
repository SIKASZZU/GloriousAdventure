import pygame
from items import *
from inventory import Inventory
from variables import UniversalVariables, GameConfig
from audio import Player_audio
from text import Fading_text
import numpy as np
from cooking import Cooking

class ObjectManagement:

    def remove_object_at_position(self, terrain_x: int, terrain_y: int, object_id: int = None) -> None:
        """ Items cannot be picked up until they are added to the minerals list """

        # If object ID is None, skip to avoid errors
        if object_id is None:
            return

        # Fetch the item from the dictionary
        item = find_item_by_id(object_id)

        if not item:
            return

        # Check if item is breakable (only ObjectItem has the breakable attribute)
        if isinstance(item, ObjectItem):
            if not item.breakable:
                return
        else:
            return

        # Check interaction delay
        if UniversalVariables.interaction_delay < UniversalVariables.interaction_delay_max:
            if UniversalVariables.debug_mode:
                print(
                    f"Don't pick up so fast: {UniversalVariables.interaction_delay} < {UniversalVariables.interaction_delay_max}")
            return


        if object_id in GameConfig.COOKING_STATIONS.value:

            for key, station in Cooking.stations.items():
                raw_item, _ = station["station_raw_item"]
                cooked_item, _ = station["station_cooked_item"]

                if not raw_item == None or not cooked_item == None:
                    Fading_text.re_display_fading_text("Aren't you forgetting something?")
                    UniversalVariables.interaction_delay = 0
                    Player_audio.error_audio(self)
                    return


        # Handle item drops
        name = item.name
        choice = None
        amount = 1

        if isinstance(item, ObjectItem):  # object item'itel on drop attribute
            choice, probabilities, amount = item.drops
            name = np.random.choice(choice, p=probabilities)

            # Check inventory space for the dropped items
            choice_len = sum(1 for drop_item in choice if drop_item not in Inventory.inventory)

            if Inventory.total_slots >= len(Inventory.inventory) + choice_len:
                ObjectManagement.update_terrain_and_add_item(self, terrain_x, terrain_y, object_id, name, amount)
            else:
                Inventory.inventory_full_error(self)
            return

        if Inventory.total_slots > len(Inventory.inventory) or name in Inventory.inventory:
            ObjectManagement.update_terrain_and_add_item(self, terrain_x, terrain_y, object_id, name, amount)
        else:
            Inventory.inventory_full_error(self)

    def update_terrain_and_add_item(self, terrain_x: int, terrain_y: int, object_id: int, name: str, amount: int) -> bool:
        grid_col: int = int(terrain_x // UniversalVariables.block_size)
        grid_row: int = int(terrain_y // UniversalVariables.block_size)

        # Ensure the coordinates are within the terrain boundaries
        if not (0 <= grid_row < len(self.terrain_data) and 0 <= grid_col < len(self.terrain_data[0])):
            return False

        terrain_update = {
            4: 5,  # Oak tree stump
            10: 98,  # Empty key slot
            12: 98,  # Empty key slot
            13: 98,  # Empty key slot
            7: 69,  # Farmland
            1008: 1009,  # Berry bush - Large
            1010: 1011,  # Berry bush - Medium
            1012: 1013  # Berry bush - Small
        }
        self.terrain_data[grid_row][grid_col] = terrain_update.get(object_id, 1)  # Default to Ground

        ObjectManagement.add_object_from_inv(name, amount)
        Player_audio.player_item_audio(self)
        UniversalVariables.interaction_delay = 0
        return True

    @staticmethod
    def add_object_from_inv(item, amount=1):
        if item in Inventory.inventory:
            # Kui ese on juba inventoris, suurendab eseme kogust
            Inventory.inventory[item] += amount

        elif Inventory.total_slots > len(Inventory.inventory):
            # Kui tegemist on uue esemega, lisab selle inventori ja annab talle koguse: amount
            Inventory.inventory[item] = amount

        else: return

    @staticmethod
    def remove_object_from_inv(item):
        if Inventory.inventory[item] > 0 :
            Inventory.inventory[item] -= 1
        
        if Inventory.inventory[item] == 0:
            del Inventory.inventory[item]

            
    def render_boxes():
        if (UniversalVariables.render_boxes_counter % 2) != 0:
            ObjectManagement.render_interaction_box()
            ObjectManagement.render_collision_box()


    def render_collision_box() -> None:
        for box_item in UniversalVariables.collision_boxes:
            item_start_x, item_start_y  = box_item[0], box_item[1]
            item_width, item_height = box_item[2], box_item[3]
            obj_collision_box = pygame.Rect(item_start_x, item_start_y, item_width, item_height)
            collision_box_color = 'green'
            pygame.draw.rect(UniversalVariables.screen, collision_box_color, obj_collision_box, 3)


    def render_interaction_box() -> None:
        # terrain_x, terrain_y, object_width, object_height, object_image, object_id
        for box_item in UniversalVariables.object_list:
            outline_thickness = 3
            if box_item[5] in [981, 982]:
                outline_thickness = 8
            
            item_start_x, item_start_y  = box_item[0], box_item[1]
            item_width, item_height = box_item[2], box_item[3]
            obj_collision_box = pygame.Rect(item_start_x, item_start_y, item_width, item_height)
            collision_box_color = 'pink'
            pygame.draw.rect(UniversalVariables.screen, collision_box_color, obj_collision_box, outline_thickness, 5)
