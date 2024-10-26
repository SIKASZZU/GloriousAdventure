from variables import UniversalVariables
from images import ImageLoader
import pygame
import math
from camera import Camera
from text import Fading_text

class Drop:
    # Animatsiooniga seotud asjad
    pouch_hitboxes = {}
    floating_angles = {}  # Track'ib iga pouchi positsiooni
    floating_distance = 5  # Max distance float'imiseks ülesse ja alla
    floating_speed = 4  # Animatsiooni kiirus

    # Pildiga seotud asjad
    pouch_image = ImageLoader.load_image("Pouch", 'images\Items\Objects\Pouch.png')
    half_block_size = UniversalVariables.block_size // 4
    pouch_image = pygame.transform.scale(pouch_image, (half_block_size, half_block_size))
    pouch_half_width, pouch_half_height = pouch_image.get_width() // 2, pouch_image.get_height() // 2

    # Pouch UI properties
    total_slots = 6
    pouch_slots = (2, 3)
    slot_size = (50, 50)  # width, height
    pouch_offset = (10, 10)  # Offset Pouch'i sisu jaoks

    # Interaction variables
    click_position = None  # Et saaks vaadata, kas click'id Pouch'i hitbox'i peale -> window click -> x, y
    pouch_position = None  # Coord ilma offsetita -> x, y
    show_pouch = True  # Pouch state -> on / off
    drop_range = UniversalVariables.block_size * .5

    # Click delay variables
    toggle_cooldown = 200  # 1000 -> 1 sek
    last_toggle_time = 0  # Timestamp viimasest toggle'imisest

    def find_location(self) -> tuple[int, int]:  # Coord ilma offsetita
        # Otsib vanat pouchi player_range seest. Kui pouch on full,
        # Otsib koha kuhu saab pouchi panna.
        # 100 playeri vaate suunas --> last input 's' siis dropib seda y + 100
        # Rect teha 0st, transparent, 2x5 ja locked inv ja dropped items ss






        if UniversalVariables.dropped_items:
            for position, _ in UniversalVariables.dropped_items.items():
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
        if position in UniversalVariables.dropped_items:
            contents = UniversalVariables.dropped_items[position]
            Drop.display_pouch_contents(contents)


    # TODO: slotid tiba transparent ja iga itemile eraldi transparentcy, kui item hakkab kaduma selle transparency langeb
    @staticmethod
    def display_pouch_contents(contents: dict) -> None:
        # Calculate the UI position and dimensions based on the item count
        current_slot_count = len(contents)
        pouch_y = 25
        pouch_x = (UniversalVariables.screen_x // 2) - (current_slot_count * Drop.slot_size[0]) // 2
        pouch_width = current_slot_count * Drop.slot_size[0] + 10
        pouch_height = Drop.slot_size[1] + 10

        # Create a transparent surface with the pouch dimensions
        pouch_surface = pygame.Surface((pouch_width, pouch_height), pygame.SRCALPHA)
        pouch_surface.fill((0, 0, 0, 0))  # Fully transparent background

        # Draw the transparent background and black border on the pouch surface
        pygame.draw.rect(pouch_surface, (200, 200, 200, 150),
                         (5, 5, pouch_width - 10, pouch_height - 10))  # Light gray, semi-transparent background
        pygame.draw.rect(pouch_surface, (0, 0, 0), (5, 5, pouch_width - 10, pouch_height - 10), 2)  # Black border

        # Define padding and adjusted slot size for items
        padding = 3
        adjusted_slot_size = (Drop.slot_size[0] - 2 * padding, Drop.slot_size[1] - 2 * padding)

        # Blit each item in a horizontal row
        slot_index = 0
        for item_name, item_data in contents.items():
            item_image = ImageLoader.load_image(item_name)
            item_quantity = item_data["quantity"]

            # Calculate item position within the pouch surface
            slot_position = (slot_index * Drop.slot_size[0] + padding + 5, padding + 5)

            # Resize the image to fit within the slot and blit to the pouch surface
            item_image = pygame.transform.scale(item_image, adjusted_slot_size)
            pouch_surface.blit(item_image, slot_position)

            # Display item quantity at the top-left corner of the item slot
            font = pygame.font.Font(None, 24)
            quantity_surface = font.render(str(item_quantity), True, (0, 0, 0))
            pouch_surface.blit(quantity_surface, (slot_position[0] + 2, slot_position[1] + 2))

            slot_index += 1  # Move to the next slot

        # Blit the completed pouch surface with transparency to the main screen
        UniversalVariables.screen.blit(pouch_surface, (pouch_x, pouch_y))

    @staticmethod
    def check_for_right_click(mouse_pos: tuple[int, int]) -> None:
        if Drop.pouch_position:
            player_x_minus_offset = UniversalVariables.player_x
            player_y_minus_offset = UniversalVariables.player_y

            # Playeri kaugus Pouch'i click'i positsioonist
            distance = math.sqrt((player_x_minus_offset - Drop.pouch_position[0]) ** 2 + (player_y_minus_offset - Drop.pouch_position[1]) ** 2)

            # Vaatab kas player ulatub Pouch'ini
            if distance > Drop.drop_range:
                Drop.close_pouch()
                return

            # Kui Pouch on playeri range'is, avab Pouch'i
            Drop.open_pouch(Drop.pouch_position)
            return

        Drop.close_pouch()
        return

    @staticmethod
    def close_pouch() -> None:
        Drop.click_position = None
        Drop.pouch_position = None
        Drop.show_pouch = False

    @staticmethod
    def update_timers():
        # Decrease timer for each item, remove if timer reaches 0
        for position, items in list(UniversalVariables.dropped_items.items()):
            for item_name, item_data in list(items.items()):
                if item_data["timer"] > 0:
                    item_data["timer"] -= 1
                if item_data["timer"] <= 0:
                    del items[item_name]

            # Remove the position entry if no items are left
            if not items:
                del UniversalVariables.dropped_items[position]
                if position == Drop.pouch_position:
                    Drop.close_pouch()

    @staticmethod
    def display_floating_pouch(position: tuple[int, int]) -> None:
        if position not in Drop.floating_angles:
            Drop.floating_angles[position] = 0

        base_position = (position[0] + UniversalVariables.offset_x, position[1] + UniversalVariables.offset_y)
        angle = Drop.floating_angles[position]
        float_offset = int(Drop.floating_distance * math.sin(math.radians(angle)))
        float_position = (base_position[0], base_position[1] + float_offset)

        UniversalVariables.screen.blit(Drop.pouch_image, float_position)
        Drop.pouch_hitboxes[position] = pygame.Rect(float_position, Drop.pouch_image.get_size())
        Drop.floating_angles[position] = (angle + Drop.floating_speed) % 360

    @staticmethod
    def toggle_pouch(mouse_pos=None):
        current_time = pygame.time.get_ticks()  # Hetkene aeg millisekundites
        if current_time - Drop.last_toggle_time >= Drop.toggle_cooldown:
            Drop.show_pouch = not Drop.show_pouch  # Toggle pouch state
            Drop.last_toggle_time = current_time  # Update the last toggle time

            if Drop.show_pouch:
                Drop.click_position = mouse_pos  # Record position when opened

                for position, hitbox in Drop.pouch_hitboxes.items():
                    if hitbox.collidepoint(mouse_pos):
                        Drop.pouch_position = position
                        break

            else:
                Drop.close_pouch()

    def update(self, item: str = None, quantity: int = None):
        if item and quantity:
            position = Drop.find_location(self)
            Drop.drop_items(position, item, quantity)

        Drop.update_timers()

        # Kui on dropped item'eid siis display'b Pouch'i
        if UniversalVariables.dropped_items:
            for position, _ in UniversalVariables.dropped_items.items():
                Drop.display_floating_pouch(position)

        # Pouchi avamine
        if pygame.mouse.get_pressed()[2]:  # Right-click
            mouse_position = pygame.mouse.get_pos()
            Drop.toggle_pouch(mouse_position)

        if Drop.show_pouch and Drop.click_position:
            Drop.check_for_right_click(Drop.click_position)
































        # Test drops
        # Drop.drop_items((17, 18), 'Bread', 6)
        # Drop.drop_items((17, 18), 'Glowstick', 6)
        # Drop.drop_items((17, 18), 'Pizza', 6)
        # Drop.drop_items((114, 18), 'Soda', 6)
        #
        # for position, items in UniversalVariables.dropped_items.items():
        #     print()
        #     print(f"\nPosition: {position} \nItems: {items}")
        #     # for item, quantity in items.items():
        #     #     print(f"Item: {item}, Quantity: {quantity}")

