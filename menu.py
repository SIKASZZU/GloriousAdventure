import pygame
import sys
import os

from variables import UniversalVariables

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class GameButton:
    def __init__(self, x: float, y: float, image: 'pygame.Surface', scale: float):
        self.image = self._scale_image(image, scale)
        self.rect = self.image.get_rect(topleft=(x, y))

    clicked: bool = False

    def draw(self, surface: 'pygame.Surface') -> bool:
        action: bool = False
        pos: tuple[int, int] = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not GameButton.clicked:
                GameButton.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            GameButton.clicked = False

        surface.blit(self.image, self.rect.topleft)
        return action

    @staticmethod
    def _scale_image(image: 'pygame.Surface', scale: float) -> 'pygame.Surface':
        width, height = image.get_width(), image.get_height()
        return pygame.transform.scale(image, (int(width * scale), int(height * scale)))


def load_and_resize_image(image_path: str) -> 'pygame.Surface':
    original_image = pygame.image.load(image_path).convert_alpha()
    width, height = original_image.get_width(), original_image.get_height()
    resized_image = pygame.transform.scale(original_image, (width * 2, height * 2))
    return resized_image


menu_images = {
    "Play": load_and_resize_image(resource_path("images/Menu_buttons/Play.png")),
    "Settings": load_and_resize_image(resource_path("images/Menu_buttons/Settings.png")),
    "Store": load_and_resize_image(resource_path("images/Menu_buttons/Store.png")),
    "Quit": load_and_resize_image(resource_path("images/Menu_buttons/Quit.png")),
    "Graphics": load_and_resize_image(resource_path("images/Menu_buttons/Graphics.png")),
    "Audio": load_and_resize_image(resource_path("images/Menu_buttons/Audio.png")),
    "Controls": load_and_resize_image(resource_path("images/Menu_buttons/Controls.png")),
    "Back": load_and_resize_image(resource_path("images/Menu_buttons/Back.png")),
    "Resume": load_and_resize_image(resource_path("images/Menu_buttons/Resume.png")),
    "Save_&_Menu": load_and_resize_image(resource_path("images/Menu_buttons/Save_&_Menu.png")),
    "Save_&_Quit": load_and_resize_image(resource_path("images/Menu_buttons/Save_&_Quit.png")),
}


def create_button(x: float, y: float, image: 'pygame.Surface', multiplier: float = None) -> GameButton:
    if not multiplier:
        multiplier = 1
    button = GameButton(x, y, image, multiplier)
    return button


