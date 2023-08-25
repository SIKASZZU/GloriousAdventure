import pygame

class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

        self.block_size = 100
    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height), pygame.SRCALPHA)  # Teeb selle transparentiks
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (self.block_size, self.block_size))
        return image
