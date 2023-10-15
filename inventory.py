import pygame

from camera import Camera
import images

class Inventory:

    inventory_display_rects = []
    last_clicked_slot = None  # V2hendab terminali spammi. Ei sp2mmi seda slotti, mida juba klikkis.

    inventory = {}  # Terve inv (prindi seda ja saad teada mis invis on)
    inv_count: int = 0  # Otsustab, kas renderida inv v6i mitte

    render_inv: bool = False  # Inventory renderminmine
    tab_pressed: bool = False  # Keep track of whether Tab was pressed

    def handle_mouse_click(self):
        """ Vaatab, kas inventoriesse on tehtud klikk.
        Inventory spetsiifiline functioon. """

        if (Inventory.inv_count % 2) != 0:
            mouse_state = pygame.mouse.get_pressed()
            if mouse_state[0]:  # Vaatab, kas player klikib vasakut hiireklikki.
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for index, rect in enumerate(Inventory.inventory_display_rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        Inventory.check_slot(self, index)


    def check_slot(self, index):
        """ Vaatab, mis invenotrys toimub valitud slotis. """
        
        try:
            if index != Inventory.last_clicked_slot:  # Kontrollib, kas viimane klikk oli samale slotile v6i ei.
                item = list(Inventory.inventory.keys())[index]
                value = list(Inventory.inventory.values())[index]
                print(f'Inventory slot {index + 1} slot contains: {item} : {value}')
                Inventory.last_clicked_slot = index  # Uuendab viimasena klikitud slotti
            else: 
                pass  # pst, v6iks PASSi asemel olla: print(f'Already selected slot nr {index + 1}')
        except IndexError: 
            print(f'Nothing in slot nr {index + 1}')
            Inventory.last_clicked_slot = index  # Uuendab viimasena klikitud slotti


    def call_inventory(self):
        """ Kui TABi vajutada, ss perma on/off see inventory.
        call_function fixib selle 2ra - self.render_inv tegeleb kui lukuna. """

        keys = pygame.key.get_pressed()
        if keys[pygame.K_TAB] and not Inventory.tab_pressed:  # double locked, yks alati true aga teine mitte
            Inventory.tab_pressed = True
            Inventory.inv_count += 1

            if (Inventory.inv_count % 2) == 0: Inventory.render_inv = False
            else: Inventory.render_inv = True

        elif not keys[pygame.K_TAB]: Inventory.tab_pressed = False


    def render_inventory(self):
        Inventory.calculate_inventory(self)

        # Tekitab semi-transparent recti
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.set_alpha(180)  # See muudab kui hästi on seda näha /// 0 - 255

        # Mustad boxid itemite ümber
        for rect in Inventory.inventory_display_rects:
            # Invi hall taust
            pygame.draw.rect(overlay, (177, 177, 177), rect)  # Draw semi-transparent rectangles on the overlay
            pygame.draw.rect(overlay, 'black', rect, 2)

        # Visualiseerib invi
        self.screen.blit(overlay, (0, 0))

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
                self.screen.blit(item_image, item_image_rect.topleft)

            # font, numbrid itemite loetlemiseks
            font = pygame.font.Font(None, 20)
            text = font.render(str(count), True, 'Black')
            text_rect = text.get_rect(center=(rect.x+10, rect.y+10))
            self.screen.blit(text, text_rect)


    def calculate_inventory(self):

        """ Arvutab invetory suuruse,
        asukoha ja visualiseerib seda
        vastavalt playeri asukohale """

        Inventory.inventory_display_rects = []
        rect_width = self.block_size / 2
        rect_height = self.block_size / 2
        total_rows = 6  # Max: 9
        total_cols = 3  # Max: 9

        # Arvutab inventoryle asukoha vastavalt playeri asukohale ja inventory settingutele
        rect_x = self.player_rect.centerx + total_cols + self.block_size / 2 + self.offset_x
        rect_y = self.player_rect.centery - total_rows * self.block_size / 4 + self.offset_y

        right_side = self.screen.get_size()[0] - (Camera.camera_borders['left'] * 2) + self.block_size * 0.6 # 1000 - (100 * 2) = 800
        left_side = Camera.camera_borders['left'] * 2 # 100

        if rect_x >= right_side:  # invi visuaalselt n2itamine vasakul, kui see paremast 22rest v2lja l2heb
            rect_x = self.player_x - self.block_size * total_cols / 2 + self.offset_x

        elif rect_x >= left_side:  # invi visuaalselt n2itamine vasakul, kui see paremast 22rest v2lja l2heb
            rect_x = self.player_x + self.block_size * 2 / 2 + self.offset_x

        for rows in range(total_rows):
            for cols in range(total_cols):
                rect = pygame.Rect(rect_x + cols * rect_width, rect_y + rows * rect_height, rect_width, rect_height)
                Inventory.inventory_display_rects.append(rect)
