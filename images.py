import pygame
from items import items_list
from typing import Dict, Optional
from functools import lru_cache
import sys
import os

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
    def load_image(image_name: str, image_path: str = None) -> Optional[pygame.Surface]:
        """load_image meetod laeb pildid nende "Item" - "Name" ja "Type" järgi ning salvestab need vahemällu edaspidiseks kasutamiseks. SEE FUNC EI VISUALISEERI PILTE!!!!"""
        try:
            if image_name in ImageLoader.loaded_item_images:
                return ImageLoader.loaded_item_images[image_name]

            elif image_path:
                if image_path.startswith(resource_path("images/Objects")):
                    loaded_image = pygame.image.load(image_path)
                    resized_image = pygame.transform.scale(loaded_image, (object_width, object_height))
                    converted_image = resized_image.convert_alpha()
                    ImageLoader.loaded_item_images[image_name] = converted_image

                    print(image_path, loaded_image, resized_image, converted_image)

                    # print(f"{image_path} resized and pre-loaded successfully.")
                    return converted_image
                else:
                    loaded_image = pygame.image.load(image_path)
                    converted_image = loaded_image.convert_alpha()
                    ImageLoader.loaded_item_images[image_name] = converted_image

                    # print(f"{image_path} resized and pre-loaded successfully.")
                    return converted_image

            else:
                image_path = None

                for item in items_list:

                    name = item.name

                    # Peab siin ära LOADima, sest neid ei ole item_list'is
                    if image_name.startswith("Ground_"):
                        image_path = resource_path(f"images/Items/World/Ground/{image_name}.png")
                        name = "Ground"
                    elif image_name.startswith("Water_"):
                        image_path = resource_path(f"images/Items/World/Water/{image_name}.png")
                        name = "Water"
                    elif image_name.startswith("Maze_Wall_"):
                        image_path = resource_path(f"images/Items/World/Maze_Wall/{image_name}.png")
                        name = "Maze_Wall"
                    elif image_name.startswith("Maze_Ground_"):
                        image_path = resource_path(f"images/Items/World/{image_name}.png")
                        name = "Maze_Ground"
                    elif image_name.startswith("Endgate"):
                        image_path = resource_path(f"images/Items/World/{image_name}.png")
                        name = "Endgate"
                    elif image_name.startswith("Farmland_"):
                        image_path = resource_path(f"images/Items/World/Farmland/{image_name}.png")
                        name = "Farmland"
                    elif image_name.startswith("Wheat_Sapling"):
                        image_path = resource_path(f"images/Items/Objects/Wheat/{image_name}.png")
                        name = "Wheat_Sapling"

                    if image_path is None:
                        # Võtab itemi type ja jagab selle statement'idesse laiali ja 'loadib/convertib/lisab listi'
                        if name == image_name:

                            type = item.type

                            if type == "Object":
                                image_path = resource_path(f"images/Items/Objects/{image_name}.png")
                            elif type == 'World':
                                image_path = resource_path(f"images/Items/World/{image_name}.png")
                            elif type == "Mineral":
                                image_path = resource_path(f"images/Items/Minerals/{image_name}.png")
                            elif type == "Tool":
                                image_path = resource_path(f"images/Items/Tools/{image_name}.png")
                            elif type == "Consumable":
                                image_path = resource_path(f"images/Items/Consumables/{image_name}.png")


                    if image_path:
                        if image_path.startswith(resource_path("images/Objects")):
                            print(image_path, image_name)
                            object_width = item.width
                            object_height = item.height

                            loaded_image = pygame.image.load(image_path)
                            resized_image = pygame.transform.scale(loaded_image, (object_width, object_height))
                            converted_image = resized_image.convert_alpha()
                            ImageLoader.loaded_item_images[image_name] = converted_image

                            print(image_path, loaded_image, resized_image, converted_image)

                            # print(f"{image_path} resized and pre-loaded successfully.")
                            return converted_image
                        else:
                            loaded_image = pygame.image.load(image_path)
                            converted_image = loaded_image.convert_alpha()
                            ImageLoader.loaded_item_images[image_name] = converted_image

                            # print(f"{image_path} resized and pre-loaded successfully.")
                            return converted_image


                # print(f"Error: '{image_name}' image not found.")
                return None
        except FileNotFoundError:
            # print(f"Error: '{image_path}' image not found.")
            return None

class ImageCache:
    @staticmethod
    @lru_cache(maxsize=128)
    def load_item_image(name):
        return ImageLoader.load_image(name)

    @staticmethod
    @lru_cache(maxsize=128)
    def load_resized_item_image(name, max_size):
        item_image = ImageLoader.load_image(name)
        return pygame.transform.scale(item_image, max_size)