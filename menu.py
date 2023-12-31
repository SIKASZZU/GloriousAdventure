import pygame
import sys

from variables import UniversalVariables
from images import pause_menu_images


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    clicked = False  # Kui see on self.clicked, siis tekib mitu inputi

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not Button.clicked:
                Button.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            Button.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


class Menu:
    game_state: bool
    settings_category: bool
    game_menu_state: str

    screen = UniversalVariables.screen
    screen_x: int = UniversalVariables.screen_x
    screen_y: int = UniversalVariables.screen_y
    block_size: int = UniversalVariables.block_size

    @staticmethod
    def load_and_resize_image(image_path):
        original_image = pygame.image.load(image_path).convert_alpha()
        width, height = original_image.get_width(), original_image.get_height()
        resized_image = pygame.transform.scale(original_image, (width * 2, height * 2))
        return resized_image

    menu_images = {
        "Play": load_and_resize_image("images/Menu_buttons/Play.png"),
        "Settings": load_and_resize_image("images/Menu_buttons/Settings.png"),
        "Store": load_and_resize_image("images/Menu_buttons/Store.png"),
        "Quit": load_and_resize_image("images/Menu_buttons/Quit.png"),
        "Graphics": load_and_resize_image("images/Menu_buttons/Graphics.png"),
        "Audio": load_and_resize_image("images/Menu_buttons/Audio.png"),
        "Controls": load_and_resize_image("images/Menu_buttons/Controls.png"),
        "Back": load_and_resize_image("images/Menu_buttons/Back.png"),
    }

    # Main menu
    play_button = Button(screen_x // 2 - menu_images["Play"].get_width() // 2, screen_y // 3, menu_images["Play"], 1)
    settings_button = Button(screen_x // 2 - menu_images["Settings"].get_width() // 2, screen_y // 2, menu_images["Settings"], 1)
    quit_button = Button(screen_x // 2 - menu_images["Quit"].get_width() // 2, screen_y // 1.5, menu_images["Quit"], 1)
    store_button = Button(screen_x - menu_images["Store"].get_width() / 1.3, screen_y - menu_images["Store"].get_height() * 1.1, menu_images["Store"], 1)

    # Settings menu
    graphics_button = Button(screen_x // 2 - menu_images["Graphics"].get_width() // 2, screen_y // 6, menu_images["Graphics"], 1)
    audio_button = Button(screen_x // 2 - menu_images["Audio"].get_width() // 2, screen_y // 3, menu_images["Audio"], 1)
    controls_button = Button(screen_x // 2 - menu_images["Controls"].get_width() // 2, screen_y // 2, menu_images["Controls"], 1)
    back_button = Button(screen_x // 2 - menu_images["Back"].get_width() // 2, screen_y // 1.5, menu_images["Back"], 1)

    def menu(self):
        """ See FUNC seadistab 'Main Menu'd.
        Täpsemalt: Siit saab muuta nuppude
        funktsioone ja ülejäänud menu loogikat. """

        # See on mängu main menu
        if self.game_menu_state == "main":
            if Menu.play_button.draw(self.screen):
                self.game_state = False  # Start the game

            if Menu.settings_button.draw(self.screen):  # Settings
                self.game_menu_state = "settings"

            if Menu.store_button.draw(self.screen):  # Store
                self.game_menu_state = "store"

            if Menu.quit_button.draw(self.screen):  # Paneb mängu kinni
                pygame.quit()
                sys.exit()

        # Kui mingi settingutesse
        elif self.game_menu_state == "settings":
            if Menu.graphics_button.draw(self.screen):  # Graphics
                self.game_menu_state = "graphics"

            if Menu.audio_button.draw(self.screen):  # Audio
                self.game_menu_state = "audio"

            if Menu.controls_button.draw(self.screen):  # Controls
                self.game_menu_state = "controls"

            if Menu.back_button.draw(self.screen):  # Tagasi Main Menu'sse
                self.game_menu_state = "main"

        # Kui mingi store'i
        elif self.game_menu_state == "store":
            if Menu.back_button.draw(self.screen):  # Tagasi Main Menu'sse
                self.game_menu_state = "main"

        # Kui mingi settings - graphics
        elif self.game_menu_state == "graphics":
            if Menu.back_button.draw(self.screen):  # Tagasi Settings'utesse
                self.game_menu_state = "settings"

        # Kui mingi settings - audio
        elif self.game_menu_state == "audio":
            if Menu.back_button.draw(self.screen):  # Tagasi Settings'utesse
                self.game_menu_state = "settings"

        # Kui mingi settings - controls
        elif self.game_menu_state == "controls":
            if Menu.back_button.draw(self.screen):  # Tagasi Settings'utesse
                self.game_menu_state = "settings"

class PauseMenu:
    game_paused: bool
    game_state: bool
    pause_menu_state: str

    screen = UniversalVariables.screen
    screen_x = UniversalVariables.screen_x
    resume_button = Button(screen_x / 2 - 100, 175, pause_menu_images["resume_img"], 1)
    options_button = Button(screen_x / 2 - 106, 300, pause_menu_images["options_img"], 1)
    video_button = Button(screen_x / 2 - 178, 125, pause_menu_images["video_img"], 1)
    audio_button = Button(screen_x / 2 - 179, 250, pause_menu_images["audio_img"], 1)
    keys_button = Button(screen_x / 2 - 159, 375, pause_menu_images["keys_img"], 1)
    back_button = Button(screen_x / 2 - 72, 500, pause_menu_images["back_img"], 1)
    quit_button = Button(screen_x / 2 - 69, 425, pause_menu_images["quit_img"], 1)

    def settings_menu(self):
        if self.pause_menu_state == "main":

            if PauseMenu.resume_button.draw(self.screen):
                self.game_paused = False
            if PauseMenu.options_button.draw(self.screen):
                self.pause_menu_state = "options"
            if PauseMenu.quit_button.draw(self.screen):
                pygame.quit()
                sys.exit()

        # TODO: Tuleb main menuga samasuguseks teha
        if self.pause_menu_state == "options":

            if PauseMenu.video_button.draw(self.screen):    # See tuleb ära muuta
                print("Video Settings")
            if PauseMenu.audio_button.draw(self.screen):    # See tuleb ära muuta
                print("Audio Settings")
            if PauseMenu.keys_button.draw(self.screen):     # See tuleb ära muuta
                print("Change Key Bindings")

            # if PauseMenu.save_button.draw(self.screen):   # Save game
            #     self.game_state = True                    # Save game
            #     self.game_paused = False                  # Save game

            if PauseMenu.back_button.draw(self.screen):
                self.pause_menu_state = "main"
