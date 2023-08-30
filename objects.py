from items import minerals
import pygame


def get_object_id_at_position(self, x, y):
    terrain_x = x - self.offset_x
    terrain_y = y - self.offset_y
    grid_col = terrain_x // self.block_size
    grid_row = terrain_y // self.block_size
    return self.terrain_data[grid_row][grid_col]

# eemaldab objekti ning lisab selle inventory
def remove_object_at_position(self, x, y, terrain_x, terrain_y, obj_hit_box, object_id=None):
    items_found = set()  # Hoiab leitud esemed
    item_count = {}  # Hoiab leitud esemete arve
    
    # itemi eemaldamine visuaalselt
    grid_col = terrain_x // self.block_size
    grid_row = terrain_y // self.block_size

    if 0 <= grid_row < len(self.terrain_data) and 0 <= grid_col < len(self.terrain_data[0]):
        grid_col = int(terrain_x //self.block_size)
        grid_row = int(terrain_y //self.block_size)

        if object_id == 4: 
            grid_col += 1
            grid_row += 1
        self.terrain_data[grid_row][grid_col] = 1

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

                        self.grab_decay = 0        
        except RuntimeError:
            print('RuntimeError')

    else:
        print("Invalid grid indices:", grid_row, grid_col)

    index = self.hit_boxes.index(obj_hit_box)
    self.hit_boxes.pop(index)

def place_and_render_object(self, object_id, obj_image, obj_x, obj_y,
                                obj_width, obj_height, hit_box_color,
                                hit_box_x, hit_box_y, hit_box_width, hit_box_height):
    if obj_image:
        # Kui mineral on puu siis annab eraldi koordinaadid
        if object_id == 4:
            # Render object image
            scaled_obj_image = pygame.transform.scale(obj_image, (obj_width, obj_height))
            self.screen.blit(scaled_obj_image, (obj_x - self.block_size / 2, obj_y - self.block_size))

            # Draw hit box
            obj_hit_box = pygame.Rect(hit_box_x - self.block_size / 2, hit_box_y - self.block_size, hit_box_width, hit_box_height)
            pygame.draw.rect(self.screen, hit_box_color, obj_hit_box, 2)

        else:
            # Render object image
            scaled_obj_image = pygame.transform.scale(obj_image, (obj_width, obj_height))
            self.screen.blit(scaled_obj_image, (obj_x, obj_y))

            # Draw hit box
            obj_hit_box = pygame.Rect(hit_box_x, hit_box_y, hit_box_width, hit_box_height)
            pygame.draw.rect(self.screen, hit_box_color, obj_hit_box, 2)