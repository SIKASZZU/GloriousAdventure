import pygame
from items import minerals

# eemaldab objekti ning lisab selle inventory
def remove_object_at_position(self, terrain_x, terrain_y, object_id=None):
    # itemi eemaldamine visuaalselt, asendamine terraini valuga (1)
    grid_col = terrain_x // self.block_size
    grid_row = terrain_y // self.block_size

    if 0 <= grid_row < len(self.terrain_data) and 0 <= grid_col < len(self.terrain_data[0]):
        grid_col = int(terrain_x //self.block_size)
        grid_row = int(terrain_y //self.block_size)

        if object_id == 4: 
            grid_col += 1
            grid_row += 1

        self.terrain_data[grid_row][grid_col] = 1
    else:
        print("Invalid grid indices:", grid_row, grid_col)


def add_object_to_inv(self, object_id, obj_hit_box):
        
    items_found = set()  # Hoiab leitud esemed
    item_count = {}  # Hoiab leitud esemete arve

    # itemi lisamine playeri inventorisse
    for item_name, item_values in minerals.items():
        if object_id == item_values[2]:
            print(object_id, item_values[2])
            items_found.add(item_name)
            try:
                for item_name in items_found:
                    item_count[item_name] = 0  # Resetib itemi koguse kuna muidu fkupiks...

                    for item_name, item_values in minerals.items():
                        if object_id == item_values[2] and item_name in items_found:
                            item_count[item_name] += 1
                            items_found.remove(item_name)  # Eemaldab eseme leitud hulgast

                            # Lisab eseme inventuuri dicti
                            if item_name in self.inventory:
                                self.inventory[item_name] += 1
                            else:
                                self.inventory[item_name] = 1

                            index = self.hit_boxes.index(obj_hit_box)
                            self.hit_boxes.pop(index)    

            except RuntimeError:
                print('RuntimeError')

def place_and_render_object(self, object_id, obj_image, obj_x, obj_y, obj_width, obj_height):
    if obj_image:
        if object_id == 4: position =  (obj_x - self.block_size / 2, obj_y - self.block_size)
        scaled_obj_image = pygame.transform.scale(obj_image, (obj_width, obj_height))
        self.screen.blit(scaled_obj_image, position)

def place_and_render_hitbox(self, object_id, hit_box_x, hit_box_y, hit_box_width, hit_box_height):
    if object_id == 4:
        hit_box_x = hit_box_x - self.block_size / 2
        hit_box_y = hit_box_y - self.block_size    
    hit_box_color = 'Green'
    obj_hit_box = pygame.Rect(hit_box_x, hit_box_y, hit_box_width, hit_box_height)
    pygame.draw.rect(self.screen, hit_box_color, obj_hit_box, 2)