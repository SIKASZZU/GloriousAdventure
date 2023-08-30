from items import minerals
import pygame
import images

def render_inventory(self):

    # Invi hall taust
    inventory_bar_rect = pygame.Rect(50, 50, 450, 50)
    pygame.draw.rect(self.screen, '#B1B1B1', inventory_bar_rect)

    # Mustad boxid itemite ümber
    for rect in self.inventory_display_rects:
        pygame.draw.rect(self.screen, 'black', rect, 2)

    for rect, (item_name, count) in zip(self.inventory_display_rects, self.inventory.items()):
        item_color = minerals.get(item_name, 'black')
        item_rect = pygame.Rect(rect.x + 3, rect.y + 3, rect.width - 6, rect.height - 6)
        pygame.draw.rect(self.screen, item_color, item_rect)
        # Paneb invile pildid
        item_image = images.item_images.get(item_name)

        if item_image is not None:
            # Resize
            item_image = pygame.transform.scale(item_image, (int(rect.width / 1.4), int(rect.height / 1.4)))
            # Paneb itembi invi boxi keskele
            item_image_rect = item_image.get_rect(center=item_rect.center)
            # Displayb resized itemit
            self.screen.blit(item_image, item_image_rect.topleft)

        font = pygame.font.Font(None, 20)
        text = font.render(str(count), True, 'White')
        text_rect = text.get_rect(center=(rect.x+10, rect.y+10))
        self.screen.blit(text, text_rect)
    inventory_bar_rect = pygame.Rect(50, 50, 450, 50)
    pygame.draw.rect(self.screen, 'black', inventory_bar_rect, 4)  # Paksem border