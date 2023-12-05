import pygame

### TODO: Hetkel on lic nii tehtud, et ta tuleb listi juurde ja loadib.
### TODO: Kui me preloadime imageid siis see võtab vähem ruumi ja  peformancei.

# item_images = {}
# image_names = ["Oak_Tree", "Stone", "Rock", "Monke", "Flower", "Mushroom", "Wheat"]
#
# try:
#     for name in image_names:
#         item_images[name] = pygame.image.load(f"images/Items/{name}.PNG")
#         print(f"images/{name}.PNG")
#
# except FileNotFoundError:
#     print(f"Error in images.py! Name: '{name.capitalize()}' not in list.")


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

# Itemite pildid
item_images = {
    "Oak_Tree": pygame.image.load("images/Items/Oak_Tree.PNG"),
    "Stone": pygame.image.load("images/Items/Stone.PNG"),
    "Rock": pygame.image.load("images/Items/Rock.PNG"),
    "Flower": pygame.image.load("images/Items/Flower.PNG"),
    "Mushroom": pygame.image.load("images/Items/Mushroom.PNG"),
    "Wheat": pygame.image.load("images/Items/Wheat.PNG"),
    "Oak_Wood": pygame.image.load("images/Items/Oak_Wood.PNG"),
    "Oak_Planks": pygame.image.load("images/Items/Oak_Planks.PNG"),
    "Stick": pygame.image.load("images/Items/Stick.PNG"),
    "Wood_Pickaxe": pygame.image.load("images/Items/Wood_Pickaxe.PNG"),
    "Wood_Axe": pygame.image.load("images/Items/Wood_Axe.PNG"),
    "Wood_Shovel": pygame.image.load("images/Items/Wood_Shovel.PNG"),
    "Stone_Shard": pygame.image.load("images/Items/Stone_Shard.PNG"),
    "Coal": pygame.image.load("images/Items/Coal.PNG"),
    "Torch": pygame.image.load("images/Items/Torch.gif"),
    "Small_Rock_Sword": pygame.image.load("images/Items/Small_Rock_Sword.PNG"),
    # "": pygame.image.load("images/.PNG"),
}

# Maa pildid
ground_images = {
    "Ground_0": pygame.image.load("images/Ground/Ground_0.png"),
    "Ground_1": pygame.image.load("images/Ground/Ground_1.png"),
    "Ground_2": pygame.image.load("images/Ground/Ground_2.png"),
    "Ground_3": pygame.image.load("images/Ground/Ground_3.png"),
    "Ground_4": pygame.image.load("images/Ground/Ground_4.png"),
    "Ground_5": pygame.image.load("images/Ground/Ground_5.png"),
    "Ground_6": pygame.image.load("images/Ground/Ground_6.png"),
    "Ground_7": pygame.image.load("images/Ground/Ground_7.png"),
    "Ground_8": pygame.image.load("images/Ground/Ground_8.png"),
    "Ground_9": pygame.image.load("images/Ground/Ground_9.png"),
    "Ground_10": pygame.image.load("images/Ground/Ground_10.png"),
    "Ground_11": pygame.image.load("images/Ground/Ground_11.png"),
    "Ground_12": pygame.image.load("images/Ground/Ground_12.png"),
    "Ground_13": pygame.image.load("images/Ground/Ground_13.png"),
    "Ground_14": pygame.image.load("images/Ground/Ground_14.png"),
    "Ground_15": pygame.image.load("images/Ground/Ground_15.png"),
    "Ground_16": pygame.image.load("images/Ground/Ground_16.png"),
    "Ground_17": pygame.image.load("images/Ground/Ground_17.png"),
    "Ground_18": pygame.image.load("images/Ground/Ground_18.png"),
    "Ground_19": pygame.image.load("images/Ground/Ground_19.png"),
}

water_images = {
    "Water_0": pygame.image.load("images/Water/Water_0.png")
}

