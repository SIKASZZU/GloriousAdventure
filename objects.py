import pygame
from items import minerals
from images import ground_images, water_images, item_images

class Object_Management:
    # x, y, ID
    def remove_object_at_position(
            self, terrain_x: int, terrain_y: int, object_id: int = None
            ) -> None:

        """ Itemeid ei saa ülesse võtta enne
        kui need on lisatud mineralide listi """

        # Kui object ID ei ole siis jätab vahele, errorite vältimiseks
        if object_id is not None:
            grid_col: int = int(terrain_x // self.block_size)
            grid_row: int = int(terrain_y // self.block_size)

            try:
                # Kontrollib kas jääb mapi sissse
                if 0 <= grid_row < len(self.terrain_data) and 0 <= grid_col < len(self.terrain_data[0]):
                    if object_id == 4:
                        grid_col += 1
                        grid_row += 1

                    # Muudab objecti väärtuse 1 - tuleb ümber muuta kui hakkame biomeid tegema vms
                    # näiteks liiva peal kaktus, tuleks muuta liivaks mitte muruks
                    # self.terrain_data[grid_row][grid_col] = 1

                # Kui ei jää mapi sisse siis prindib errori
                else:
                    print("\nError in file: objects.py \n  Invalid grid indices:", grid_row, grid_col)

            except:
                print("IndexError: objects - remove_object_at_position", object_id)
    
    # ID, hitboxi list, näiteks (160, 240, 50, 130, 4, 80, 40)
    # 160 - X
    # 240 - U
    # 50  - hitboxi laius
    # 130 - hitboxi pikkus
    # 4   - objecti ID
    # 80  - hitboxi offset x
    # 40  - hitboxi offset y
    def add_object_to_inv(
            self, object_id: int, obj_hit_box: tuple[int, ...]
            ) -> None:  # Tuple kus on ainult integer'id
        print(object_id)
        # Hoiab leitud esemeid: test_found = ["test0", "test1", "test2"]
        items_found: set[str] = set()
        # Hoiab leitud esemeid koos kogusega: test_count = {["Test0": 2], ["Test1": 4], ["Test2": 6]}
        item_count: dict[str, int] = {}
    
        # itemi lisamine playeri inventorisse
        for item_name, item_values in minerals.items():
            if object_id == item_values[2]:
                print(object_id, item_values[2])
                items_found.add(item_name)
    
        # Copy, et vältida erroreid, mis tulenevad suuruse muutumisega
        # Hoiab leitud esemeid: test_found_copy = ["test0", "test1", "test2"]
        items_found_copy: set[str] = items_found.copy()
    
        try:
            for item_name in items_found_copy:
                item_count[item_name] = 0
    
                for item_name, item_values in minerals.items():
                    if object_id == item_values[2] and item_name in items_found:
                    
                        item_count[item_name] += 1
                        items_found.remove(item_name)
    
                        # Uuenda mängija inventori
                        if item_name in self.inventory:
                            # Kui ese on juba inventoris, suurendab eseme kogust
                            self.inventory[item_name] += 1
                        else:
                            # Kui tegemist on uue esemega, lisab selle inventori ja annab talle koguse: 1
                            self.inventory[item_name] = 1
    
                        index = self.hit_boxes.index(obj_hit_box)
                        self.hit_boxes.pop(index)
    
        except RuntimeError as e: print("\nError in file: objects.py", e)
    

    def place_and_render_object(self) -> None:
        """Visuaalselt paneb objekti maailma (image)"""
        for hit_box_x, hit_box_y, hit_box_width, hit_box_height, object_id, hit_box_offset_x, hit_box_offset_y in self.hit_boxes:
            obj_image = None
            
            terrain_x: int = (hit_box_x - hit_box_offset_x) + self.offset_x
            terrain_y: int = (hit_box_y - hit_box_offset_y) + self.offset_y

            # Object id, pilt, ja pildi suurus
            if object_id == 2:
                obj_image = item_images.get("Rock")
                object_width = int(self.block_size * 1)
                object_height = int(self.block_size * 0.8)

            elif object_id == 4:
                obj_image = item_images.get("Tree")
                object_width = int(self.block_size * 2)
                object_height = int(self.block_size * 2)

            elif object_id == 5:
                obj_image = item_images.get("Flower")
                object_width = int(self.block_size * 0.5)
                object_height = int(self.block_size * 0.5)

            elif object_id == 6:
                obj_image = item_images.get("Mushroom")
                object_width = int(self.block_size * 0.3)
                object_height = int(self.block_size * 0.3)

            else:
                object_width = int(self.block_size)
                object_height = int(self.block_size)

            if obj_image:
                position: tuple = (terrain_x, terrain_y)
                object_rect = pygame.Rect(terrain_x, terrain_y, object_width, object_height)
    
                # Muudab pildi suurust ja visualiseerib seda
                scaled_obj_image = pygame.transform.scale(obj_image, (object_width, object_height))
                self.screen.blit(scaled_obj_image, position)
    
                # Teeb roosa outline objecti ümber
                pygame.draw.rect(self.screen, 'pink', object_rect, 1)

            else: pass  # print('Object image missing!. File: objects.py Function: place_and_render_object')
            Object_Management.place_and_render_hitbox(self, hit_box_x, hit_box_y, hit_box_width, hit_box_height)
    

    def place_and_render_hitbox(self,
                                hit_box_x, hit_box_y,
                                hit_box_width, hit_box_height
                                ) -> None:
        """Renderib hitboxi objektitele"""

        hit_box_color: str = 'green'
        hit_box_x += self.offset_x
        hit_box_y += self.offset_y

        # Teeb antud asjadest hitboxi ja visualiseerib seda
        obj_hit_box = pygame.Rect(hit_box_x, hit_box_y, hit_box_width, hit_box_height)
        pygame.draw.rect(self.screen, hit_box_color, obj_hit_box, 2)
    
