import pygame
from items import ObjectItem
from typing import Dict, Optional

class ImageLoader:
    loaded_item_images: Dict[str, pygame.Surface] = {}
    loaded_sprite_images: Dict[str, pygame.Surface] = {}

    @staticmethod
    def load_gui_image(image_name: str) -> Optional[pygame.Surface]:
        """ Renderib Gui pildid """

        try:
            if image_name not in ImageLoader.loaded_item_images:
                ImageLoader.loaded_item_images[image_name] = pygame.image.load(f"images/Hud/{image_name}.png")
                print(f"images/Gui/{image_name}.png pre-loaded successfully.")

            return ImageLoader.loaded_item_images[image_name]

        except FileNotFoundError:
            print(f"Error: '{image_name.capitalize()}' image not found.")
            return None
    @staticmethod
    def load_sprite_image(sprite: str) -> Optional[pygame.Surface]:
        """
        Salvestab pildid vahemällu.

        SEE FUNC EI VISUALISEERI PILTE !
        """

        image_path = None

        # Vaatab kas pilt on juba ära laetud
        if sprite in ImageLoader.loaded_sprite_images:
            return ImageLoader.loaded_sprite_images[sprite]

        try:
            image_path = f"images/Sprites/{sprite}.png"
            loaded_image = pygame.image.load(image_path)
            converted_image = loaded_image.convert_alpha()
            ImageLoader.loaded_sprite_images[sprite] = converted_image
            print(f"{sprite} image ({image_path}) pre-loaded successfully.")
            return converted_image

        # Kui Sprite ei ole olemas
        except FileNotFoundError:
            print(f"Error: '{image_path}' image not found.")
            return None

    @staticmethod
    def load_image(image_name: str) -> Optional[pygame.Surface]:
        """ load_image meetod laeb pildid nende "Item" - "Name" ja "Type"
        järgi ning salvestab need vahemällu edaspidiseks kasutamiseks.

                     SEE FUNC EI VISUALISEERI PILTE !!!! """

        try:
            if image_name in ImageLoader.loaded_item_images:
                return ImageLoader.loaded_item_images[image_name]
            else:

                image_path = None

                for item in ObjectItem.instances:
                    name = item.name

                    object_width = item.width
                    object_height = item.height
                    # Peab siin ära LOADima, sest neid ei ole item_list'is
                    if image_name.startswith("Ground_"):
                        image_path = f"images/Objects/Ground/{image_name}.png"
                        name = "Ground"

                    elif image_name.startswith("Water_"):
                        image_path = f"images/Objects/Water/{image_name}.png"
                        name = "Water"

                    elif image_name.startswith("Maze_Wall_"):
                        image_path = f"images/Objects/{image_name}.png"
                        name = "Maze_Wall"

                    elif image_name.startswith("Maze_Ground_"):
                        image_path = f"images/Objects/{image_name}.png"
                        name = "Maze_Ground"

                    elif image_name.startswith("Endgate"):
                        image_path = f"images/Objects/{image_name}.png"
                        name = "Endgate"
                    if image_path == None:
                        # Võtab itemi type ja jagab selle statement'idesse laiali ja 'loadib/convertib/lisab listi'
                        if name == image_name:
                            item_type = item.type

                            if item_type == "Object":
                                image_path = f"images/Objects/{image_name}.png"
                            elif item_type == "Mineral":
                                image_path = f"images/Items/Minerals/{image_name}.png"
                            elif item_type == "Tool":
                                image_path = f"images/Items/Tools/{image_name}.png"

                    if image_path:
                        loaded_image = pygame.image.load(image_path)
                        resized_image = pygame.transform.scale(loaded_image, (object_width, object_height))

                        converted_image = resized_image.convert_alpha()
                        ImageLoader.loaded_item_images[image_name] = converted_image

                        print(f"{image_path} resized and pre-loaded successfully.")
                        return converted_image

                print(f"Error: '{image_name}' image not found.")
                return None

        except FileNotFoundError:
            print(f"Error: '{image_path}' image not found.")
            return None
