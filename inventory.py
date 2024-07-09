import pygame

from images import ImageLoader, ImageCache
from camera import Camera
from variables import UniversalVariables
from items import items_list
from audio import Player_audio
from text import Fading_text

def craftable_items_manager(func):
    def wrapper(self, *args, **kwargs):
        Inventory.calculate_craftable_items(self)
        func(self, *args, **kwargs)
    return wrapper

class Inventory:

    inventory_display_rects = []
    craftable_items_display_rects = []

    inventory = {}  # Terve inv (prindi seda ja saad teada mis invis on)
    old_inventory = {}  # track varasemat inv white texti jaoks
    inv_count: int = 0  # Otsustab, kas renderida inv v6i mitte
    white_text = False
    white_colored_items = set()
    white_text_counters = {}

    render_inv: bool = False  # Inventory renderminmine
    tab_pressed: bool = False  # Keep track of whether Tab was pressed
    crafting_menu_open: bool = False
    check_slot_delay: int = 0
    craftable_items = {}

    previous_inv = None  # printimise jaoks
    text_cache = {}  # Cache rendered text surfaces
    message_to_user = False
    first_time_click = False
    total_slots:int = 4

    @staticmethod
    def print_inventory() -> None:
        """ Prints out the contents of the inventory."""

        if Inventory.inventory != Inventory.previous_inv:
            print('Inventory contains:\n   ', Inventory.inventory)
            Inventory.previous_inv = Inventory.inventory.copy()


    def handle_mouse_click(self) -> None:
        """ Lubab invis ja craftimises clicke kasutada
        ja lisab ka viite CHECK_DELAY_THRESHOLD  """
        CHECK_DELAY_THRESHOLD = 200  # Threshold slotide clickimiseks
        if (Inventory.inv_count % 2) != 0 or Inventory.crafting_menu_open:
            mouse_state: tuple[bool, bool, bool] = pygame.mouse.get_pressed()
            if mouse_state[0] or mouse_state[2]:  # Left click ja right click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                current_time = pygame.time.get_ticks()


                if current_time - Inventory.check_slot_delay >= CHECK_DELAY_THRESHOLD:
                    Inventory.check_slot_delay = current_time  # Uuendab viimast check_slot_delay
                    clicked_inventory_item = False

                    if Inventory.crafting_menu_open:
                        Inventory.handle_crafting_click(self, mouse_x, mouse_y)

                    # Vaatab kas click oli invis sees või mitte
                    for index, rect in enumerate(Inventory.inventory_display_rects):
                        if rect.collidepoint(mouse_x, mouse_y):
                            Inventory.check_slot(self, index, mouse_state[2])
                            clicked_inventory_item = True
                            break  # Exitib loopist kui keegi clickib

    def handle_crafting_click(self, x: int, y: int) -> None:
        """ Lubab hiit kasutades craftida """
        try:
            for item_name, rect in Inventory.craftable_items_display_rects.items():
                if rect.collidepoint(x, y):
                    if item_name in Inventory.inventory or Inventory.total_slots > len(Inventory.inventory):

                        crafted_item = Inventory.craft_item(self, item_name)  # Pass 'self' and 'item_name'
                        if crafted_item:
                            # Eemaldab invist craftitud itemi tegemiseks vajalikud materjalid
                            for required_item, required_amount in items_list[item_name]["Recipe"].items():
                                Inventory.remove_item(self, required_item, required_amount)  # Pass 'self'

                            # Lisab craftitud itemi invi
                            Inventory.add_item(self, crafted_item)

                    else:
                        Player_audio.error_audio(self)
                        text = "Not enough space in Inventory."
                        UniversalVariables.ui_elements.append(text)

                        if text in Fading_text.shown_texts:
                            Fading_text.shown_texts.remove(text)

        except AttributeError: return

    def check_slot(self, index: int, delete_boolean=False) -> None:
        """Checks what's in the inventory's selected slot."""

        try:
            if delete_boolean == False:
                item = list(Inventory.inventory.keys())[index]
                value = list(Inventory.inventory.values())[index]
                UniversalVariables.current_equipped_item =  item

            else:
                item = list(Inventory.inventory.keys())[index]
                value = list(Inventory.inventory.values())[index]
                Inventory.inventory[item] -= 1
                if value <= 1:
                    del Inventory.inventory[item]
                    UniversalVariables.current_equipped_item = None  
                else:
                    UniversalVariables.current_equipped_item =  item

        except IndexError as IE:
            print(IE)
            UniversalVariables.current_equipped_item = None

    def call(self) -> None:
        """ Inventory kutsumiseks on see func. """

        if len(Inventory.inventory.items()) != 0 and Inventory.message_to_user == False and Inventory.first_time_click != True:
            UniversalVariables.ui_elements.append(
                """ Press TAB to open inventory. """)
            Inventory.message_to_user = True

        Inventory.handle_mouse_click(self)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_TAB] and not Inventory.tab_pressed:  # double locked, yks alati true aga teine mitte
            if Inventory.first_time_click == False:
                Inventory.first_time_click = True
                UniversalVariables.ui_elements.append(' Select items with left click. Remove items with right click. ')
            
            Inventory.tab_pressed = True
            Inventory.inv_count += 1

            if (Inventory.inv_count % 2) == 0: Inventory.render_inv = False
            else:
                Inventory.render_inv = True

        elif not keys[pygame.K_TAB]: Inventory.tab_pressed = False
        
        if Inventory.render_inv:
            Inventory.render(self)  # Render inventory
        else:
            Inventory.render(self, update_white_text=True)  # Kui sulgeb invi white text itemitega, ss j2rgmine kord ei ole neid itemid enam valged

    # TODO : invi on vaja optimatiseerida
    def calculate(self, calc_slots_only=False) -> None:
        """ Arvutab invetory suuruse, asukoha
        vastavalt playeri asukohale """

        if UniversalVariables.maze_counter == 1:
            total_rows = 2
            total_cols = 2

        if UniversalVariables.maze_counter == 2:
            total_rows = 3
            total_cols = 2

        if UniversalVariables.maze_counter == 3:
            total_rows = 4
            total_cols = 2

        if UniversalVariables.maze_counter >= 4:
            total_rows = 5
            total_cols = 2

        Inventory.total_slots = total_rows * total_cols

        if calc_slots_only:
            return

        Inventory.inventory_display_rects = []
        rect_width: int = UniversalVariables.block_size / 2
        rect_height: int = UniversalVariables.block_size / 2

        # Calculate inventory position relative to player and screen size
        rect_x: int = self.player_rect.centerx + total_cols + UniversalVariables.block_size / 2  # Siia ei tohi offsetti panna
        rect_y: int = self.player_rect.centery - total_rows * UniversalVariables.block_size / 4  # Siia ei tohi offsetti panna

        right_side: int = UniversalVariables.screen.get_size()[0] - (
                    Camera.camera_borders['left'] * 2) + UniversalVariables.block_size * 0.6
        left_side: int = Camera.camera_borders['left'] * 2

        if rect_x >= right_side:
            rect_x = UniversalVariables.player_x - UniversalVariables.block_size * total_cols / 2 + UniversalVariables.offset_x
        elif rect_x >= left_side:
            rect_x = UniversalVariables.player_x + UniversalVariables.block_size * 2 / 2 + UniversalVariables.offset_x

        # Create inventory rectangles
        for rows in range(total_rows):
            for cols in range(total_cols):
                rect = pygame.Rect(rect_x + cols * rect_width, rect_y + rows * rect_height, rect_width, rect_height)
                Inventory.inventory_display_rects.append(rect)

    def render(self, update_white_text=None) -> None:
        """ Callib calculate_inventory, renderib invi, invis olevad itemid ja nende kogused """

        # Clear the white text items and counters if rendering inventory is false
        if update_white_text == True:
            Inventory.white_colored_items.clear()
            Inventory.white_text_counters.clear()
            return

        Inventory.calculate(self)
    
        # Create a semi-transparent overlay
        overlay = pygame.Surface((UniversalVariables.screen.get_width(), UniversalVariables.screen.get_height()), pygame.SRCALPHA)
        overlay.set_alpha(180)
    
        # Draw item slots with borders
        for rect in Inventory.inventory_display_rects:
            pygame.draw.rect(overlay, (177, 177, 177), rect, border_radius=5)  # Gray background
            pygame.draw.rect(overlay, 'black', rect, 2, border_radius=5)  # Black border
    
        # Blit the overlay onto the screen
        UniversalVariables.screen.blit(overlay, (0, 0))
    
        new_white_items = set()
        for rect, (item_name, count) in zip(Inventory.inventory_display_rects, Inventory.inventory.items()):
            item_rect = pygame.Rect(rect.x + 3, rect.y + 3, rect.width - 6, rect.height - 6)
    
            if count > 0:
                item_image = ImageLoader.load_image(item_name)
                if item_image:
                    item_image = pygame.transform.scale(item_image, (int(rect.width / 1.4), int(rect.height / 1.4)))
                    item_image_rect = item_image.get_rect(center=item_rect.center)
    
                    font = pygame.font.Font(None, 20)
                    
                    # Check if the item is new or its count has changed
                    if (item_name not in Inventory.old_inventory or 
                        (item_name in Inventory.old_inventory and Inventory.inventory[item_name] != Inventory.old_inventory[item_name])):
                        Inventory.white_text = True
                        new_white_items.add(item_name)
                        Inventory.white_text_counters[item_name] = 0  # Initialize the counter for the new item
    
                    text_color = 'black'
                    if item_name in Inventory.white_colored_items:
                        text_color = 'white'  # color for item change 
                        Inventory.white_text_counters[item_name] += 1  # Increment the counter for the item
    
                    text = font.render(str(count), True, text_color)
                    text_rect = text.get_rect(center=(rect.x + 10, rect.y + 10))
    
                    blit_operations = [(item_image, item_image_rect.topleft), (text, text_rect.topleft)]
                    UniversalVariables.screen.blits(blit_operations, False)
    
        items_to_remove = [item for item, counter in Inventory.white_text_counters.items() if counter >= 120]
        for item in items_to_remove:
            Inventory.white_colored_items.remove(item)
            del Inventory.white_text_counters[item]
    
        Inventory.white_colored_items.update(new_white_items)
        Inventory.old_inventory = Inventory.inventory.copy()

    def calculate_craftable_items(self):
        """ Otsib kõik itemid ülesse mida
        saab craftida vastavalt invile """

        self.craftable_items = {}

        for item in items_list:
            if "Recipes" in item:
                # Käib kõik itemi retseptid läbi
                for recipe in item["Recipes"]:
                    can_craft = True
                    required_items = recipe.get("Recipe", {})

                    for required_item, required_amount in required_items.items():
                        if required_item not in Inventory.inventory or \
                                Inventory.inventory[required_item] < required_amount:
                            can_craft = False
                            break

                    if can_craft:
                        self.craftable_items[item["Name"]] = recipe.get("Amount", 1)

        Inventory.craftable_items_display_rects = {}

        rect_width: int = UniversalVariables.block_size / 2
        rect_height: int = UniversalVariables.block_size / 2
        max_cols: int = 3  # Max tulpade arv reas

        # Arvutab inventoryle asukoha vastavalt playeri asukohale ja inventory settingutele
        rect_x: int = 50
        rect_y: int = 50

        craftable_items = list(self.craftable_items.keys())  # Extractib craftitud itemite nimed

        for index, craftable_item in enumerate(craftable_items):
            rows = index // max_cols
            cols = index % max_cols

            rect = pygame.Rect(rect_x + cols * rect_width, rect_y + rows * rect_height, rect_width, rect_height)
            Inventory.craftable_items_display_rects[craftable_item] = rect

    @craftable_items_manager
    def render_craftable_items(self):
        """ Render craftable items and respond to clicks """

        # Exit function if there are no craftable items
        if not Inventory.craftable_items_display_rects:
            return

        screen_width = UniversalVariables.screen.get_width()
        screen_height = UniversalVariables.screen.get_height()

        # Create a semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.set_alpha(180)  # Set overlay transparency

        # Prepare the font once
        font = pygame.font.Font(None, 20)

        # Pre-load images and resize them
        resized_images = {}
        for item_name, rect in Inventory.craftable_items_display_rects.items():
            object_image = ImageLoader.load_image(item_name)
            if object_image is not None:
                object_image = pygame.transform.scale(object_image, (int(rect.width / 1.4), int(rect.height / 1.4)))
                resized_images[item_name] = object_image

        # Prepare the list of blit operations
        blit_operations = []

        # Draw the background and items on the overlay
        for item_name, rect in Inventory.craftable_items_display_rects.items():
            pygame.draw.rect(overlay, (177, 177, 177), rect)  # Draw semi-transparent background
            pygame.draw.rect(overlay, 'black', rect, 2)  # Draw black border

            item_rect = pygame.Rect(rect.x + 3, rect.y + 3, rect.width - 6, rect.height - 6)
            pygame.draw.rect(overlay, (0, 0, 0, 180), item_rect)  # Draw item background

            # Blit the pre-loaded and resized image
            if item_name in resized_images:
                object_image = resized_images[item_name]
                item_image_rect = object_image.get_rect(center=item_rect.center)
                blit_operations.append((object_image, item_image_rect.topleft))

            # Render the amount of craftable items
            text = font.render(str(self.craftable_items[item_name]), True, 'Black')
            text_rect = text.get_rect(center=(rect.x + 10, rect.y + 10))
            blit_operations.append((text, text_rect))

        # Perform all blit operations at once
        overlay.blits(blit_operations)

        # Blit the overlay to the screen once
        UniversalVariables.screen.blit(overlay, (0, 0))

    def craft_item(self, item_name):
        """ Craftib itemi ja uuendab invi """
        # Võtab item_list'ist nimed
        crafted_item = next((item for item in items_list if item["Name"] == item_name), None)

        if crafted_item:
            recipes = crafted_item.get("Recipes", [])
            amount = 0

            # Läheb läbi iga retsepti
            for recipe in recipes:
                required_items = recipe.get("Recipe", {})
                can_craft = all(
                    Inventory.inventory.get(required_item, 0) >= required_amount for required_item, required_amount in
                    required_items.items()
                )

                if can_craft:
                    # Võtab invist kasutatud itemid ära
                    for required_item, required_amount in required_items.items():
                        Inventory.inventory[required_item] -= required_amount

                    # Arvutab craftimisest saadud koguse vastavalt retseptile
                    amount += recipe.get("Amount", 1)

            # Lisab craftitud itemi invi
            Inventory.inventory[item_name] = Inventory.inventory.get(item_name, 0) + amount

            # Remove items with a count of zero from the inventory
            Inventory.inventory = {k: v for k, v in Inventory.inventory.items() if v > 0}

    def render_equipped_slot(self, item_name):
        slot_image = ImageLoader.load_gui_image("Selected_Item_Inventory")
        position = (UniversalVariables.screen_x // 2 - 170, UniversalVariables.screen_y - 51)
        resized_slot_image = pygame.transform.scale(slot_image, (slot_image.get_width() * 0.9 , slot_image.get_height() * 0.9))

        # List to hold all blit operations
        blit_operations = [(resized_slot_image, position)]

        if item_name is None:
            UniversalVariables.screen.blits(blit_operations)
            UniversalVariables.current_equipped_item = None
            return

        if item_name not in Inventory.inventory:
            UniversalVariables.screen.blits(blit_operations)
            UniversalVariables.current_equipped_item = None
            return

        # Update equipped item type if the item has changed
        if UniversalVariables.current_equipped_item != item_name:
            UniversalVariables.current_equipped_item_item_type = next(
                (item["Type"] for item in items_list if item["Name"] == item_name), None)
            UniversalVariables.current_equipped_item = item_name

        item_image = ImageLoader.load_image(item_name)

        # Resize item image to fit within slot dimensions
        max_item_size = (resized_slot_image.get_width() - 15, resized_slot_image.get_height() - 15)
        resized_item_image = pygame.transform.scale(item_image, max_item_size)

        # Calculate position to center item image
        item_x = position[0] + (resized_slot_image.get_width() - resized_item_image.get_width()) // 2
        item_y = position[1] + (resized_slot_image.get_height() - resized_item_image.get_height()) // 2

        # Add item image to blit operations
        blit_operations.append((resized_item_image, (item_x, item_y)))

        # Render item count at top left corner of slot if count is greater than 1 and item is not a tool
        if UniversalVariables.current_equipped_item_item_type != "Tool":
            text = str(Inventory.inventory[item_name])
            if text not in Inventory.text_cache:
                font = pygame.font.Font(None, 20)
                Inventory.text_cache[text] = font.render(text, True, (0, 0, 0))  # Render text with black color

            text_surface = Inventory.text_cache[text]
            text_rect = text_surface.get_rect(topleft=(position[0] + 5, position[1] + 5))  # Calculate position
            blit_operations.append((text_surface, text_rect.topleft))

        # Perform all blit operations
        UniversalVariables.screen.blits(blit_operations)
        Inventory.item_delay_bar(self, resized_slot_image, position)

    def item_delay_bar(self, slot_image, position):
        """ See func on inventory all, sest slot_image andmed asuvad siin ja eksportimine on keerukas. """

        width  = slot_image.get_width()
        height = slot_image.get_height()

        # Tekitab semi-transparent recti
        overlay = pygame.Surface((UniversalVariables.screen.get_width(), UniversalVariables.screen.get_height()),
                                 pygame.SRCALPHA)
        overlay.set_alpha(100)

        if UniversalVariables.item_delay < UniversalVariables.item_delay_max:
            tl_point = position[0]
            tr_point = position[1]
            
            progress = int((UniversalVariables.item_delay / UniversalVariables.item_delay_max) * height)

            loading_bar_border_rect = pygame.Rect(tl_point, tr_point + progress, width, height - progress,)
            pygame.draw.rect(overlay, 'black', loading_bar_border_rect)
            UniversalVariables.screen.blit(overlay, (0,0))