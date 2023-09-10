import pygame
from items import minerals


# x, y, ID
def remove_object_at_position(
        self, terrain_x: int, terrain_y: int,
        object_id: int = None

) -> None:

    # Kui object ID ei ole siis jätab vahele, errorite vältimiseks
    if object_id is not None:
        grid_col: int = int(terrain_x // self.block_size)
        grid_row: int = int(terrain_y // self.block_size)

        # Kontrollib kas jääb mapi sissse
        if 0 <= grid_row < len(self.terrain_data) and 0 <= grid_col < len(self.terrain_data[0]):
            if object_id == 4:
                grid_col += 1
                grid_row += 1

            # Muudab objecti value 1 - tuleb ümber muuta kui hakkame biomeid tegema vms
            # näiteks liiva peal kaktus, tuleks muuta liivaks mitte muruks
            self.terrain_data[grid_row][grid_col] = 1

        # Kui ei jää mapi sisse siis prindib errori
        else:
            print("Error in file: objects.py\nInvalid grid indices:", grid_row, grid_col)


# ID, hitboxi list, näiteks (160, 240, 50, 130, 4, 80, 40)
# 160 - X
# 240 - U
# 50  - hitboxi laius
# 130 - hitboxi pikkus
# 4   - objecti ID
# 80  - hitboxi offset x
# 40  - hitboxi offset y
def add_object_to_inv(
        self, object_id: int,
        obj_hit_box: tuple[int, ...]  # Tuple kus on ainult integer'id

) -> None:

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

    except RuntimeError as e:
        print('Error in file: objects.py', e)


# ID, pilt, x, y, laius, pikkus
def place_and_render_object(
        self, object_id: int, obj_image,
        object_x: int, object_y: int,
        object_width: int, object_height: int

) -> None:

    # Kui pilt on olemas siis võimaldab seda
    # ülesse võtta ja visualiseerib seda
    if obj_image:

        # Kui OBJECT ID on 4, võtab antud x ja y
        if object_id == 4:
            position: tuple = (object_x, object_y)
            object_rect = pygame.Rect(object_x, object_y, self.block_size * 2, self.block_size * 2)

        else:
            object_rect = pygame.Rect(object_x, object_y, self.block_size, self.block_size)

        # Muudab pildi suurust ja visualiseerib seda
        scaled_obj_image = pygame.transform.scale(obj_image, (object_width, object_height))
        self.screen.blit(scaled_obj_image, position)

        # Teeb roosa outline objecti ümber
        pygame.draw.rect(self.screen, 'pink', object_rect, 2)


# ID, x, y, laius, pikkus
def place_and_render_hitbox(
        self, object_id: int,
        hit_box_x: int, hit_box_y: int,
        hit_box_width: int, hit_box_height: int

) -> None:

    hit_box_color: str = 'green'

    # Teeb antud asjadest hitboxi ja visualiseerib seda
    obj_hit_box = pygame.Rect(hit_box_x, hit_box_y, hit_box_width, hit_box_height)
    pygame.draw.rect(self.screen, hit_box_color, obj_hit_box, 2)
