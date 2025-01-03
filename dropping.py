import pygame
import math


class Drop:
    def __init__(self, player_update, inv, image_loader, o_managment, variables):
        self.player_update = player_update
        self.inv = inv
        self.image_loader = image_loader
        self.object_management = o_managment
        self.variables = variables
            
        # Animatsiooniga seotud asjad
        self.pouch_hitboxes = {}
        self.floating_angles = {}  # Track'ib iga pouchi positsiooni
        self.floating_distance = 3  # Max distance float'imiseks ülesse ja alla  # Default 3
        self.floating_speed = 4  # Animatsiooni kiirus  # Default 4

        # Pildiga seotud asjad
        self.pouch_image = self.image_loader.load_image("Pouch", 'images/Items/Objects/Pouch.png')
        self.half_block_size = self.variables.block_size // 4
        self.pouch_image = pygame.transform.scale(self.pouch_image, (self.half_block_size, self.half_block_size))
        self.pouch_half_width, self.pouch_half_height = self.pouch_image.get_width() // 2, self.pouch_image.get_height() // 2

        # Pouch UI properties
        self.total_slots = 6
        self.pouch_slots = (2, 3)
        self.pouch_offset = (10, 10)  # Offset Pouch'i sisu jaoks
        self.slot_size = (50, 50)  # width, height

        # Interaction variables
        self.click_position = None  # Et saaks vaadata, kas click'id Pouch'i hitbox'i peale -> window click -> x, y
        self.pouch_position = None  # Coord ilma offsetita -> x, y
        self.show_pouch = True  # Pouch state -> on / off
        self.drop_range = self.variables.block_size * .8

        # Click delay variables
        self.toggle_cooldown = 200  # 1000 -> 1 sek
        self.last_toggle_time = 0  # Timestamp viimasest toggle'imisest

        # Drop
        self.drop_delay_max = 15
        self.drop_delay = self.drop_delay_max

    def find_location(self) -> tuple[int, int]:  # Coord ilma offsetita
        if self.variables.dropped_items:
            for position, contents in self.variables.dropped_items.items():
                pouch_x, pouch_y = position
                player_x_minus_offset, player_y_minus_offset = self.variables.player_x, self.variables.player_y

                distance = math.sqrt((player_x_minus_offset - pouch_x) ** 2 + (player_y_minus_offset - pouch_y) ** 2)
                # Vaatab kas player ulatub Pouch'ini

                if distance < self.drop_range:
                    return position

        player_position = self.player_update.player_rect.center
        player_x, player_y = \
            player_position[0] - self.variables.offset_x - self.pouch_half_width, \
            player_position[1] - self.variables.offset_y - self.pouch_half_height

        return player_x, player_y

    def drop_items(self, position: tuple, item: str, quantity: int):
        # Use `add_item_to_existing_position` instead of directly setting dropped_items
        self.add_item_to_existing_position(position, item, quantity)

    def add_item_to_existing_position(self, position: tuple, item: str, quantity: int) -> None:
        # Initialize the position with an empty dict if not already present
        if position not in self.variables.dropped_items:
            self.variables.dropped_items[position] = {}

        # Add the item or update quantity and timer if it already exists
        if item not in self.variables.dropped_items[position]:
            self.variables.dropped_items[position][item] = {
                "quantity": quantity,
                "timer": self.variables.despawn_timer_default
            }
        else:
            self.variables.dropped_items[position][item]["quantity"] += quantity
            self.variables.dropped_items[position][item]["timer"] = self.variables.despawn_timer_default

    def open_pouch(self, position: tuple[int, int]) -> None:
        if not self.show_pouch:
            return

        if self.pouch_position:
            player_x_minus_offset = self.variables.player_x
            player_y_minus_offset = self.variables.player_y

            # Playeri kaugus Pouch'i click'i positsioonist
            distance = math.sqrt((player_x_minus_offset - self.pouch_position[0]) ** 2 + (player_y_minus_offset - self.pouch_position[1]) ** 2)

            # Vaatab kas player ulatub Pouch'ini
            if distance > self.drop_range:
                self.close_pouch()
                return False

            if position in self.variables.dropped_items:
                contents = self.variables.dropped_items[position]
                self.display_pouch_contents(contents)
                return True

        self.close_pouch()
        return False

    def display_pouch_contents(self, contents: dict) -> list:
        # Calculate the UI position and dimensions based on the item count
        current_slot_count = len(contents)
        pouch_y = 25
        pouch_x = (self.variables.screen_x // 2) - (current_slot_count * self.slot_size[0]) // 2
        pouch_width = current_slot_count * self.slot_size[0] + 10
        pouch_height = self.slot_size[1] + 10

        # Create a dedicated surface for the pouch contents
        pouch_surface = pygame.Surface((pouch_width, pouch_height), pygame.SRCALPHA)

        # Draw background and border on the pouch surface
        pygame.draw.rect(pouch_surface, (200, 200, 200, 150), (5, 5, pouch_width - 10, pouch_height - 10),
                         border_radius=3)
        pygame.draw.rect(pouch_surface, (0, 0, 0), (5, 5, pouch_width - 10, pouch_height - 10), 2, border_radius=3)

        # Define padding and slot size for items within the pouch
        padding = 3
        adjusted_slot_size = (self.slot_size[0] - 2 * padding, self.slot_size[1] - 2 * padding)

        # List to hold slot hitboxes for item interaction
        slot_hitboxes = []

        # Process each item for display in the pouch
        slot_index = 0
        for item_name, item_data in contents.items():
            original_image = self.image_loader.load_image(item_name)
            if original_image is None:
                continue  # Skip if image not found

            # Create a copy of the image specifically for the pouch to adjust transparency
            item_image = original_image.copy()
            item_quantity = item_data["quantity"]
            item_timer = item_data.get("timer", 0)  # Retrieve the timer for this item

            # Calculate transparency based on the despawn timer
            max_transparency = 255
            min_transparency = 100
            despawn_timer_default = self.variables.despawn_timer_default

            # Ratio for transparency
            transparency_ratio = max(0, min(1, item_timer / despawn_timer_default))
            transparency = int(min_transparency + (max_transparency - min_transparency) * transparency_ratio)
            item_image.set_alpha(transparency)  # Apply transparency to the copied image

            # Calculate position within the pouch surface
            slot_position = (slot_index * self.slot_size[0] + padding + 5, padding + 5)

            # Resize and blit item image to pouch surface
            item_image = pygame.transform.scale(item_image, adjusted_slot_size)
            pouch_surface.blit(item_image, slot_position)

            # Display quantity as text in top-left corner of each slot
            font = pygame.font.Font(None, 24)
            quantity_surface = font.render(str(item_quantity), True, (0, 0, 0))
            pouch_surface.blit(quantity_surface, (slot_position[0] + 2, slot_position[1] + 2))

            # Create and store the hitbox for interaction
            slot_rect = pygame.Rect(pouch_x + slot_position[0], pouch_y + slot_position[1], self.slot_size[0],
                                    self.slot_size[1])
            slot_hitboxes.append((slot_rect, item_name))

            slot_index += 1

        # Render the pouch display surface to the main screen without affecting inventory
        self.variables.screen.blit(pouch_surface, (pouch_x, pouch_y))

        return slot_hitboxes

    def remove_item_from_pouch(self, position: tuple[int, int], name: str) -> None:
        # Check if the position exists in dropped_items
        # TODO: Reset timer to default
        if self.inv.total_slots > len(self.inv.inventory) or name in self.inv.inventory:
            if position in self.variables.dropped_items:
                item_data = self.variables.dropped_items[position].get(name)

                if item_data:
                    # Kui hoiad shifti siis võtab kõik itemid
                    amount = 1 if not pygame.key.get_mods() & pygame.KMOD_SHIFT else item_data["quantity"]

                    # Decrement the quantity
                    item_data["quantity"] -= amount
                    self.object_management.add_object_from_inv(name, amount)

                    # If quantity reaches zero, remove the item from the dictionary
                    if item_data["quantity"] <= 0:
                        del self.variables.dropped_items[position][name]

                        # If no items left at this position, remove the position from the dictionary
                        if not self.variables.dropped_items[position]:  # Check if the dict is empty
                            del self.variables.dropped_items[position]
                            del self.pouch_hitboxes[position]
                            self.close_pouch()
                            return

                    # Resetib timeri ja transparency kui võtad itemi invist ära
                    item_data["timer"] = item_data["timer"] + 200
                    if item_data["timer"] > self.variables.despawn_timer_default:
                        item_data["timer"] = self.variables.despawn_timer_default
        else:
            self.inv.inventory_full_error(self)
            return


    def close_pouch(self) -> None:
        self.click_position = None
        self.pouch_position = None
        self.show_pouch = False

    def update_timers(self):
        self.drop_delay += 1
        for position, items in list(self.variables.dropped_items.items()):
            for item_name, item_data in list(items.items()):
                if item_data["timer"] > 0:
                    item_data["timer"] -= 1
                if item_data["timer"] <= 0:
                    del items[item_name]

            # Remove the position entry if no items are left
            if not items:
                del self.variables.dropped_items[position]
                del self.pouch_hitboxes[position]
                if position == self.pouch_position:
                    self.close_pouch()

    def display_floating_pouch(self, position: tuple[int, int]) -> None:
        """Displays the floating pouch at the specified position."""

        ### TODO: Resizeida vaja!! Kui block_size muutub siis pouch jääb samaks mis enne :(

        if position not in self.floating_angles:
            self.floating_angles[position] = 0

        base_position = (position[0] + self.variables.offset_x, position[1] + self.variables.offset_y)
        angle = self.floating_angles[position]
        float_offset = int(self.floating_distance * math.sin(math.radians(angle)))
        float_position = (base_position[0], base_position[1] + float_offset)

        # Display pouch image at the calculated floating position
        self.variables.screen.blit(self.pouch_image, float_position)

        # Update hitbox in the pouch hitboxes dictionary for position
        pouch_width, pouch_height = self.pouch_image.get_size()
        self.pouch_hitboxes[position] = pygame.Rect(float_position, (pouch_width, pouch_height))

        # Update the angle for floating animation
        self.floating_angles[position] = (angle + self.floating_speed) % 360

    def display_all_floating_pouch_hitboxes(self) -> None:
        for position, original_hitbox in self.pouch_hitboxes.items():
            pygame.draw.rect(self.variables.screen, 'pink', original_hitbox, 3, 5)

    def toggle_pouch(self, mouse_pos=None):
        if not mouse_pos:
            return False  # Kas Toggle's või mitte

        current_time = pygame.time.get_ticks()

        if current_time - self.last_toggle_time < self.toggle_cooldown:
            return False  # Kas Toggle's või mitte

        # Vaatab jas ckuck on pouch'i hitboxi'i sees
        for position, hitbox in self.pouch_hitboxes.items():
            if hitbox.collidepoint(mouse_pos):

                # Sulgeb Pouch'i kui clickid samasse hitbox'i
                if self.show_pouch and self.pouch_position == position:
                    self.close_pouch()
                    self.show_pouch = False

                else:
                    self.pouch_position = position
                    self.show_pouch = True  # Avab pouch

                self.last_toggle_time = current_time
                return True  # Kas Toggle's või mitte

        return False  # Kas Toggle's või mitte

    def update(self, item: str = None, quantity: int = None):
       # Lisab item'id invi, mida ei saa otse lisada, circular error asi
        if self.variables.items_to_drop:
            items_to_remove = []

            for item, quantity in self.variables.items_to_drop.items():
                # Otsib õige Pouch'i
                position = self.find_location()
                self.drop_items(position, item, quantity)

                # Viin ühest listist asjad teise listi -> Circular errori pärast
                self.variables.items_to_drop[item] = 0
                items_to_remove.append(item)

            # Listi loopimise ajal ei saa samat listi muuta
            for item in items_to_remove:
                del self.variables.items_to_drop[item]

        self.update_timers()

        # Check if there are dropped items and display the pouch
        if self.variables.dropped_items:
            # Iterate over a copy of dropped_items to avoid modification errors
            for position, contents in list(self.variables.dropped_items.items()):  # Create a list copy

                # Display the floating pouch
                self.display_floating_pouch(position)

                # Open the pouch if it's the current position
                if self.show_pouch and self.pouch_position == position:
                    # Call display_pouch_contents and get the hitboxes
                    slot_hitboxes = self.display_pouch_contents(contents)

                    # Check for right-clicks on item slots
                    mouse_pos = pygame.mouse.get_pos()
                    if pygame.mouse.get_pressed()[2]:  # Right-click

                        for slot_rect, item_name in slot_hitboxes:
                            if slot_rect.collidepoint(mouse_pos):

                                if self.drop_delay >= self.drop_delay_max:
                                    self.remove_item_from_pouch(self.pouch_position, item_name)
                                    self.drop_delay = 0
                                    break

            # Handle pouch toggling with right-click
            if pygame.mouse.get_pressed()[2] and not self.variables.cooking_menu:  # Right-click
                mouse_position = pygame.mouse.get_pos()
                self.toggle_pouch(mouse_position)
