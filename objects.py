import pygame
from items import items_list
from images import ImageLoader
from inventory import Inventory
from variables import UniversalVariables

class ObjectManagement:

    def remove_object_at_position(self, terrain_x: int, terrain_y: int,
                                  object_id: int = None) -> None:
        """ Itemeid ei saa ülesse võtta enne
        kui need on lisatud mineralide listi """

        # Kui object ID ei ole siis jätab vahele, errorite vältimiseks
        if object_id is not None:
            for item in items_list:
                item_name = item.get("Name")

                if object_id == item["ID"]:
                    if item["Breakable"] != True:
                        return
                    else:
                        if Inventory.total_slots > len(Inventory.inventory) or item_name in Inventory.inventory:

                            grid_col: int = int(terrain_x // UniversalVariables.block_size)
                            grid_row: int = int(terrain_y // UniversalVariables.block_size)

                            try:
                                # Kontrollib kas jääb mapi sissse
                                if 0 <= grid_row < len(self.terrain_data) and 0 <= grid_col < len(self.terrain_data[0]):


                                    # Muudab objecti väärtuse 1 - tuleb ümber muuta kui hakkame biomeid tegema vms
                                    # näiteks liiva peal kaktus, tuleks muuta liivaks mitte muruks
                                    if object_id == 10:
                                        self.terrain_data[grid_row][grid_col] = 11

                                    elif object_id == 7:
                                        self.terrain_data[grid_row][grid_col] = 107

                                    else:
                                        position: tuple = (terrain_x, terrain_y)
                                        self.terrain_data[grid_row][grid_col] = 1

                                    ObjectManagement.add_object_to_inv(self, object_id)

                                else:
                                    print("Invalid grid indices:", grid_row,
                                          grid_col)  # Kui ei jää mapi sisse siis prindib errori

                            except Exception as e:
                                print("IndexError: objects.py, remove_object_at_position", e)

                        else:
                            text = "Not enough space in Inventory."
                            UniversalVariables.ui_elements.append(text)

                            if text in self.shown_texts:
                                self.shown_texts.remove(text)

    # ID, hitboxi list, näiteks (160, 240, 50, 130, 4, 80, 40)
    # 160 - X
    # 240 - Y
    # 50  - hitboxi laius
    # 130 - hitboxi pikkus
    # 4   - objecti ID
    # 80  - hitboxi offset x
    # 40  - hitboxi offset y
                            
    def add_object_to_inv(self, object_id: int) -> None:
        # Hoiab leitud esemeid: test_found = ["test0", "test1", "test2"]
        items_found: set[str] = set()
        # Hoiab leitud esemeid koos kogusega: test_count = {"Test0": 2, "Test1": 4, "Test2": 6}
        item_count: dict[str, int] = {}

        # itemi lisamine playeri inventorisse
        for item_data in items_list:
            if object_id == item_data["ID"]:
                items_found.add(item_data["Name"])

        # Copy, et vältida erroreid, mis tulenevad suuruse muutumisega
        # Hoiab leitud esemeid: test_found_copy = ["test0", "test1", "test2"]
        items_found_copy: set[str] = items_found.copy()

        try:
            for item_name in items_found_copy:
                item_count[item_name] = 0

                for item_data in items_list:
                    if object_id == item_data["ID"] and item_data["Name"] in items_found:
                        item_count[item_data["Name"]] += 1
                        items_found.remove(item_data["Name"])

                        # Uuenda mängija inventori
                        if item_data["Name"] in Inventory.inventory:
                            # Kui ese on juba inventoris, suurendab eseme kogust
                            Inventory.inventory[item_data["Name"]] += 1
                        else:
                            # Kui tegemist on uue esemega, lisab selle inventori ja annab talle koguse: 1
                            Inventory.inventory[item_data["Name"]] = 1

        except RuntimeError as e:
            print("\nError in file: objects.py, add_object_to_inv", e)

    # temporary add func?
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