class Menu:
    game_state: bool = True
    game_menu_state: str

    screen = UniversalVariables.screen
    screen_x: int = UniversalVariables.screen_x
    screen_y: int = UniversalVariables.screen_y

    image = resource_path("images/Main_Menu.jpg")
    original_image = pygame.image.load(image).convert()
    main_menu_image = pygame.transform.scale(original_image, (UniversalVariables.screen_x, UniversalVariables.screen_y))

    main_main = [
        create_button(screen_x // 2 - menu_images["Play"].get_width() // 2, screen_y // 3, menu_images["Play"], 1),
        create_button(screen_x // 2 - menu_images["Settings"].get_width() // 2, screen_y // 2, menu_images["Settings"], 1),
        create_button(screen_x - menu_images["Store"].get_width() // 1.3, screen_y // 1.1, menu_images["Store"], 1),
        create_button(screen_x // 2 - menu_images["Quit"].get_width() // 2, screen_y // 1.5, menu_images["Quit"], 1),
    ]

    main_settings = [
        create_button(screen_x // 2 - menu_images["Graphics"].get_width() // 2, screen_y // 6, menu_images["Graphics"], 1),
        create_button(screen_x // 2 - menu_images["Audio"].get_width() // 2, screen_y // 3, menu_images["Audio"], 1),
        create_button(screen_x // 2 - menu_images["Controls"].get_width() // 2, screen_y // 2, menu_images["Controls"], 1),
        create_button(screen_x // 2 - menu_images["Back"].get_width() // 2, screen_y // 1.5, menu_images["Back"], 1),
    ]

    main_store = [
        create_button(screen_x // 2 - menu_images["Back"].get_width() // 2, screen_y // 6, menu_images["Back"], 1),
    ]

    main_graphics = [
        create_button(screen_x // 2 - menu_images["Back"].get_width() // 2, screen_y // 6, menu_images["Back"], 1),
    ]

    main_audio = [
        create_button(screen_x // 2 - menu_images["Back"].get_width() // 2, screen_y // 3, menu_images["Back"], 1),
    ]

    main_controls = [
        create_button(screen_x // 2 - menu_images["Back"].get_width() // 2, screen_y // 2, menu_images["Back"], 1),
    ]

    def main_menu(self) -> None:
        """ See FUNC seadistab 'Main Menu'd.
        Täpsemalt: Siit saab muuta nuppude
        funktsioone ja ülejäänud menu loogikat. """

        self.screen.blit(Menu.main_menu_image, (0, 0))

        if self.game_menu_state == "main":
            if Menu.main_main[0].draw(self.screen):  # Main menu
                Menu.game_state = False  # Paneb mängu tööle

            if Menu.main_main[1].draw(self.screen):  # Settings
                self.game_menu_state = "settings"

            if Menu.main_main[2].draw(self.screen):  # Store
                self.game_menu_state = "store"

            if Menu.main_main[3].draw(self.screen):  # Quit
                pygame.quit()
                sys.exit()

        # Sub-Menu -- Main / Store
        elif self.game_menu_state == "store":
            if Menu.main_store[0].draw(self.screen):  # Main menu
                self.game_menu_state = "main"

        # Sub-Menu -- Main / Settings
        elif self.game_menu_state == "settings":
            if Menu.main_settings[0].draw(self.screen):  # Graphics
                self.game_menu_state = "graphics"

            if Menu.main_settings[1].draw(self.screen):  # Audio
                self.game_menu_state = "audio"

            if Menu.main_settings[2].draw(self.screen):  # Controls
                self.game_menu_state = "controls"

            if Menu.main_settings[3].draw(self.screen):  # Main menu
                self.game_menu_state = "main"

        # Sub-Menu -- Main / Settings / Graphics
        elif self.game_menu_state == "graphics":
            if Menu.main_graphics[0].draw(self.screen):  # Settings
                self.game_menu_state = "settings"

        # Sub-Menu -- Main / Settings / Audio
        elif self.game_menu_state == "audio":
            if Menu.main_audio[0].draw(self.screen):  # Settings
                self.game_menu_state = "settings"

        # Sub-Menu -- Main / Settings / Controls
        elif self.game_menu_state == "controls":
            if Menu.main_controls[0].draw(self.screen):  # Settings
                self.game_menu_state = "settings"


class PauseMenu:
    game_paused = False
    screenshot = None
    pause_menu_state: str

    screen = UniversalVariables.screen
    screen_x: int = UniversalVariables.screen_x
    screen_y: int = UniversalVariables.screen_y

    # Semi-transparent hall pilt
    semi_transparent_color = pygame.Surface((screen_x, screen_y), pygame.SRCALPHA)
    transparency_level = 150  # 0 - 255 // väiksem seda paremini läbi näha
    semi_transparent_color.fill((20, 20, 20, transparency_level))

    pause_main = [
        create_button(screen_x // 2 - menu_images["Resume"].get_width() // 2, screen_y // 6, menu_images["Resume"], 1),
        create_button(screen_x // 2 - menu_images["Settings"].get_width() // 2, screen_y // 3, menu_images["Settings"], 1),
        create_button(screen_x // 2 - menu_images["Save_&_Menu"].get_width() // 2, screen_y // 2, menu_images["Save_&_Menu"], 1),
        create_button(screen_x // 2 - menu_images["Save_&_Quit"].get_width() // 2, screen_y // 1.5, menu_images["Save_&_Quit"], 1),
    ]

    pause_settings = [
        create_button(screen_x // 2 - menu_images["Graphics"].get_width() // 2, screen_y // 6, menu_images["Graphics"], 1),
        create_button(screen_x // 2 - menu_images["Audio"].get_width() // 2, screen_y // 3, menu_images["Audio"], 1),
        create_button(screen_x // 2 - menu_images["Controls"].get_width() // 2, screen_y // 2, menu_images["Controls"], 1),
        create_button(screen_x // 2 - menu_images["Back"].get_width() // 2, screen_y // 1.5, menu_images["Back"], 1),
    ]

    pause_graphics = [
        create_button(screen_x // 2 - menu_images["Back"].get_width() // 2, screen_y // 6, menu_images["Back"], 1),
    ]

    pause_audio = [
        create_button(screen_x // 2 - menu_images["Back"].get_width() // 2, screen_y // 3, menu_images["Back"], 1),

    ]

    pause_controls = [
        create_button(screen_x // 2 - menu_images["Back"].get_width() // 2, screen_y // 2, menu_images["Back"], 1),

    ]

    def settings_menu(self) -> None:
        """ See FUNC seadistab 'Pause Menu'd.
        Täpsemalt: Siit saab muuta nuppude
        funktsioone ja ülejäänud menu loogikat. """
        if self.pause_menu_state == "main":

            # Kaotab muud buttonid ära
            if not PauseMenu.screenshot:
                PauseMenu.screenshot = pygame.display.get_surface().copy()
            self.screen.blit(PauseMenu.screenshot, (0, 0))
            self.screen.blit(PauseMenu.semi_transparent_color, (0, 0))

            if PauseMenu.pause_main[0].draw(self.screen):  # Resume
                PauseMenu.game_paused = False
                PauseMenu.screenshot = None

            if PauseMenu.pause_main[1].draw(self.screen):  # Settings
                self.pause_menu_state = "settings"

            if PauseMenu.pause_main[2].draw(self.screen):  # Save & Menu

                # TODO: Save game
                # Player data - cords, inv, stats(health,hunger, ...)
                # World data - Glade, Maze, placed blocks, Time, Weather, ...
                # Entity data

                PauseMenu.game_paused = False
                Menu.game_state = True

            if PauseMenu.pause_main[3].draw(self.screen):  # Save & Quit
                # TODO: Save game
                # Player data - coords, inv, stats(health,hunger, ...)
                # World data - Glade, Maze, placed blocks, Time, Weather, ...
                # Entity data

                pygame.quit()
                sys.exit()

        # Sub-Menu -- Main / Settings
        elif self.pause_menu_state == "settings":
            self.screen.blit(PauseMenu.screenshot, (0, 0))
            self.screen.blit(PauseMenu.semi_transparent_color, (0, 0))

            if PauseMenu.pause_settings[0].draw(self.screen):  # Graphics
                self.pause_menu_state = "graphics"

            if PauseMenu.pause_settings[1].draw(self.screen):  # Audio
                self.pause_menu_state = "audio"

            if PauseMenu.pause_settings[2].draw(self.screen):  # Controls
                self.pause_menu_state = "controls"

            if PauseMenu.pause_settings[3].draw(self.screen):  # Main menu
                self.pause_menu_state = "main"

        # Sub-Menu -- Main / Settings / Graphics
        elif self.pause_menu_state == "graphics":
            self.screen.blit(PauseMenu.screenshot, (0, 0))
            self.screen.blit(PauseMenu.semi_transparent_color, (0, 0))

            if PauseMenu.pause_graphics[0].draw(self.screen):  # Settings
                self.pause_menu_state = "settings"

        # Sub-Menu -- Main / Settings / Audio
        elif self.pause_menu_state == "audio":
            self.screen.blit(PauseMenu.screenshot, (0, 0))
            self.screen.blit(PauseMenu.semi_transparent_color, (0, 0))

            if PauseMenu.pause_audio[0].draw(self.screen):  # Settings
                self.pause_menu_state = "settings"

        # Sub-Menu -- Main / Settings / Controls
        elif self.pause_menu_state == "controls":
            self.screen.blit(PauseMenu.screenshot, (0, 0))
            self.screen.blit(PauseMenu.semi_transparent_color, (0, 0))

            if PauseMenu.pause_controls[0].draw(self.screen):  # Settings
                self.pause_menu_state = "settings"
