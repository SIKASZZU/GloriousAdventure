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

    def handle_mouse_click(self) -> None:
        """ Inventory spetsiifiline functioon. 
            Vaatab, kas inventoriesse on tehtud klikk. """

        if (Inventory.inv_count % 2) != 0:
            mouse_state: Tuple[bool, bool, bool] = pygame.mouse.get_pressed()
            if mouse_state[0]:  # Vaatab, kas player klikib vasakut hiireklikki.
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for index, rect in enumerate(Inventory.inventory_display_rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        Inventory.check_slot(self, index)

                Inventory.calculate_craftable_items(self)  # Kontrollib itemeid mida saab craftida


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
                Inventory.render_craftable_items(self)
                Inventory.render_craftable_items(self)

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


### TODO: Craftimise box on veel tegemata broken af
    def calculate_craftable_items(self):
        """ Otsib kõik itemid ülesse mida
        saab craftida vastavalt mis invis on.
        Arvutab crafting menu """

        # Seda kasutatakse objects.py - ObjectManagement - def add_object_to_inv(self, object_id: int, obj_collision_box: tuple[int, ...]) -> None:
        # Seda kasutatakse inventory.py - Inventory - def handle_mouse_click(self) -> None:
        craftable_items = {}

        # Otsib itemi retsepti ja vaatab kas invis on piisavalt materjale, et seda craftida.
        for item in items_list:
            if "Recipe" in item:
                can_craft = True
                for required_item, required_amount in item["Recipe"].items():
                    if required_item not in Inventory.inventory or Inventory.inventory[required_item] < required_amount:
                        can_craft = False
                        break
                if can_craft:
                    craftable_items[item["Name"]] = item.get("Amount", 1)
        self.craftable_items = craftable_items



        self.craftable_items_display_rects = {}

        print(self.craftable_items)
        print(self.craftable_items_display_rects)

        rect_width: int = UniversalVariables.block_size / 2
        rect_height: int = UniversalVariables.block_size / 2
        total_rows: int = 6  # Max: 9
        total_cols: int = 3  # Max: 9

        # Arvutab inventoryle asukoha vastavalt playeri asukohale ja inventory settingutele
        rect_x: int = 100
        rect_y: int = 100

        for rows in range(total_rows):
            for cols in range(total_cols):
                rect = pygame.Rect(rect_x + cols * rect_width, rect_y + rows * rect_height, rect_width, rect_height)
                item_name = f"Craftable Item {rows * total_cols + cols + 1}"
                self.craftable_items_display_rects[item_name] = rect

    def render_craftable_items(self):
        pass

        # font = pygame.font.Font(None, 24)
        # max_cols = 3
        # max_rows = 6
        # rect_width = UniversalVariables.block_size / 2
        # rect_height = UniversalVariables.block_size / 2
        # spacing_x = 50

        # craftable_items_rects = Inventory.craftable_items_display_rects

        # craftable_index = 0
        # for craftable_item, rect in craftable_items_rects.items():
        #     row = craftable_index // max_cols
        #     col = craftable_index % max_cols

        #     if row >= max_rows:
        #         break

        #     rect.x = col * (rect_width + spacing_x)
        #     rect.y = row * rect_height

        #     text_surface = font.render(craftable_item, True, (255, 255, 255))
        #     text_rect = text_surface.get_rect(center=rect.center)

        #     pygame.draw.rect(screen, (50, 50, 50), rect)
        #     screen.blit(text_surface, text_rect)

        #     craftable_index += 1
