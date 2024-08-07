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
                    name = item.get("Name")
                    object_width = item.get("Object_width")
                    object_height = item.get("Object_height")
                    # Peab siin ära LOADima, sest neid ei ole item_list'is
                    if image_name.startswith("Ground_"):
                        image_path = resource_path(f"images/Objects/Ground/{image_name}.png")
                        name = "Ground"
                    elif image_name.startswith("Water_"):
                        image_path = resource_path(f"images/Objects/Water/{image_name}.png")
                        name = "Water"
                    elif image_name.startswith("Maze_Wall_"):
                        image_path = resource_path(f"images/Objects/Maze_Wall/{image_name}.png")
                        name = "Maze_Wall"
                    elif image_name.startswith("Maze_Ground_"):
                        image_path = resource_path(f"images/Objects/{image_name}.png")
                        name = "Maze_Ground"
                    elif image_name.startswith("Endgate"):
                        image_path = resource_path(f"images/Objects/{image_name}.png")
                        name = "Endgate"
                    elif image_name.startswith("Farmland_"):
                        image_path = resource_path(f"images/Objects/Farmland/{image_name}.png")
                        name = "Farmland"

                    if image_path is None:
                        # Võtab itemi type ja jagab selle statement'idesse laiali ja 'loadib/convertib/lisab listi'
                        if name == image_name:
                            item_type = item.get("Type")
                            if item_type == "Object":
                                image_path = resource_path(f"images/Objects/{image_name}.png")
                            elif item_type == "Mineral":
                                image_path = resource_path(f"images/Items/Minerals/{image_name}.png")
                            elif item_type == "Tool":
                                image_path = resource_path(f"images/Items/Tools/{image_name}.png")
                            elif item_type == "Food":
                                image_path = resource_path(f"images/Items/Foods/{image_name}.png")

                    if image_path:
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


                # print(f"Error: '{image_name}' image not found.")
                return None
        except FileNotFoundError:
            # print(f"Error: '{image_path}' image not found.")
            return None

class ImageCache:
    @staticmethod
    @lru_cache(maxsize=128)
    def load_item_image(item_name):
        return ImageLoader.load_image(item_name)

    @staticmethod
    @lru_cache(maxsize=128)
    def load_resized_item_image(item_name, max_size):
        item_image = ImageLoader.load_image(item_name)
        return pygame.transform.scale(item_image, max_size)