import pygame
from items import items_list
from typing import Dict, Optional

import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

class ImageLoader:
    def __init__(self, variables) -> None:
        self.variables = variables

        self.loaded_item_images: Dict[str, pygame.Surface] = {}
        self.loaded_sprite_images: Dict[str, pygame.Surface] = {}

    def load_gui_image(self, image_name: str) -> Optional[pygame.Surface]:
        """ Renders GUI images and caches them for future use. """
        if image_name not in self.loaded_item_images:
            image_path = f"images/Hud/{image_name}.png"
            if os.path.isfile(image_path):
                loaded_image = pygame.image.load(image_path)
                converted_image = loaded_image.convert_alpha()
                self.loaded_item_images[image_name] = converted_image
                # print(f"{image_path} pre-loaded successfully.")
            else:
                # print(f"Error: '{image_name.capitalize()}' image not found.")
                return None
        return self.loaded_item_images[image_name]

    def load_sprite_image(self, sprite: str) -> Optional[pygame.Surface]:
        """ Caches sprite images for future use. THIS FUNC DOES NOT RENDER IMAGES! """
        image_path = resource_path(f"images/Sprites/{sprite}.png")

        # Check if the sprite image is already loaded
        if sprite in self.loaded_sprite_images:
            return self.loaded_sprite_images[sprite]

        if os.path.isfile(image_path):
            loaded_image = pygame.image.load(image_path)
            converted_image = loaded_image.convert_alpha()
            self.loaded_sprite_images[sprite] = converted_image
            # print(f"{sprite} image ({image_path}) pre-loaded successfully.")
            return converted_image
        else:
            # print(f"Error: '{sprite}' image not found.")
            return None

    @staticmethod
    def get_image_path(image_name: str) -> Optional[str]:
        if image_name.startswith("Ground_"):
            return resource_path(f"images/Items/World/Ground/{image_name}.png")

        if image_name.startswith("Maze_Ground_"):
            return resource_path(f"images/Items/World/{image_name}.png")

        if image_name.startswith("Maze_Wall_"):
            return resource_path(f"images/Items/World/Maze_Wall/{image_name}.png")

        if image_name.startswith("Keyholder_"):
            return resource_path(f"images/Items/World/{image_name}.png")

        if image_name.startswith("Water_"):
            return resource_path(f"images/Items/World/Water/{image_name}.png")

        if image_name.startswith("Farmland_"):
            return resource_path(f"images/Items/World/Farmland/{image_name}.png")

        if image_name.startswith(("Wheat_", "Carrot_", "Potato_", "Corn_")):
            path_name = image_name.split('_')[0]
            return resource_path(f"images/Items/Objects/Farmables/{path_name}/{image_name}.png")

        if image_name.startswith("Maze_End"):
            return resource_path(f"images/Items/World/Closed_Maze_Door.png")

        if image_name.startswith("Maze_Start"):
            return resource_path(f"images/Items/World/Open_Maze_Door.png")

    def get_image_path_with_type(self, image_name: str, type: str = None) -> Optional[str]:
        if type == "Object":
            return resource_path(f"images/Items/Objects/{image_name}.png")
        if type == 'World':
            return resource_path(f"images/Items/World/{image_name}.png")
        if type == "Mineral":
            return resource_path(f"images/Items/Minerals/{image_name}.png")
        if type == "Tool":
            return resource_path(f"images/Items/Tools/{image_name}.png")
        if type == "Consumable":
            return resource_path(f"images/Items/Consumables/{image_name}.png")

    def load_image(self, image_name: str, image_path: str = None) -> Optional[pygame.Surface]:
        """load_image meetod laeb pildid nende "Item" - "Name" ja "Type" järgi ning salvestab need vahemällu edaspidiseks kasutamiseks. SEE FUNC EI VISUALISEERI PILTE!!!!"""
        if not image_name:
            return

        if image_name in self.loaded_item_images:
            return self.loaded_item_images[image_name]

        # Kui on path siis returnib pildi
        if image_path:
            return self._load_and_convert_image(image_path, image_name)

        for item in items_list:
            name = item.name

            # Otsib erandid välja
            image_path = self.get_image_path(image_name)

            if image_path is None:
                if name == image_name:
                    type = item.type
                    image_path = self.get_image_path_with_type(image_name, type)

            if image_path:
                if os.path.isfile(image_path):
                    return self._load_and_convert_image(image_path, image_name)

                # Kui ei leia pilti
                return None

        # Kui ei leia pilti
        return None

    def _load_and_convert_image(self, image_path: str, image_name: str) -> Optional[pygame.Surface]:
        """Utility method to load and convert images."""
        try:
            loaded_image = pygame.image.load(image_path)
            converted_image = loaded_image.convert_alpha()
            self.loaded_item_images[image_name] = converted_image
            return converted_image
        except pygame.error:
            return None
