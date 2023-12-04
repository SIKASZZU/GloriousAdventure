import pygame

import images
from camera import Camera
from variables import UniversalVariables
from items import items_list

class Inventory:

    inventory_display_rects = []
    craftable_items_display_rects = []
    last_clicked_slot = int  # V2hendab terminali spammi. Ei sp2mmi seda slotti, mida juba klikkis.

    inventory = {}  # Terve inv (prindi seda ja saad teada mis invis on)
    inv_count: int = 0  # Otsustab, kas renderida inv v6i mitte

    render_inv: bool = False  # Inventory renderminmine
    tab_pressed: bool = False  # Keep track of whether Tab was pressed

    craftable_items = {}

    def handle_mouse_click(self) -> None:
        """Inventory specific function. Handles both inventory item clicks and crafting item clicks."""

        if (Inventory.inv_count % 2) != 0:
            mouse_state: Tuple[bool, bool, bool] = pygame.mouse.get_pressed()
            if mouse_state[0]:  # Check if the player clicks the left mouse button.
                mouse_x, mouse_y = pygame.mouse.get_pos()
                clicked_inventory_item = False

                # Check if the click is within the inventory display
                for index, rect in enumerate(Inventory.inventory_display_rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        Inventory.check_slot(self, index)
                        clicked_inventory_item = True

                if not clicked_inventory_item:
                    # Check if the click is within the crafting display
                    Inventory.calculate_craftable_items(self)  # Check craftable items
                    Inventory.handle_crafting_click(self, mouse_x, mouse_y)

    def handle_crafting_click(self, x: int, y: int) -> None:
        """Handles clicks on craftable items in the crafting display."""

        for item_name, rect in Inventory.craftable_items_display_rects.items():
            if rect.collidepoint(x, y):
                crafted_item = Inventory.craft_item(self, item_name)  # Pass 'self' and 'item_name'
                if crafted_item:
                    # Eemaldab invist craftitud itemi tegemiseks vajalikud materjalid
                    for required_item, required_amount in items_list[item_name]["Recipe"].items():
                        Inventory.remove_item(self, required_item, required_amount)  # Pass 'self'

                    # Lisab craftitud itemi invi
                    Inventory.add_item(self, crafted_item)

    def check_slot(self, index: int) -> None:
        """ Vaatab, mis toimub inventory valitud slotis. """
        
        try:
            if index != Inventory.last_clicked_slot:  # Kontrollib, kas viimane klikk oli samale slotile v6i ei.
                item = list(Inventory.inventory.keys())[index]
                value = list(Inventory.inventory.values())[index]
                print(f'Inventory slot {index + 1} slot contains: {item} : {value}')
            else: 
                pass  # pst, v6iks PASSi asemel olla: print(f'Already selected slot nr {index + 1}')
        except IndexError: 
            print(f'Nothing in slot nr {index + 1}')
        Inventory.last_clicked_slot = index  # Uuendab viimasena klikitud slotti


    def call_inventory(self) -> None:
        """ Vajutades tabi ei hakka inventory
        visuaalselt glitchima on/off. """

        keys = pygame.key.get_pressed()
        if keys[pygame.K_TAB] and not Inventory.tab_pressed:  # double locked, yks alati true aga teine mitte
            Inventory.tab_pressed = True
            Inventory.inv_count += 1

            if (Inventory.inv_count % 2) == 0: Inventory.render_inv = False
            else:
                Inventory.render_inv = True

        elif not keys[pygame.K_TAB]: Inventory.tab_pressed = False

    def calculate_inventory(self) -> None:
        """ Arvutab invetory suuruse, asukoha
        vastavalt playeri asukohale """

        Inventory.inventory_display_rects = []
        rect_width: int = UniversalVariables.block_size / 2
        rect_height: int = UniversalVariables.block_size / 2
        total_rows: int = 6  # Max: 9
        total_cols: int = 3  # Max: 9

        ### TODO: Kui inv on PAREMAL siis see on playerist kaugemal - Vaata seda valget boxi playeri ümber

        # Arvutab inventoryle asukoha vastavalt playeri asukohale ja inventory settingutele
        rect_x: int = self.player_rect.centerx + total_cols + UniversalVariables.block_size / 2 + UniversalVariables.offset_x
        rect_y: int = self.player_rect.centery - total_rows * UniversalVariables.block_size / 4 + UniversalVariables.offset_y

        right_side: int = UniversalVariables.screen.get_size()[0] - (Camera.camera_borders['left'] * 2) + UniversalVariables.block_size * 0.6 # 1000 - (100 * 2) = 800
        left_side: int = Camera.camera_borders['left'] * 2 # 100

        if rect_x >= right_side:  # invi visuaalselt n2itamine vasakul, kui see paremast 22rest v2lja l2heb
            rect_x = UniversalVariables.player_x - UniversalVariables.block_size * total_cols / 2 + UniversalVariables.offset_x

        elif rect_x >= left_side:  # invi visuaalselt n2itamine vasakul, kui see paremast 22rest v2lja l2heb
            rect_x = UniversalVariables.player_x + UniversalVariables.block_size * 2 / 2 + UniversalVariables.offset_x

        for rows in range(total_rows):
            for cols in range(total_cols):
                rect = pygame.Rect(rect_x + cols * rect_width, rect_y + rows * rect_height, rect_width, rect_height)
                Inventory.inventory_display_rects.append(rect)


    def render_inventory(self) -> None:
        """ Callib calculate_inventory,
        renderib invi, invis olevad
        itemid ja nende kogused """

        Inventory.calculate_inventory(self)

        # Tekitab semi-transparent recti
        overlay = pygame.Surface((UniversalVariables.screen.get_width(), UniversalVariables.screen.get_height()), pygame.SRCALPHA)
        overlay.set_alpha(180)  # See muudab kui hästi on seda näha /// 0 - 255

        # Mustad boxid itemite ümber
        for rect in Inventory.inventory_display_rects:
            # Invi hall taust
            pygame.draw.rect(overlay, (177, 177, 177), rect)  # Teeb inventory läbipaistvaks
            pygame.draw.rect(overlay, 'black', rect, 2)

        # Visualiseerib invi
        UniversalVariables.screen.blit(overlay, (0, 0))

        for rect, (item_name, count) in zip(Inventory.inventory_display_rects, Inventory.inventory.items()):
            item_rect = pygame.Rect(rect.x + 3, rect.y + 3, rect.width - 6, rect.height - 6)
            pygame.draw.rect(overlay, (105, 105, 105, 128), item_rect)

            # Paneb invi pildid
            item_image = images.item_images.get(item_name)

            # Muudab pildi suurust vastavalt inventory sloti suurusele
            if item_image is not None:
                # Resize itemi inventory
                item_image = pygame.transform.scale(item_image, (int(rect.width / 1.4), int(rect.height / 1.4)))

                # Paneb itembi invi boxi keskele
                item_image_rect = item_image.get_rect(center=item_rect.center)

                # Displayb resized itemit
                UniversalVariables.screen.blit(item_image, item_image_rect.topleft)

            # font, numbrid itemite loetlemiseks
            font = pygame.font.Font(None, 20)
            text = font.render(str(count), True, 'Black')
            text_rect = text.get_rect(center=(rect.x+10, rect.y+10))
            UniversalVariables.screen.blit(text, text_rect)


### TODO: SEE AJAB MÄNGU LAGGAMA
    def calculate_craftable_items(self):
        """Calculates craftable items from the items_list"""

        self.craftable_items = {}

        for item in items_list:
            if "Recipe" in item:
                can_craft = True
                for required_item, required_amount in item["Recipe"].items():
                    if required_item not in Inventory.inventory or Inventory.inventory[required_item] < required_amount:
                        can_craft = False
                        break
                if can_craft:
                    self.craftable_items[item["Name"]] = item.get("Amount", 1)

        self.craftable_items_display_rects = {}

        rect_width: int = UniversalVariables.block_size / 2
        rect_height: int = UniversalVariables.block_size / 2
        max_cols: int = 3  # Maximum columns per row

        # Arvutab inventoryle asukoha vastavalt playeri asukohale ja inventory settingutele
        rect_x: int = 100
        rect_y: int = 100

        craftable_items = list(self.craftable_items.keys())  # Extract craftable item names

        for index, craftable_item in enumerate(craftable_items):
            rows = index // max_cols
            cols = index % max_cols

            rect = pygame.Rect(rect_x + cols * rect_width, rect_y + rows * rect_height, rect_width, rect_height)
            self.craftable_items_display_rects[craftable_item] = rect

    def render_craftable_items(self):
        """Render craftable items with images, amounts, and handle adding them to the inventory when clicked"""

        Inventory.calculate_craftable_items(self)

        Inventory.craftable_items_display_rects = self.craftable_items_display_rects

        # Tekitab semi-transparent recti
        overlay = pygame.Surface((UniversalVariables.screen.get_width(), UniversalVariables.screen.get_height()),
                                 pygame.SRCALPHA)
        overlay.set_alpha(180)  # See muudab kui hästi on seda näha /// 0 - 255

        # Mustad boxid itemite ümber
        for rect in Inventory.craftable_items_display_rects.values():  # Use self here to refer to the instance variable
            # Invi hall taust
            pygame.draw.rect(overlay, (177, 177, 177), rect)  # Teeb inventory läbipaistvaks
            pygame.draw.rect(overlay, 'black', rect, 2)

        # Visualiseerib invi
        UniversalVariables.screen.blit(overlay, (0, 0))
        for item_name, rect in Inventory.craftable_items_display_rects.items():
            item_rect = pygame.Rect(rect.x + 3, rect.y + 3, rect.width - 6, rect.height - 6)
            pygame.draw.rect(overlay, (0, 0, 0, 180), item_rect)

            item_image = images.item_images.get(item_name)



            print(f"item_name: {item_name}")

            # Muudab pildi suurust vastavalt inventory sloti suurusele
            if item_image is not None:
                # Resize itemi inventory
                item_image = pygame.transform.scale(item_image, (int(rect.width / 1.4), int(rect.height / 1.4)))

                # Paneb itembi invi boxi keskele
                item_image_rect = item_image.get_rect(center=item_rect.center)

                # Displayb resized itemit
                UniversalVariables.screen.blit(item_image, item_image_rect.topleft)

            # font, numbrid itemite loetlemiseks
            font = pygame.font.Font(None, 20)
            text = font.render(str(self.craftable_items[item_name]), True, 'Black')  # Display craftable amounts
            text_rect = text.get_rect(center=(rect.x + 10, rect.y + 10))
            UniversalVariables.screen.blit(text, text_rect)

    def craft_item(self, item_name):
        """Craft an item and update the inventory accordingly"""

        # Retrieve the item details from items_list
        crafted_item = next((item for item in items_list if item["Name"] == item_name), None)

        if crafted_item:
            recipe = crafted_item.get("Recipe", {})
            amount = crafted_item.get("Amount", 1)

            # Check if the player has all the required items for the recipe
            can_craft = all(
                Inventory.inventory.get(required_item, 0) >= required_amount for required_item, required_amount in
                recipe.items()
            )

            if can_craft:
                # Remove the recipe items from the inventory
                for required_item, required_amount in recipe.items():
                    Inventory.inventory[required_item] -= required_amount

                # Add the crafted item to the inventory
                Inventory.inventory[item_name] = Inventory.inventory.get(item_name, 0) + amount
