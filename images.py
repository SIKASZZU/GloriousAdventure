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


    ### TODO: Ei tööta, ei tea miks
    def load_image(self, item_name):
        try:
            if item_name in ImageLoader.loaded_item_images:
                return ImageLoader.loaded_item_images.get(item_name)

            for item in items_list:
                name = item.get("Name")

                if name == item_name:
                    image_path = None
                    item_type = item.get("Type")

                    if item_type == "Ground":
                        image_path = f"images/Objects/Ground/{item_name}.PNG"

                    elif item_type == "Water":
                        image_path = f"images/Objects/Water/{item_name}.PNG"

                    elif item_type == "Object":
                        image_path = f"images/Objects/{item_name}.PNG"

                    elif item_type == "Mineral":
                        image_path = f"images/Items/Minerals/{item_name}.PNG"

                    elif item_type == "Tool":
                        image_path = f"images/Items/Tools/{item_name}.PNG"

                    if image_path:
                        ImageLoader.loaded_item_images[item_name] = pygame.image.load(image_path)
                        print(f"{image_path} pre-loaded successfully.")
                        return ImageLoader.loaded_item_images[item_name]

            print(f"Error: '{item_name}' image not found.")
            return None

        except FileNotFoundError:
            print(f"Error: '{item_name}' image not found.")
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

# Maa pildid
ground_images = {
    "Ground_0": pygame.image.load("images/Objects/Ground/Ground_0.png"),
    "Ground_1": pygame.image.load("images/Objects/Ground/Ground_1.png"),
    "Ground_2": pygame.image.load("images/Objects/Ground/Ground_2.png"),
    "Ground_3": pygame.image.load("images/Objects/Ground/Ground_3.png"),
    "Ground_4": pygame.image.load("images/Objects/Ground/Ground_4.png"),
    "Ground_5": pygame.image.load("images/Objects/Ground/Ground_5.png"),
    "Ground_6": pygame.image.load("images/Objects/Ground/Ground_6.png"),
    "Ground_7": pygame.image.load("images/Objects/Ground/Ground_7.png"),
    "Ground_8": pygame.image.load("images/Objects/Ground/Ground_8.png"),
    "Ground_9": pygame.image.load("images/Objects/Ground/Ground_9.png"),
    "Ground_10": pygame.image.load("images/Objects/Ground/Ground_10.png"),
    "Ground_11": pygame.image.load("images/Objects/Ground/Ground_11.png"),
    "Ground_12": pygame.image.load("images/Objects/Ground/Ground_12.png"),
    "Ground_13": pygame.image.load("images/Objects/Ground/Ground_13.png"),
    "Ground_14": pygame.image.load("images/Objects/Ground/Ground_14.png"),
    "Ground_15": pygame.image.load("images/Objects/Ground/Ground_15.png"),
    "Ground_16": pygame.image.load("images/Objects/Ground/Ground_16.png"),
    "Ground_17": pygame.image.load("images/Objects/Ground/Ground_17.png"),
    "Ground_18": pygame.image.load("images/Objects/Ground/Ground_18.png"),
    "Ground_19": pygame.image.load("images/Objects/Ground/Ground_19.png"),
}

water_images = {
    "Water_0": pygame.image.load("images/Objects/Water/Water_0.png")
}

