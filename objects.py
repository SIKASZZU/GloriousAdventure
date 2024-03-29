import pygame
from items import items_list
from images import ImageLoader
from inventory import Inventory
from variables import UniversalVariables


class ObjectManagement:

    hitbox_count: int = 0

    def remove_object_at_position(self, terrain_x: int, terrain_y: int, obj_collision_box: tuple[int, ...],
                                  object_id: int = None) -> None:
        """ Itemeid ei saa ülesse võtta enne
        kui need on lisatud mineralide listi """

        # Kui object ID ei ole siis jätab vahele, errorite vältimiseks
        if object_id is not None:
            for item_data in items_list:
                if object_id == item_data["ID"]:
                    if item_data["Breakable"] != True:
                        pass
                    else:
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
                                    self.terrain_data[grid_row][grid_col] = 1


                                ObjectManagement.add_object_to_inv(self, object_id, obj_collision_box)

                            else:
                                print("Invalid grid indices:", grid_row,
                                      grid_col)  # Kui ei jää mapi sisse siis prindib errori

                        except Exception as e:
                            print("IndexError: objects.py, remove_object_at_position", e)

    # ID, hitboxi list, näiteks (160, 240, 50, 130, 4, 80, 40)
    # 160 - X
    # 240 - Y
    # 50  - hitboxi laius
    # 130 - hitboxi pikkus
    # 4   - objecti ID
    # 80  - hitboxi offset x
    # 40  - hitboxi offset y
                            
    def add_object_to_inv(self, object_id: int, obj_collision_box: tuple[int, ...]) -> None:
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

                        index = UniversalVariables.collision_boxes.index(obj_collision_box)
                        UniversalVariables.collision_boxes.pop(index)

        except RuntimeError as e:
            print("\nError in file: objects.py, add_object_to_inv", e)


    def remove_object_from_inv(item):
        if Inventory.inventory[item] > 0 :
            Inventory.inventory[item] -= 1
        
        if Inventory.inventory[item] == 0:
            print()
            print(Inventory.inventory)
            print(Inventory.inventory['Maze_Key'])
            del Inventory.inventory['Maze_Key']
            print(Inventory.inventory)


    def place_and_render_object(self) -> None:
        """ Visuaalselt paneb objekti maailma (image). """

        interaction_boxes = {}  # Object id, pilt, ja pildi suurus

        # Check if block size has changed
        if UniversalVariables.prev_block_size != UniversalVariables.block_size:
            # Update the previous block size
            UniversalVariables.prev_block_size = UniversalVariables.block_size

        for collision_box_x, collision_box_y, collision_box_width, collision_box_height, object_id, collision_box_offset_x, collision_box_offset_y in UniversalVariables.collision_boxes:
            terrain_x: int = (collision_box_x - collision_box_offset_x) + UniversalVariables.offset_x
            terrain_y: int = (collision_box_y - collision_box_offset_y) + UniversalVariables.offset_y
            object_image = None
            object_width = 0
            object_height = 0

            for item in items_list:
                if item.get("Type") == "Object" and item.get("ID") == object_id:
                    object_breakable = None
                    if item.get("Name") == "Maze_Wall": pass
                    else:
                        object_image_name = item.get("Name")
                        object_width = item.get("Object_width")
                        object_height = item.get("Object_height")
                        object_breakable = item.get("Breakable")

                        # Load the image

                        object_image = ImageLoader.load_image(object_image_name)

                        interaction_boxes[object_id] = (object_image, object_width, object_height)

            if object_image:
                position: tuple = (terrain_x, terrain_y)
                scaled_object_image = pygame.transform.scale(object_image, (
                    object_width * UniversalVariables.block_size / 109,
                    object_height * UniversalVariables.block_size / 109))
                UniversalVariables.screen.blit(scaled_object_image, position)

            else:
                pass

            object_rect = pygame.Rect(terrain_x, terrain_y, object_width * UniversalVariables.block_size / 109,
                                      object_height * UniversalVariables.block_size / 109)

            if (ObjectManagement.hitbox_count % 2) != 0:
                ObjectManagement.place_and_render_hitbox(self, collision_box_x, collision_box_y, collision_box_width,
                                                         collision_box_height)
                if object_breakable:
                    pygame.draw.rect(UniversalVariables.screen, 'pink', object_rect,
                                     1)  # Teeb roosa outline objecti ümber


    def place_and_render_hitbox(self, collision_box_x, collision_box_y, collision_box_width,
                                collision_box_height) -> None:
        """ Renderib hitboxi objektitele. """

        collision_box_color: str = 'green'
        collision_box_x += UniversalVariables.offset_x
        collision_box_y += UniversalVariables.offset_y

        # Teeb antud asjadest hitboxi ja visualiseerib seda
        obj_collision_box = pygame.Rect(collision_box_x, collision_box_y, collision_box_width, collision_box_height)
        pygame.draw.rect(UniversalVariables.screen, collision_box_color, obj_collision_box, 2)



