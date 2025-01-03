import pygame

from items import object_items, mineral_items, tool_items, ObjectItem, MineralItem, ToolItem


def craftable_items_manager(func):
    def wrapper(self, *args, **kwargs):
        self.calculate_craftable_items()
        func(self, *args, **kwargs)

    return wrapper


class Inventory:
    def __init__(self, camera, player_update, image_loader, fading_text, variables):
        self.camera = camera
        self.player_update = player_update
        self.image_loader = image_loader
        self.fading_text = fading_text
        self.variables = variables

        self.slot_image = self.image_loader.load_gui_image("Selected_Item_Inventory")
        self.position = (self.variables.screen_x // 2 - 170, self.variables.screen_y - 51)
        self.resized_slot_image = pygame.transform.scale(self.slot_image, (
        self.slot_image.get_width() * 0.9, self.slot_image.get_height() * 0.9))

        self.inventory_display_rects = []
        self.craftable_items_display_rects = []

        self.inventory = {}  # Terve inv (prindi seda ja saad teada mis invis on)
        self.old_inventory = {}  # track varasemat inv white texti jaoks
        self.inv_count: int = 0  # Otsustab, kas renderida inv v6i mitte
        self.white_text = False
        self.white_colored_items = set()
        self.white_text_counters = {}

        self.render_inv: bool = False  # Inventory renderminmine
        self.tab_pressed: bool = False  # Keep track of whether Tab was pressed
        self.crafting_menu_open: bool = False
        self.check_slot_delay: int = 0
        self.craftable_items = {}

        self.previous_inv = None  # printimise jaoks
        self.text_cache = {}  # Cache rendered text surfaces
        self.message_to_user = False
        self.first_time_click = False
        self.total_slots: int = 2

        self.total_rows = 0
        self.total_cols = 0
        self.old_x = 500

        self.previous_inventory = None  # Track the previous state of the inventory

    def print_inventory(self) -> None:
        """ Prints out the contents of the inventory."""

        if self.inventory != self.previous_inv:
            print('Inventory contains:\n   ', self.inventory)
            self.previous_inv = self.inventory.copy()

    def handle_mouse_click(self) -> None:
        """ Lubab invis ja craftimises clicke kasutada
        ja lisab ka viite CHECK_DELAY_THRESHOLD  """

        CHECK_DELAY_THRESHOLD = 200  # Threshold slotide clickimiseks
        if (self.inv_count % 2) != 0 or self.crafting_menu_open:
            mouse_state: tuple[bool, bool, bool] = pygame.mouse.get_pressed()
            if mouse_state[0] or mouse_state[2]:  # Left click ja right click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                current_time = pygame.time.get_ticks()

                if current_time - self.check_slot_delay >= CHECK_DELAY_THRESHOLD:
                    self.check_slot_delay = current_time  # Uuendab viimast check_slot_delay

                    if self.crafting_menu_open:
                        self.handle_crafting_click(mouse_x, mouse_y)

                    self.is_click_in_inventory(mouse_x, mouse_y, mouse_state)

    def is_click_in_inventory(self, mouse_x, mouse_y, mouse_state):
        """ Kas click on invi sees ja siis displayb itemi nime mida invis klikkis"""

        # Vaatab kas click oli invis sees või mitte
        for index, rect in enumerate(self.inventory_display_rects):
            if rect.collidepoint(mouse_x, mouse_y):
                self.check_slot(index, mouse_state[2])
                try:
                    item = list(self.inventory.keys())[index]
                    item = str(item).replace('_', ' ')
                    self.fading_text.re_display_fading_text(item)

                except Exception:
                    pass
                return

        return

    def handle_crafting_click(self, x: int, y: int) -> None:
        """ Lubab hiit kasutades craftida """
        try:
            for name, rect in self.craftable_items_display_rects.items():
                if not rect.collidepoint(x, y):
                    continue

                if name not in self.inventory and self.total_slots <= len(self.inventory):
                    self.player_audio.error_audio(self)
                    self.fading_text.re_display_fading_text("Not enough space in Inventory.")
                    return

                crafted_item = self.craft_item(name)  # Pass 'self' and 'name'

        except AttributeError:
            return

    def check_slot(self, index: int, delete_boolean=False) -> None:
        """Checks what's in the inventory's selected slot."""

        try:
            if not delete_boolean:
                item = list(self.inventory.keys())[index]
                value = list(self.inventory.values())[index]
                self.variables.current_equipped_item = item

            else:
                item = list(self.inventory.keys())[index]
                value = list(self.inventory.values())[index]

                # Kui hoiad Shift'i all siis drop'id max amount'i
                amount = 1 if not pygame.key.get_mods() & pygame.KMOD_SHIFT else self.inventory[item]

                self.inventory[item] -= amount

                # Võtab itemi invist ära kui on <= 0
                if self.inventory[item] <= 0:
                    del self.inventory[item]
                    self.variables.current_equipped_item = None

                # Lisab itemi `Floating Pouch`i
                if item in self.variables.items_to_drop:
                    self.variables.items_to_drop[item] += amount
                else:
                    self.variables.items_to_drop[item] = amount

                self.fading_text.display_once_fading_text("Left unattended, items will fade into whispers of the wind.")


        except IndexError as IE:
            print(IE)
            self.variables.current_equipped_item = None

    def call(self) -> None:
        """ Inventory kutsumiseks on see func. """

        if len(self.inventory.items()) != 0 and not self.message_to_user and not self.first_time_click:
            self.variables.ui_elements.append(
                """ Press TAB to open inventory. """)
            self.message_to_user = True

        self.handle_mouse_click()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_TAB] and not self.tab_pressed:  # double locked, yks alati true aga teine mitte
            self.tab_pressed = True
            self.inv_count += 1

            if not self.first_time_click:
                self.first_time_click = True
                self.variables.ui_elements.append('Select items with left click. Remove items with right click.')

            self.render_inv = (self.inv_count % 2 != 0)
            self.variables.cooking_menu = False

        elif not keys[pygame.K_TAB]:
            self.tab_pressed = False

        if self.render_inv:
            # self.variables.allow_movement = False
            self.render()  # Render inventory
            self.variables.allow_building = False
        else:
            # self.variables.allow_movement = True
            self.render(update_white_text=True)  # Kui sulgeb invi white text itemitega, ss j2rgmine kord ei ole neid itemid enam valged
            self.variables.allow_building = True

    # TODO : invi on vaja optimatiseerida
    def calculate(self, calc_slots_only=False) -> None:
        """ Arvutab invetory suuruse, asukoha
        vastavalt playeri asukohale """

        if self.variables.maze_counter <= 5:
            self.total_rows = self.variables.maze_counter + 1 if self.variables.maze_counter < 5 else self.variables.maze_counter
            self.total_cols = 3 if self.variables.maze_counter == 5 else 2

        if self.variables.maze_counter <= 5:
            self.total_rows = self.variables.maze_counter + 1
            if self.total_rows > 5:
                self.total_rows = 5

            if self.variables.maze_counter == 5:
                self.total_cols = 3
            else:
                self.total_cols = 2

        total_rows = self.total_rows
        total_cols = self.total_cols

        self.total_slots = total_rows * total_cols

        if calc_slots_only:
            return

        if not self.old_x:
            self.old_x = self.variables.player_x

        if self.old_x == self.variables.player_x:
            return

        self.inventory_display_rects = []
        rect_width: int = self.variables.block_size / 2
        rect_height: int = self.variables.block_size / 2

        # Calculate inventory position relative to player and screen size
        rect_x: int = self.player_update.player_rect.centerx + total_cols + self.variables.block_size / 2  # Siia ei tohi offsetti panna
        rect_y: int = self.player_update.player_rect.centery - total_rows * self.variables.block_size / 4  # Siia ei tohi offsetti panna

        right_side: int = self.variables.screen.get_size()[0] - (
                self.camera.camera_borders['left'] * 2) + self.variables.block_size * 0.6
        left_side: int = self.camera.camera_borders['left'] * 2

        if rect_x >= right_side:
            rect_x = self.variables.player_x - self.variables.block_size * total_cols / 2 + self.variables.offset_x
        elif rect_x >= left_side:
            rect_x = self.variables.player_x + self.variables.block_size * 2 / 2 + self.variables.offset_x

        # Create inventory rectangles
        for rows in range(total_rows):
            for cols in range(total_cols):
                rect = pygame.Rect(rect_x + cols * rect_width, rect_y + rows * rect_height, rect_width, rect_height)
                self.inventory_display_rects.append(rect)

    def render(self, update_white_text=None) -> None:
        """ Callib calculate_inventory, renderib invi, invis olevad itemid ja nende kogused """

        # Clear the white text items and counters if rendering inventory is false
        if update_white_text:
            self.white_colored_items.clear()
            self.white_text_counters.clear()
            return

        self.calculate()

        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.variables.screen.get_width(), self.variables.screen.get_height()),
                                 pygame.SRCALPHA)
        overlay.set_alpha(180)

        # Draw item slots with borders
        for rect in self.inventory_display_rects:
            pygame.draw.rect(overlay, (177, 177, 177), rect, border_radius=5)  # Gray background
            pygame.draw.rect(overlay, 'black', rect, 2, border_radius=5)  # Black border

        # Blit the overlay onto the screen
        self.variables.screen.blit(overlay, (0, 0))

        new_white_items = set()
        for rect, (name, count) in zip(self.inventory_display_rects, self.inventory.items()):
            item_rect = pygame.Rect(rect.x + 3, rect.y + 3, rect.width - 6, rect.height - 6)

            if count < 0:
                continue

            item_image = self.image_loader.load_image(name)
            if not item_image:
                continue

            item_image = pygame.transform.scale(item_image, (int(rect.width / 1.4), int(rect.height / 1.4)))
            item_image_rect = item_image.get_rect(center=item_rect.center)

            font = pygame.font.Font(None, 20)

            # Check if the item is new or its count has changed
            if (name not in self.old_inventory or
                    (name in self.old_inventory and self.inventory[name] != self.old_inventory[name])):
                self.white_text = True
                new_white_items.add(name)
                self.white_text_counters[name] = 0  # Initialize the counter for the new item

            text_color = 'black'
            if name in self.white_colored_items:
                text_color = 'white'  # color for item change
                self.white_text_counters[name] += 1  # Increment the counter for the item

            text = font.render(str(count), True, text_color)
            text_rect = text.get_rect(center=(rect.x + 10, rect.y + 10))

            blit_operations = [(item_image, item_image_rect.topleft), (text, text_rect.topleft)]
            self.variables.screen.blits(blit_operations, False)

        items_to_remove = [item for item, counter in self.white_text_counters.items() if counter >= 120]
        for item in items_to_remove:
            self.white_colored_items.remove(item)
            del self.white_text_counters[item]

        self.white_colored_items.update(new_white_items)
        self.old_inventory = self.inventory.copy()

    def has_inventory_changed(self) -> bool:
        """Check if the inventory has changed since the last calculation."""
        current_inventory = self.inventory

        # If previous_inventory is None, it means we haven't calculated yet
        if self.previous_inventory is None:
            self.previous_inventory = current_inventory.copy()
            return True  # Recalculate on first run

        # Check if the current inventory is different from the previous one
        if current_inventory != self.previous_inventory:
            self.previous_inventory = current_inventory.copy()
            return True

        return False

    def calculate_craftable_items(self):
        """Otsib kõik itemid ülesse, mida saab craftida vastavalt invile."""

        # Check if inventory has changed before recalculating
        if not self.has_inventory_changed():
            return  # Skip calculation if inventory has not changed

        self.craftable_items = {}

        for item_list in [object_items, mineral_items, tool_items]:
            for item in item_list:
                recipes = item.recipe if isinstance(item, (ObjectItem, MineralItem, ToolItem)) else None

                if not recipes:
                    continue

                # Iterate through the recipes
                for recipe in recipes:
                    required_items = recipe.get("Recipe", {})

                    # Check if all required items are available
                    can_craft = all(
                        self.inventory.get(required_item, 0) >= required_amount
                        for required_item, required_amount in required_items.items()
                    )

                    if can_craft:
                        # Use dot notation to access item attributes
                        self.craftable_items[item.name] = recipe.get("Amount",
                                                                         1)  # Use item.name instead of item["Name"]

        self.update_craftable_items_display()

    def update_craftable_items_display(self):
        """Update the display for craftable items."""

        self.craftable_items_display_rects = {}

        rect_width: float = self.variables.block_size / 2
        rect_height: float = self.variables.block_size / 2
        max_cols: int = 3  # Max columns in a row

        # Calculate inventory item positions based on player location and inventory settings
        rect_x: int = 50
        rect_y: int = 50

        craftable_items = list(self.craftable_items.keys())  # Extract craftable item names

        for index, craftable_item in enumerate(craftable_items):
            rows = index // max_cols
            cols = index % max_cols

            # Create a rectangle for displaying the craftable item
            rect = pygame.Rect(rect_x + cols * rect_width, rect_y + rows * rect_height, rect_width, rect_height)
            self.craftable_items_display_rects[craftable_item] = rect

    @craftable_items_manager
    def render_craftable_items(self):
        """ Render craftable items and respond to clicks """

        # Exit function if there are no craftable items
        if not self.craftable_items_display_rects:
            return

        screen_width = self.variables.screen.get_width()
        screen_height = self.variables.screen.get_height()

        # Create a semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.set_alpha(180)  # Set overlay transparency

        # Prepare the font once
        font = pygame.font.Font(None, 20)

        # Pre-load images and resize them
        resized_images = {}
        for name, rect in self.craftable_items_display_rects.items():
            object_image = self.image_loader.load_image(name)
            if object_image is not None:
                object_image = pygame.transform.scale(object_image, (int(rect.width / 1.4), int(rect.height / 1.4)))
                resized_images[name] = object_image

        # Prepare the list of blit operations
        blit_operations = []

        # Draw the background and items on the overlay
        for name, rect in self.craftable_items_display_rects.items():
            pygame.draw.rect(overlay, (177, 177, 177), rect)  # Draw semi-transparent background
            pygame.draw.rect(overlay, 'black', rect, 2)  # Draw black border

            item_rect = pygame.Rect(rect.x + 3, rect.y + 3, rect.width - 6, rect.height - 6)
            pygame.draw.rect(overlay, (0, 0, 0, 180), item_rect)  # Draw item background

            # Blit the pre-loaded and resized image
            if name in resized_images:
                object_image = resized_images[name]
                item_image_rect = object_image.get_rect(center=item_rect.center)
                blit_operations.append((object_image, item_image_rect.topleft))

            # Render the amount of craftable items
            text = font.render(str(self.craftable_items[name]), True, 'Black')
            text_rect = text.get_rect(center=(rect.x + 10, rect.y + 10))
            blit_operations.append((text, text_rect))

        # Perform all blit operations at once
        overlay.blits(blit_operations)

        # Blit the overlay to the screen once
        self.variables.screen.blit(overlay, (0, 0))

    def craft_item(self, name):
        """Craft an item and update the inventory."""
        # Get the crafted item from the lists
        crafted_item = next((item for item_list in [object_items, mineral_items, tool_items] for item in item_list if
                             item.name == name), None)

        if crafted_item:
            recipes = crafted_item.recipe if hasattr(crafted_item, 'recipe') else []
            amount = 0

            # Iterate through each recipe
            for recipe in recipes:
                required_items = recipe.get("Recipe", {})
                can_craft = all(
                    self.inventory.get(required_item, 0) >= required_amount
                    for required_item, required_amount in required_items.items()
                )

                if can_craft:
                    # Remove used items from the inventory
                    for required_item, required_amount in required_items.items():
                        self.inventory[required_item] -= required_amount

                    # Calculate the amount crafted based on the recipe
                    amount += recipe.get("Amount", 1)

            # Add the crafted item to the inventory
            self.inventory[name] = self.inventory.get(name, 0) + amount

            # Remove items with a count of zero from the inventory
            self.inventory = {k: v for k, v in self.inventory.items() if v > 0}

    def render_equipped_slot(self, name):
        # Initialize blit operations list
        blit_operations = [(self.resized_slot_image, self.position)]

        # Check if the item name is valid
        if name is None or name not in self.inventory:
            self.variables.screen.blits(blit_operations)
            self.variables.current_equipped_item = None
            return

        # Load and resize item image
        item_image = self.image_loader.load_image(name)
        slot_width, slot_height = self.resized_slot_image.get_size()
        max_item_size = (slot_width - 15, slot_height - 15)
        resized_item_image = pygame.transform.scale(item_image, max_item_size)

        # Calculate position to center item image within the slot
        item_x = self.position[0] + (slot_width - resized_item_image.get_width()) // 2
        item_y = self.position[1] + (slot_height - resized_item_image.get_height()) // 2

        # Add item image to blit operations
        blit_operations.append((resized_item_image, (item_x, item_y)))

        # Render item count if greater than 1
        item_count = self.inventory.get(name, 0)
        if item_count > 1:
            count_text = str(item_count)
            if count_text not in self.text_cache:
                font = pygame.font.Font(None, 20)
                self.text_cache[count_text] = font.render(count_text, True, (0, 0, 0))

            text_surface = self.text_cache[count_text]
            text_rect = text_surface.get_rect(topleft=(self.position[0] + 5, self.position[1] + 5))
            blit_operations.append((text_surface, text_rect.topleft))

        # Perform all blit operations
        self.variables.screen.blits(blit_operations)

        # Call item delay bar rendering function
        self.item_delay_bar(self.resized_slot_image, self.position)

    def item_delay_bar(self, slot_image, position):
        """ See func on inventory all, sest slot_image andmed asuvad siin ja eksportimine on keerukas. """

        width = slot_image.get_width()
        height = slot_image.get_height()

        # Tekitab semi-transparent recti
        overlay = pygame.Surface((self.variables.screen.get_width(), self.variables.screen.get_height()),
                                 pygame.SRCALPHA)
        overlay.set_alpha(100)

        if self.variables.interaction_delay < self.variables.interaction_delay_max:
            tl_point = position[0]
            tr_point = position[1]

            progress = int((self.variables.interaction_delay / self.variables.interaction_delay_max) * height)

            loading_bar_border_rect = pygame.Rect(tl_point, tr_point + progress, width, height - progress, )
            pygame.draw.rect(overlay, 'black', loading_bar_border_rect)
            self.variables.screen.blit(overlay, (0, 0))

    def inventory_full_error(self):
        # Player_audio.error_audio(self)
        self.fading_text.re_display_fading_text("Not enough space in Inventory.")
        self.variables.interaction_delay = 0
