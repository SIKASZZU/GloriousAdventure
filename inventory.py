from items import minerals
import pygame
import images

class Inventory:

    def handle_mouse_click(self):
        if (self.inv_count % 2) != 0:
            mouse_state = pygame.mouse.get_pressed()
            if mouse_state[0]:  # Check for left mouse button press
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for index, rect in enumerate(self.inventory_display_rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        print(f"Inventory slot {index} clicked")
    

    def call_inventory(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_TAB] and not self.tab_pressed:  # double locked, yks alati true aga teine mitte
            self.tab_pressed = True
            self.inv_count += 1

            if (self.inv_count % 2) == 0: self.render_inv = False
            else: self.render_inv = True

        elif not keys[pygame.K_TAB]: self.tab_pressed = False


    def render_inventory(self):
        Inventory.calculate_inventory(self)
        # Mustad boxid itemite ümber
        for rect in self.inventory_display_rects:

            # Invi hall taust
            pygame.draw.rect(self.screen, '#B1B1B1', rect)  # Invi hall taust
            pygame.draw.rect(self.screen, 'black', rect, 2)  # Sisemiste ruutude paksus
            #inventory_bar_rect = pygame.Rect(rect.x + 3, rect.y + 3, rect.width - 6, rect.height - 6)
            #pygame.draw.rect(self.screen, 'black', inventory_bar_rect, 4)  # Paks border ymber invi

        for rect, (item_name, count) in zip(self.inventory_display_rects, self.inventory.items()):
            item_color = minerals.get(item_name, 'white')
            item_rect = pygame.Rect(rect.x + 3, rect.y + 3, rect.width - 6, rect.height - 6)
            pygame.draw.rect(self.screen, item_color, item_rect)

            # Paneb invi pildid
            item_image = images.item_images.get(item_name)

            # Pildi mahutamine sellesse v2iksesse ruutu
            if item_image is not None:
                # Resize
                item_image = pygame.transform.scale(item_image, (int(rect.width / 1.4), int(rect.height / 1.4)))
                # Paneb itembi invi boxi keskele
                item_image_rect = item_image.get_rect(center=item_rect.center)
                # Displayb resized itemit
                self.screen.blit(item_image, item_image_rect.topleft)

            # font, numbrid itemite loetlemiseks
            font = pygame.font.Font(None, 20)
            text = font.render(str(count), True, 'White')
            text_rect = text.get_rect(center=(rect.x+10, rect.y+10))
            self.screen.blit(text, text_rect)


    def calculate_inventory(self):
        self.inventory_display_rects = []
        self.rect_width = 50
        self.rect_height = 50
        self.total_rows = 6
        self.total_cols = 3

        self.rect_x = self.player_rect.right + 50 + self.offset_x  # Tavaliselt on inv playerist paremal
        self.rect_y = self.player_y - self.block_size + self.offset_y

        right_side = self.screen.get_size()[0] - (self.camera_borders['left'] * 2)  # 1000 - (100 * 2) = 800
        left_side = self.camera_borders['left']  # 100

        if self.rect_x >= right_side:  # invi visuaalselt n2itamine vasakul, kui see paremast 22rest v2lja l2heb
            self.rect_x = self.player_x - 150 + self.offset_x

        if self.rect_x <= left_side:  # invi visuaalselt n2itamine vasakul, kui see vasakust 22rest v2lja l2heb
            self.rect_x = left_side + self.block_size + 25

        for rows in range(self.total_rows):
            for cols in range(self.total_cols):
                rect = pygame.Rect(self.rect_x + cols * self.rect_width, self.rect_y + rows * self.rect_height, self.rect_width, self.rect_height)
                self.inventory_display_rects.append(rect)
