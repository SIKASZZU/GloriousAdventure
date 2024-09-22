import pygame
from items import items_list
from inventory import Inventory
from variables import UniversalVariables
from audio import Player_audio
from text import Fading_text
import numpy as np

class ObjectManagement:

    def remove_object_at_position(self, terrain_x: int, terrain_y: int,
                                  object_id: int = None) -> None:
        """ Itemeid ei saa ülesse võtta enne
        kui need on lisatud mineralide listi """

        # Kui object ID ei ole siis jätab vahele, errorite vältimiseks
        if object_id is None:
            return

        else:
            for item in items_list:
                item_name = item.get("Name")

                if object_id == item["ID"]:
                    if item["Breakable"] != True:
                        return

                    if UniversalVariables.interaction_delay < UniversalVariables.interaction_delay_max:
                        if UniversalVariables.debug_mode:
                            print("Don't pick up so fast:", UniversalVariables.interaction_delay, "<", UniversalVariables.interaction_delay_max)
                        return

                    choice = None
                    amount = 1

                    if "Drops" in item:
                        choice = item["Drops"][0]
                        item_name = np.random.choice(choice, p=item["Drops"][1])
                        amount = item["Drops"][2]

                        choice_len = len(choice)
                        for item in choice:
                            if item in Inventory.inventory:
                                choice_len -= 1

                        if Inventory.total_slots >= len(Inventory.inventory) + choice_len:
                            ObjectManagement.update_terrain_and_add_item(self, terrain_x, terrain_y, object_id, item_name, amount)
                            return

                        else:
                            Inventory.inventory_full_error(self)
                            return

                    if Inventory.total_slots > len(Inventory.inventory) or item_name in Inventory.inventory:
                        ObjectManagement.update_terrain_and_add_item(self, terrain_x, terrain_y, object_id, item_name, amount)
                        return

                    else:
                        Inventory.inventory_full_error(self)
                        return

    def update_terrain_and_add_item(self, terrain_x: int, terrain_y: int, object_id: int, item_name: str, amount: int) -> bool:
        grid_col: int = int(terrain_x // UniversalVariables.block_size)
        grid_row: int = int(terrain_y // UniversalVariables.block_size)

        try:
            # Kontrollib kas jääb mapi sissse
            if 0 <= grid_row < len(self.terrain_data) and 0 <= grid_col < len(self.terrain_data[0]):

                terrain_update = {
                    4: 5,  # Oak tree stump
                    10: 98,  # Empty key slot
                    12: 98,  # Empty key slot
                    13: 98,  # Empty key slot
                    7: 107,  # Farmland
                    1008: 1009,  # Berry bush - Large
                    1010: 1011,  # Berry bush - Medium
                    1012: 1013,  # Berry bush - Small
                    
                }
                self.terrain_data[grid_row][grid_col] = terrain_update.get(object_id, 1)  # Default to Ground

                ObjectManagement.add_object_from_inv(item_name, amount)
                Player_audio.player_item_audio(self)
                UniversalVariables.interaction_delay = 0
                return

            else:
                return

        except Exception:
            return

    def add_object_from_inv(item, amount=1):
        if item in Inventory.inventory:
            # Kui ese on juba inventoris, suurendab eseme kogust
            Inventory.inventory[item] += amount

        elif Inventory.total_slots > len(Inventory.inventory):
            # Kui tegemist on uue esemega, lisab selle inventori ja annab talle koguse: amount
            Inventory.inventory[item] = amount

        else: return


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
        ### TODO: hetkel renderib isegi non-breakalbe objekt itemitle selle rooosa ruudu ymber
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
