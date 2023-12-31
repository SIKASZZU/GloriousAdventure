import pygame
from items import items_list
from typing import Dict, Optional
from variables import Decorators

# Menu pildid
pause_menu_images = {
    "resume_img": pygame.image.load("images/Menu_buttons/button_resume.png").convert_alpha(),
    "options_img": pygame.image.load("images/Menu_buttons/button_options.png").convert_alpha(),
    "quit_img": pygame.image.load("images/Menu_buttons/button_quit.png").convert_alpha(),
    "video_img": pygame.image.load('images/Menu_buttons/button_video.png').convert_alpha(),
    "audio_img":  pygame.image.load('images/Menu_buttons/button_audio.png').convert_alpha(),
    "keys_img": pygame.image.load('images/Menu_buttons/button_keys.png').convert_alpha(),
    "back_img": pygame.image.load('images/Menu_buttons/button_back.png').convert_alpha()
}


class ImageLoader:
    loaded_item_images: Dict[str, pygame.Surface] = {}

    @staticmethod
    ### TODO: Tuleks panna load_image funci sisse
    def load_gui_image(image_name: str) -> Optional[pygame.Surface]:
        """ Renderib Gui pildid """

        try:
            if image_name not in ImageLoader.loaded_item_images:
                ImageLoader.loaded_item_images[image_name] = pygame.image.load(f"images/Gui/{image_name}.PNG")
                print(f"images/Gui/{image_name}.PNG pre-loaded successfully.")

            return ImageLoader.loaded_item_images[image_name]

        except FileNotFoundError:
            print(f"Error: '{image_name.capitalize()}' image not found.")
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

                # Peab siin ära LOADima, sest neid ei ole item_list'is
                if image_name.startswith("Ground_"):
                    image_path = f"images/Objects/Ground/{image_name}.PNG"

                elif image_name.startswith("Water_"):
                    image_path = f"images/Objects/Water/{image_name}.PNG"

                if image_path:
                    loaded_image = pygame.image.load(image_path)
                    converted_image = loaded_image.convert_alpha()
                    ImageLoader.loaded_item_images[image_name] = converted_image
                    print(f"{image_path} pre-loaded successfully.")
                    return converted_image

                for item in items_list:
                    name = item.get("Name")

                    # Võtab itemi type ja jagab selle statement'idesse laiali ja 'loadib/convertib/lisab listi'
                    if name == image_name:
                        item_type = item.get("Type")

                        if item_type == "Object":
                            image_path = f"images/Objects/{image_name}.PNG"
                        elif item_type == "Mineral":
                            image_path = f"images/Items/Minerals/{image_name}.PNG"
                        elif item_type == "Tool":
                            image_path = f"images/Items/Tools/{image_name}.PNG"

                        if image_path:
                            loaded_image = pygame.image.load(image_path)
                            converted_image = loaded_image.convert_alpha()
                            ImageLoader.loaded_item_images[image_name] = converted_image
                            print(f"{image_path} pre-loaded successfully.")
                            return converted_image

                print(f"Error: '{image_name}' image not found.")
                return None

        except FileNotFoundError:
            print(f"Error: '{image_path}' image not found.")
            return None
