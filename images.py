import pygame
from items import items_list, items_dict_by_name
from typing import Dict, Optional
from functools import lru_cache
import sys
import os
from variables import UniversalVariables
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        #print('try', base_path)
    except AttributeError:
        base_path = os.path.abspath(".")
        #print('base', base_path)

        #print('returns', os.path.join(base_path, relative_path))
    return os.path.join(base_path, relative_path)

class ImageLoader:
    loaded_item_images: Dict[str, pygame.Surface] = {}
    loaded_sprite_images: Dict[str, pygame.Surface] = {}

    @staticmethod
    def load_gui_image(image_name: str) -> Optional[pygame.Surface]:
        """ Renderib Gui pildid """
        try:
            if image_name not in ImageLoader.loaded_item_images:
                ImageLoader.loaded_item_images[image_name] = pygame.image.load(f"images/Hud/{image_name}.png")
                # print(f"images/Gui/{image_name}.png pre-loaded successfully.")

            return ImageLoader.loaded_item_images[image_name]
        except FileNotFoundError:
            # print(f"Error: '{image_name.capitalize()}' image not found.")
            return None

    @staticmethod
    def load_sprite_image(sprite: str) -> Optional[pygame.Surface]:
        """Salvestab pildid vahemällu. SEE FUNC EI VISUALISEERI PILTE!"""
        image_path = None
        # Vaatab kas pilt on juba ära laetud
        if sprite in ImageLoader.loaded_sprite_images:
            return ImageLoader.loaded_sprite_images[sprite]

        try:
            image_path = resource_path(f"images/Sprites/{sprite}.png")
            loaded_image = pygame.image.load(image_path)
            converted_image = loaded_image.convert_alpha()
            ImageLoader.loaded_sprite_images[sprite] = converted_image
            # print(f"{sprite} image ({image_path}) pre-loaded successfully.")
            return converted_image
        except FileNotFoundError:
            # print(f"Error: '{image_path}' image not found.")
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

    @staticmethod
    def get_image_path_with_type(image_name: str, type: str = None) -> Optional[str]:
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

    @staticmethod
    def load_image(image_name: str, image_path: str = None) -> Optional[pygame.Surface]:
        """load_image meetod laeb pildid nende "Item" - "Name" ja "Type" järgi ning salvestab need vahemällu edaspidiseks kasutamiseks. SEE FUNC EI VISUALISEERI PILTE!!!!"""
        if not image_name:
            return

        if image_name in ImageLoader.loaded_item_images:
            return ImageLoader.loaded_item_images[image_name]

        # Kui on path siis returnib pildi
        if image_path:
            loaded_image = pygame.image.load(resource_path(image_path))
            converted_image = loaded_image.convert_alpha()
            ImageLoader.loaded_item_images[image_name] = converted_image
            return converted_image

        for item in items_list:
            name = item.name

            # Otsib erandid välja
            image_path = ImageLoader.get_image_path(image_name)

            if image_path is None:
                if name == image_name:
                    type = item.type
                    image_path = ImageLoader.get_image_path_with_type(image_name, type)

            if image_path:
                if os.path.isfile(image_path):
                    loaded_image = pygame.image.load(image_path)
                    converted_image = loaded_image.convert_alpha()
                    ImageLoader.loaded_item_images[image_name] = converted_image

                    return converted_image

                # Kui ei leia pilti
                return None

        # Kui ei leia pilti
        return None
