import pygame

from images import ImageLoader
from camera import Camera
from variables import UniversalVariables
from items import items_list
from variables import log_calls_with_location, memoize, log_execution_time


class Inventory:

    inventory_display_rects = []
    craftable_items_display_rects = []
    last_clicked_slot = int  # V2hendab terminali spammi. Ei sp2mmi seda slotti, mida juba klikkis.

    inventory = {}  # Terve inv (prindi seda ja saad teada mis invis on)
    inv_count: int = 0  # Otsustab, kas renderida inv v6i mitte

    render_inv: bool = False  # Inventory renderminmine
    tab_pressed: bool = False  # Keep track of whether Tab was pressed
    check_slot_delay: int = 0
    craftable_items = {}

    def handle_mouse_click(self) -> None:
        """ Lubab invis ja craftimises clicke kasutada
        ja lisab ka viite CHECK_DELAY_THRESHOLD  """
        CHECK_DELAY_THRESHOLD = 200  # Threshold slotide clickimiseks
        if (Inventory.inv_count % 2) != 0:
            mouse_state: tuple[bool, bool, bool] = pygame.mouse.get_pressed()
            if mouse_state[0]:  # Vaatab kas keegi on hiire vasakut clicki vajutanud
                mouse_x, mouse_y = pygame.mouse.get_pos()
                current_time = pygame.time.get_ticks()
                if current_time - Inventory.check_slot_delay >= CHECK_DELAY_THRESHOLD:
                    Inventory.check_slot_delay = current_time  # Uuendab viimast check_slot_delay
                    clicked_inventory_item = False
                    last_clicked_index = Inventory.last_clicked_slot  # Jätab viimase clicki aja meelde

                    # Vaatab kas click oli invis sees või mitte
                    for index, rect in enumerate(Inventory.inventory_display_rects):
                        if rect.collidepoint(mouse_x, mouse_y):
                            if index != last_clicked_index:  # Kontrollib millist sloti vajutati, kas on sama või mitte
                                Inventory.check_slot(self, index)
                            else:
                                print(f'Already selected slot nr {index + 1}')  ### TODO: Peaks olema check sloti all
                            clicked_inventory_item = True
                            break  # Exitib loopist kui keegi clickib

                    if not clicked_inventory_item:
                        # Vaatab kas click on craftimis rectis
                        Inventory.calculate_craftable_items(self)
                        Inventory.handle_crafting_click(self, mouse_x, mouse_y)

                    Inventory.last_clicked_slot = index  # Uuendab last_clicked_slot

    def handle_crafting_click(self, x: int, y: int) -> None:
        """ Lubab hiit kasutades craftida """

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
        """Checks what's in the inventory's selected slot."""

        try:
            if index != Inventory.last_clicked_slot:
                item = list(Inventory.inventory.keys())[index]
                value = list(Inventory.inventory.values())[index]
                print(f'Inventory slot {index + 1} contains: {item} : {value}')
        except IndexError:
            print(f'Nothing in slot nr {index + 1}')
        Inventory.last_clicked_slot = index  # Updateb viimast clicki

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
        Inventory.calculate_craftable_items(self)

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

            if count > 0:  # Renderib pilti ainult siis kui item on invis olemas
                item_image = ImageLoader.load_image(item_name)

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
                text_rect = text.get_rect(center=(rect.x + 10, rect.y + 10))
                UniversalVariables.screen.blit(text, text_rect)

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

        self.craftable_items_display_rects = {}

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
            self.craftable_items_display_rects[craftable_item] = rect

    def render_craftable_items(self):
        """ Renderib itemeid, mida saab
        craftida ja reageerib clickidele """

        Inventory.craftable_items_display_rects = self.craftable_items_display_rects

        # Kui craftable itemeid pole siis tuleb funcist välja
        if Inventory.craftable_items_display_rects.__len__() != 0:

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

                # Pre-loading pildi, peformance säästmiseks
                object_image = ImageLoader.load_image(item_name)

                # Muudab pildi suurust vastavalt inventory sloti suurusele
                if object_image is not None:
                    # Resize itemi inventory
                    object_image = pygame.transform.scale(object_image, (int(rect.width / 1.4), int(rect.height / 1.4)))

                    # Paneb itembi invi boxi keskele
                    item_image_rect = object_image.get_rect(center=item_rect.center)

                    # Displayb resized itemit
                    UniversalVariables.screen.blit(object_image, item_image_rect.topleft)

                # font, numbrid itemite loetlemiseks
                font = pygame.font.Font(None, 20)
                text = font.render(str(self.craftable_items[item_name]), True, 'Black')  # Display craftable amounts
                text_rect = text.get_rect(center=(rect.x + 10, rect.y + 10))
                UniversalVariables.screen.blit(text, text_rect)

    ### TODO: kui craftimise ajal hoida shifti all ja clickida siis crafti max koguse mida saab craftida
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

