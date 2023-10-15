import pygame
from items import items_list
from images import ground_images, water_images, item_images
from inventory import Inventory

class Object_Management:
    
    hitbox_count: int = 0

    # x, y, ID
    def remove_object_at_position(self, terrain_x: int, terrain_y: int, obj_hit_box: tuple[int, ...], object_id: int = None) -> None:
        """ Itemeid ei saa ülesse võtta enne
        kui need on lisatud mineralide listi """

        # Kui object ID ei ole siis jätab vahele, errorite vältimiseks
        if object_id is not None:
            for item_data in items_list:
                if object_id == item_data["ID"]:
                    if item_data["Breakable"] != True: pass
                    else:
                        grid_col: int = int(terrain_x // self.block_size)
                        grid_row: int = int(terrain_y // self.block_size)

                        try:
                            # Kontrollib kas jääb mapi sissse
                            if 0 <= grid_row < len(self.terrain_data) and 0 <= grid_col < len(self.terrain_data[0]):
                            
                                # Muudab objecti väärtuse 1 - tuleb ümber muuta kui hakkame biomeid tegema vms
                                # näiteks liiva peal kaktus, tuleks muuta liivaks mitte muruks
                                if object_id == 7: self.terrain_data[grid_row][grid_col] = 107
                                else: self.terrain_data[grid_row][grid_col] = 1
                                Object_Management.add_object_to_inv(self, object_id, obj_hit_box)

                            else:
                                print("Invalid grid indices:", grid_row, grid_col)  # Kui ei jää mapi sisse siis prindib errori

                        except Exception as e:
                            print("IndexError: objects.py, remove_object_at_position", e)

    
    # ID, hitboxi list, näiteks (160, 240, 50, 130, 4, 80, 40)
    # 160 - X
    # 240 - U
    # 50  - hitboxi laius
    # 130 - hitboxi pikkus
    # 4   - objecti ID
    # 80  - hitboxi offset x
    # 40  - hitboxi offset y
    def add_object_to_inv(self, object_id: int, obj_hit_box: tuple[int, ...]) -> None:
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

                        index = self.hit_boxes.index(obj_hit_box)
                        self.hit_boxes.pop(index)

        except RuntimeError as e: print("\nError in file: objects.py, add_object_to_inv", e)


    def place_and_render_object(self) -> None:
        """ Visuaalselt paneb objekti maailma (image). """
        
        keys = pygame.key.get_pressed()

        interaction_boxes = {}  # Object id, pilt, ja pildi suurus

        for hit_box_x, hit_box_y, hit_box_width, hit_box_height, object_id, hit_box_offset_x, hit_box_offset_y in self.hit_boxes:
            object_image = None

            terrain_x: int = (hit_box_x - hit_box_offset_x) + self.offset_x
            terrain_y: int = (hit_box_y - hit_box_offset_y) + self.offset_y
            
            for item in items_list:
                if item.get("Type") == "Object" and item.get("ID") == object_id:
                    object_image = item_images.get(item.get("Name"))
                    object_width = item.get("Object_width")
                    object_height = item.get("Object_height")

                    interaction_boxes[object_id] = (object_image, object_width, object_height)

            if object_image:
                position: tuple = (terrain_x, terrain_y)
                scaled_object_image = pygame.transform.scale(object_image, (object_width, object_height))
                self.screen.blit(scaled_object_image, position)
            else: pass
            object_rect = pygame.Rect(terrain_x, terrain_y, object_width, object_height)

            # Kui vajutad "h" siis tulevad hitboxid visuaalselt nähtavale
            if keys[pygame.K_h] and not self.h_pressed:
                self.h_pressed = True
                Object_Management.hitbox_count += 1
            elif not keys[pygame.K_h]:
                self.h_pressed = False

            if (Object_Management.hitbox_count % 2) != 0:
                Object_Management.place_and_render_hitbox(self, hit_box_x, hit_box_y, hit_box_width, hit_box_height)
                pygame.draw.rect(self.screen, 'pink', object_rect, 1)  # Teeb roosa outline objecti ümber


    def place_and_render_hitbox(self, hit_box_x, hit_box_y, hit_box_width, hit_box_height) -> None:
        """ Renderib hitboxi objektitele. """

        hit_box_color: str = 'green'
        hit_box_x += self.offset_x
        hit_box_y += self.offset_y

        # Teeb antud asjadest hitboxi ja visualiseerib seda
        obj_hit_box = pygame.Rect(hit_box_x, hit_box_y, hit_box_width, hit_box_height)
        pygame.draw.rect(self.screen, hit_box_color, obj_hit_box, 2)



