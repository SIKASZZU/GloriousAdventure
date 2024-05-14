import pygame
from typing import Dict, Optional
from items import ObjectItem, MineralItem, ToolItem


class ImageLoader:
    loaded_hud_images: Dict[str, pygame.Surface] = {}
    loaded_sprite_images: Dict[str, pygame.Surface] = {}
    loaded_item_images: Dict[str, pygame.Surface] = {}

    @staticmethod
    def load_hud_image(hud: str) -> Optional[pygame.Surface]:
        """
        Salvestab pildid vahemällu.

        SEE FUNC EI VISUALISEERI PILTE !
        """

        image_path = None

        # Vaatab kas pilt on juba ära laetud
        if hud in ImageLoader.loaded_hud_images:
            return ImageLoader.loaded_hud_images[hud]

        try:
            image_path = f"Images/Hud/{hud}.PNG"
            loaded_image = pygame.image.load(image_path)
            converted_image = loaded_image.convert_alpha()
            ImageLoader.loaded_hud_images[hud] = converted_image
            print(f"{hud} image ({image_path}) pre-loaded successfully.")
            return converted_image

        # Kui Hud ei ole olemas
        except FileNotFoundError:
            print(f"Error: '{image_path}' image not found.")
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
            image_path = f"Images/Sprites/{sprite}.png"
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
    def load_debug_image(debug: str) -> Optional[pygame.Surface]:
        """
        Salvestab pildid vahemällu.

        SEE FUNC EI VISUALISEERI PILTE !
        """

        image_path = None

        # Vaatab kas pilt on juba ära laetud
        if debug in ImageLoader.loaded_sprite_images:
            return ImageLoader.loaded_sprite_images[debug]

        try:
            image_path = f"Images/Debug/{debug}.png"
            loaded_image = pygame.image.load(image_path)
            converted_image = loaded_image.convert_alpha()
            ImageLoader.loaded_sprite_images[debug] = converted_image
            print(f"{debug} image ({image_path}) pre-loaded successfully.")
            return converted_image

        # Kui Sprite ei ole olemas
        except FileNotFoundError:
            print(f"Error: '{image_path}' image not found.")
            return None

    @staticmethod
    def load_item_image(item_name: str) -> Optional[pygame.Surface]:
        """
        Salvestab pildid vahemällu.

        SEE FUNC EI VISUALISEERI PILTE !
        """

        # Vaatab kas pilt on juba ära laetud
        if item_name in ImageLoader.loaded_item_images:
            print(item_name, 'item_name')
            return ImageLoader.loaded_item_images[item_name]

        # Func, et laadida ja mahutada pilti
        def load_and_store(image_path: str):
            try:
                loaded_image = pygame.image.load(image_path)
                converted_image = loaded_image.convert_alpha()
                ImageLoader.loaded_item_images[item_name] = converted_image
                print(f"{item_name} image ({image_path}) pre-loaded successfully.")
                print(ImageLoader.loaded_item_images)
                return converted_image

            except FileNotFoundError:
                print(f"Error: '{image_path}' image not found.")
                return None

        # Vaatab kõik itemid läbi
        for item_list in [ObjectItem.instances, MineralItem.instances, ToolItem.instances]:
            for item in item_list:
                if item.name.startswith("Ground_"):
                    image_path = f"images/Objects/Ground/{item.name}.png"
                    name = "Ground"

                elif item.name.startswith("Water_"):
                    image_path = f"images/Objects/Water/{item.name}.png"
                    name = "Water"

                elif item.name.startswith("Maze_Wall_"):
                    image_path = f"images/Objects/{item.name}.png"
                    name = "Maze_Wall"

                elif item.name.startswith("Maze_Ground_"):
                    image_path = f"images/Objects/{item.name}.png"
                    name = "Maze_Ground"

                elif item.name.startswith("Endgate"):
                    image_path = f"images/Objects/{item.name}.png"
                    name = "Endgate"

                print(item_name) 
                return load_and_store(image_path)

        # Kui itemit ei ole olemas
        print(f"Error: '{item_name}' image not found.")
        return None

# Testida asju mis on seotud ainult item.py'ga
if __name__ == "__main__":
    pass
