import pygame
from variables import UniversalVariables
from images import ImageLoader

class SpriteSheet:
    def __init__(self, image: str, frame_width: int, frame_height: int) -> None:
        self.sheet = ImageLoader.load_image(image)
        self.frame_width = frame_width
        self.frame_height = frame_height

    def get_image(self, frame_index: int) -> pygame.Surface:
        y = 0  # Default

        x = frame_index * self.frame_width
        image = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (x, y, self.frame_width, self.frame_height))
        return pygame.transform.scale(image, (UniversalVariables.player_width, UniversalVariables.player_height))
