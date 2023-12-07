import pygame
from items import items_list


class ImageLoader:
    loaded_item_images = {}


    def load_gui_image(self, item_name):

        # Mingi glitch sellega
        self.loaded_item_images = ImageLoader.loaded_item_images

        try:
            if item_name not in self.loaded_item_images:
                self.loaded_item_images[item_name] = pygame.image.load(f"images/Gui/{item_name}.PNG")
                print(f"images/Items/{item_name}.PNG pre-loaded successfully.")
            return self.loaded_item_images[item_name]
        except FileNotFoundError:
            print(f"Error: '{item_name.capitalize()}' image not found.")
            return None


    @staticmethod
    def load_image(self, item_name):
        try:
            if item_name in ImageLoader.loaded_item_images:
                return ImageLoader.loaded_item_images[item_name]

            image_path = None

            # Peab siin ära LOADima, sest neid ei ole item_list'is
            if item_name.startswith("Ground_"):
                image_path = f"images/Objects/Ground/{item_name}.PNG"

            elif item_name.startswith("Water_"):
                image_path = f"images/Objects/Water/{item_name}.PNG"

            if image_path:
                loaded_image = pygame.image.load(image_path)
                converted_image = loaded_image.convert_alpha()
                ImageLoader.loaded_item_images[item_name] = converted_image
                print(f"{image_path} pre-loaded successfully.")
                return converted_image

            for item in items_list:
                name = item.get("Name")

                # Võtab itemi type ja jagab selle statement'idesse laiali ja 'loadib/convertib/lisab listi'
                if name == item_name:
                    item_type = item.get("Type")

                    if item_type == "Object":
                        image_path = f"images/Objects/{item_name}.PNG"

                    elif item_type == "Mineral":
                        image_path = f"images/Items/Minerals/{item_name}.PNG"

                    elif item_type == "Tool":
                        image_path = f"images/Items/Tools/{item_name}.PNG"

                    if image_path:
                        loaded_image = pygame.image.load(image_path)
                        converted_image = loaded_image.convert_alpha()
                        ImageLoader.loaded_item_images[item_name] = converted_image
                        print(f"{image_path} pre-loaded successfully.")
                        return converted_image


            #print(f"Error: '{item_name}' image not found.")
            return None

        except FileNotFoundError:
            print(f"Error: '{image_path}' image not found.")
            return None


# Menu pildid
menu_images = {
    "pause_background": pygame.image.load("images/Menu_buttons/pause_background.png").convert_alpha(),
    "resume_img": pygame.image.load("images/Menu_buttons/button_resume.png").convert_alpha(),
    "options_img": pygame.image.load("images/Menu_buttons/button_options.png").convert_alpha(),
    "quit_img": pygame.image.load("images/Menu_buttons/button_quit.png").convert_alpha(),
    "video_img": pygame.image.load('images/Menu_buttons/button_video.png').convert_alpha(),
    "audio_img":  pygame.image.load('images/Menu_buttons/button_audio.png').convert_alpha(),
    "keys_img": pygame.image.load('images/Menu_buttons/button_keys.png').convert_alpha(),
    "back_img": pygame.image.load('images/Menu_buttons/button_back.png').convert_alpha()
}

water_images = {
    "Water_0": pygame.image.load("images/Objects/Water/Water_0.png")
}

