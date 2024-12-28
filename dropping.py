from variables import UniversalVariables
from images import ImageLoader
import pygame
import math
from inventory import Inventory
from objects import ObjectManagement

class Drop:
    # Animatsiooniga seotud asjad
    pouch_hitboxes = {}
    floating_angles = {}  # Track'ib iga pouchi positsiooni
    floating_distance = 3  # Max distance float'imiseks ülesse ja alla  # Default 3
    floating_speed = 4  # Animatsiooni kiirus  # Default 4

    # Pildiga seotud asjad
    pouch_image = ImageLoader.load_image("Pouch", 'images/Items/Objects/Pouch.png')
    half_block_size = UniversalVariables.block_size // 4
    pouch_image = pygame.transform.scale(pouch_image, (half_block_size, half_block_size))
    pouch_half_width, pouch_half_height = pouch_image.get_width() // 2, pouch_image.get_height() // 2

    # Pouch UI properties
    total_slots = 6
    pouch_slots = (2, 3)
    pouch_offset = (10, 10)  # Offset Pouch'i sisu jaoks
    slot_size = (50, 50)  # width, height

    # Interaction variables
    click_position = None  # Et saaks vaadata, kas click'id Pouch'i hitbox'i peale -> window click -> x, y
    pouch_position = None  # Coord ilma offsetita -> x, y
    show_pouch = True  # Pouch state -> on / off
    drop_range = UniversalVariables.block_size * .8

    # Click delay variables
    toggle_cooldown = 200  # 1000 -> 1 sek
    last_toggle_time = 0  # Timestamp viimasest toggle'imisest

    # Drop
    drop_delay_max = 15
    drop_delay = drop_delay_max

    def find_location(self) -> tuple[int, int]:  # Coord ilma offsetita
        if UniversalVariables.dropped_items:
            for position, contents in UniversalVariables.dropped_items.items():
                pouch_x, pouch_y = position
                player_x_minus_offset, player_y_minus_offset = UniversalVariables.player_x, UniversalVariables.player_y

                distance = math.sqrt((player_x_minus_offset - pouch_x) ** 2 + (player_y_minus_offset - pouch_y) ** 2)
                # Vaatab kas player ulatub Pouch'ini

                if distance < Drop.drop_range:
                    return position

        player_position = self.player_rect.center
        player_x, player_y = \
            player_position[0] - UniversalVariables.offset_x - Drop.pouch_half_width, \
            player_position[1] - UniversalVariables.offset_y - Drop.pouch_half_height

        return player_x, player_y

    @staticmethod
    def drop_items(position: tuple, item: str, quantity: int):
        # Use `add_item_to_existing_position` instead of directly setting dropped_items
        Drop.add_item_to_existing_position(position, item, quantity)

    @staticmethod
    def add_item_to_existing_position(position: tuple, item: str, quantity: int) -> None:
        # Initialize the position with an empty dict if not already present
        if position not in UniversalVariables.dropped_items:
            UniversalVariables.dropped_items[position] = {}

        # Add the item or update quantity and timer if it already exists
        if item not in UniversalVariables.dropped_items[position]:
            UniversalVariables.dropped_items[position][item] = {
                "quantity": quantity,
                "timer": UniversalVariables.despawn_timer_default
            }
        else:
            UniversalVariables.dropped_items[position][item]["quantity"] += quantity
            UniversalVariables.dropped_items[position][item]["timer"] = UniversalVariables.despawn_timer_default

    @staticmethod
    def open_pouch(position: tuple[int, int]) -> None:
        if not Drop.show_pouch:
            return

        if Drop.pouch_position:
            player_x_minus_offset = UniversalVariables.player_x
            player_y_minus_offset = UniversalVariables.player_y

            # Playeri kaugus Pouch'i click'i positsioonist
            distance = math.sqrt((player_x_minus_offset - Drop.pouch_position[0]) ** 2 + (player_y_minus_offset - Drop.pouch_position[1]) ** 2)

            # Vaatab kas player ulatub Pouch'ini
            if distance > Drop.drop_range:
                Drop.close_pouch()
                return False

            if position in UniversalVariables.dropped_items:
                contents = UniversalVariables.dropped_items[position]
                Drop.display_pouch_contents(contents)
                return True

        Drop.close_pouch()
        return False

    @staticmethod
    def display_pouch_contents(contents: dict) -> list:
        # Calculate the UI position and dimensions based on the item count
        current_slot_count = len(contents)
        pouch_y = 25
        pouch_x = (UniversalVariables.screen_x // 2) - (current_slot_count * Drop.slot_size[0]) // 2
        pouch_width = current_slot_count * Drop.slot_size[0] + 10
        pouch_height = Drop.slot_size[1] + 10

        # Create a dedicated surface for the pouch contents
        pouch_surface = pygame.Surface((pouch_width, pouch_height), pygame.SRCALPHA)

        # Draw background and border on the pouch surface
        pygame.draw.rect(pouch_surface, (200, 200, 200, 150), (5, 5, pouch_width - 10, pouch_height - 10),
                         border_radius=3)
        pygame.draw.rect(pouch_surface, (0, 0, 0), (5, 5, pouch_width - 10, pouch_height - 10), 2, border_radius=3)

        # Define padding and slot size for items within the pouch
        padding = 3
        adjusted_slot_size = (Drop.slot_size[0] - 2 * padding, Drop.slot_size[1] - 2 * padding)

        # List to hold slot hitboxes for item interaction
        slot_hitboxes = []

        # Process each item for display in the pouch
        slot_index = 0
        for item_name, item_data in contents.items():
            original_image = ImageLoader.load_image(item_name)
            if original_image is None:
                continue  # Skip if image not found

            # Create a copy of the image specifically for the pouch to adjust transparency
            item_image = original_image.copy()
            item_quantity = item_data["quantity"]
            item_timer = item_data.get("timer", 0)  # Retrieve the timer for this item

            # Calculate transparency based on the despawn timer
            max_transparency = 255
            min_transparency = 100
            despawn_timer_default = UniversalVariables.despawn_timer_default

            # Ratio for transparency
            transparency_ratio = max(0, min(1, item_timer / despawn_timer_default))
            transparency = int(min_transparency + (max_transparency - min_transparency) * transparency_ratio)
            item_image.set_alpha(transparency)  # Apply transparency to the copied image

            # Calculate position within the pouch surface
            slot_position = (slot_index * Drop.slot_size[0] + padding + 5, padding + 5)

            # Resize and blit item image to pouch surface
            item_image = pygame.transform.scale(item_image, adjusted_slot_size)
            pouch_surface.blit(item_image, slot_position)

            # Display quantity as text in top-left corner of each slot
            font = pygame.font.Font(None, 24)
            quantity_surface = font.render(str(item_quantity), True, (0, 0, 0))
            pouch_surface.blit(quantity_surface, (slot_position[0] + 2, slot_position[1] + 2))

            # Create and store the hitbox for interaction
            slot_rect = pygame.Rect(pouch_x + slot_position[0], pouch_y + slot_position[1], Drop.slot_size[0],
                                    Drop.slot_size[1])
            slot_hitboxes.append((slot_rect, item_name))

            slot_index += 1

        # Render the pouch display surface to the main screen without affecting inventory
        UniversalVariables.screen.blit(pouch_surface, (pouch_x, pouch_y))

        return slot_hitboxes

    def remove_item_from_pouch(self, position: tuple[int, int], name: str) -> None:
        # Check if the position exists in dropped_items
        # TODO: Reset timer to default
        if Inventory.total_slots > len(Inventory.inventory) or name in Inventory.inventory:
            if position in UniversalVariables.dropped_items:
                item_data = UniversalVariables.dropped_items[position].get(name)

                if item_data:
                    # Kui hoiad shifti siis võtab kõik itemid
                    amount = 1 if not pygame.key.get_mods() & pygame.KMOD_SHIFT else item_data["quantity"]

                    # Decrement the quantity
                    item_data["quantity"] -= amount
                    ObjectManagement.add_object_from_inv(name, amount)

                    # If quantity reaches zero, remove the item from the dictionary
                    if item_data["quantity"] <= 0:
                        del UniversalVariables.dropped_items[position][name]

                        # If no items left at this position, remove the position from the dictionary
                        if not UniversalVariables.dropped_items[position]:  # Check if the dict is empty
                            del UniversalVariables.dropped_items[position]
                            del Drop.pouch_hitboxes[position]
                            Drop.close_pouch()
                            return

                    # Resetib timeri ja transparency kui võtad itemi invist ära
                    item_data["timer"] = item_data["timer"] + 200
                    if item_data["timer"] > UniversalVariables.despawn_timer_default:
                        item_data["timer"] = UniversalVariables.despawn_timer_default
        else:
            Inventory.inventory_full_error(self)
            return


    @staticmethod
    def close_pouch() -> None:
        Drop.click_position = None
        Drop.pouch_position = None
        Drop.show_pouch = False

    @staticmethod
    def update_timers():
        Drop.drop_delay += 1
        for position, items in list(UniversalVariables.dropped_items.items()):
            for item_name, item_data in list(items.items()):
                if item_data["timer"] > 0:
                    item_data["timer"] -= 1
                if item_data["timer"] <= 0:
                    del items[item_name]

            # Remove the position entry if no items are left
            if not items:
                del UniversalVariables.dropped_items[position]
                del Drop.pouch_hitboxes[position]
                if position == Drop.pouch_position:
                    Drop.close_pouch()

    @staticmethod
    def display_floating_pouch(position: tuple[int, int]) -> None:
        """Displays the floating pouch at the specified position."""
        if position not in Drop.floating_angles:
            Drop.floating_angles[position] = 0

        base_position = (position[0] + UniversalVariables.offset_x, position[1] + UniversalVariables.offset_y)
        angle = Drop.floating_angles[position]
        float_offset = int(Drop.floating_distance * math.sin(math.radians(angle)))
        float_position = (base_position[0], base_position[1] + float_offset)

        # Display pouch image at the calculated floating position
        UniversalVariables.screen.blit(Drop.pouch_image, float_position)

        # Update hitbox in the pouch hitboxes dictionary for position
        pouch_width, pouch_height = Drop.pouch_image.get_size()
        Drop.pouch_hitboxes[position] = pygame.Rect(float_position, (pouch_width, pouch_height))

        # Update the angle for floating animation
        Drop.floating_angles[position] = (angle + Drop.floating_speed) % 360

    @staticmethod
    def display_all_floating_pouch_hitboxes() -> None:
        for position, original_hitbox in Drop.pouch_hitboxes.items():
            pygame.draw.rect(UniversalVariables.screen, 'pink', original_hitbox, 3, 5)

    @staticmethod
    def toggle_pouch(mouse_pos=None):
        if not mouse_pos:
            return False  # Kas Toggle's või mitte

        current_time = pygame.time.get_ticks()

        if current_time - Drop.last_toggle_time < Drop.toggle_cooldown:
            return False  # Kas Toggle's või mitte

        # Vaatab jas ckuck on pouch'i hitboxi'i sees
        for position, hitbox in Drop.pouch_hitboxes.items():
            if hitbox.collidepoint(mouse_pos):

                # Sulgeb Pouch'i kui clickid samasse hitbox'i
                if Drop.show_pouch and Drop.pouch_position == position:
                    Drop.close_pouch()
                    Drop.show_pouch = False

                else:
                    Drop.pouch_position = position
                    Drop.show_pouch = True  # Avab pouch

                Drop.last_toggle_time = current_time
                return True  # Kas Toggle's või mitte

        return False  # Kas Toggle's või mitte

    def update(self, item: str = None, quantity: int = None):
       # Lisab item'id invi, mida ei saa otse lisada, circular error asi
        if UniversalVariables.items_to_drop:
            items_to_remove = []

            for item, quantity in UniversalVariables.items_to_drop.items():
                # Otsib õige Pouch'i
                position = Drop.find_location(self)
                Drop.drop_items(position, item, quantity)

                # Viin ühest listist asjad teise listi -> Circular errori pärast
                UniversalVariables.items_to_drop[item] = 0
                items_to_remove.append(item)

            # Listi loopimise ajal ei saa samat listi muuta
            for item in items_to_remove:
                del UniversalVariables.items_to_drop[item]

        Drop.update_timers()

        # Kui on dropped item'eid siis display'b Pouch'i
        if UniversalVariables.dropped_items:
            # Check if there are dropped items and display the pouch
            if UniversalVariables.dropped_items:
                # Iterate over a copy of dropped_items to avoid modification errors
                for position, contents in list(UniversalVariables.dropped_items.items()):  # Create a list copy

                    # Display the floating pouch
                    Drop.display_floating_pouch(position)

                    # Open the pouch if it's the current position
                    if Drop.show_pouch and Drop.pouch_position == position:
                        # Call display_pouch_contents and get the hitboxes
                        slot_hitboxes = Drop.display_pouch_contents(contents)

                        # Check for right-clicks on item slots
                        mouse_pos = pygame.mouse.get_pos()
                        if pygame.mouse.get_pressed()[2]:  # Right-click

                            for slot_rect, item_name in slot_hitboxes:
                                if slot_rect.collidepoint(mouse_pos):

                                    if Drop.drop_delay >= Drop.drop_delay_max:
                                        Drop.remove_item_from_pouch(self, Drop.pouch_position, item_name)
                                        Drop.drop_delay = 0
                                        break

            # Handle pouch toggling with right-click
            if pygame.mouse.get_pressed()[2] and not UniversalVariables.cooking_menu:  # Right-click
                mouse_position = pygame.mouse.get_pos()
                Drop.toggle_pouch(mouse_position)
