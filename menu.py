import pygame
import sys
import os


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
    "Play": load_and_resize_image(resource_path("images/Menu/Play.png")),
    "Settings": load_and_resize_image(resource_path("images/Menu/Settings.png")),
    "Store": load_and_resize_image(resource_path("images/Menu/Store.png")),
    "Quit": load_and_resize_image(resource_path("images/Menu/Quit.png")),
    "Graphics": load_and_resize_image(resource_path("images/Menu/Graphics.png")),
    "Audio": load_and_resize_image(resource_path("images/Menu/Audio.png")),
    "Controls": load_and_resize_image(resource_path("images/Menu/Controls.png")),
    "Back": load_and_resize_image(resource_path("images/Menu/Back.png")),
    "Resume": load_and_resize_image(resource_path("images/Menu/Resume.png")),
    "Save_&_Menu": load_and_resize_image(resource_path("images/Menu/Save_&_Menu.png")),
    "Save_&_Quit": load_and_resize_image(resource_path("images/Menu/Save_&_Quit.png")),
}


def create_button(x: float, y: float, image: 'pygame.Surface', multiplier: float = None) -> GameButton:
    if not multiplier:
        multiplier = 1
    button = GameButton(x, y, image, multiplier)
    return button


class Menu:
    def __init__(self, variables):
        self.variables = variables
            
        if self.variables.debug_mode:
            self.game_state: bool = False
            self.game_menu_state: str

        else:
            self.game_state: bool = True
            self.game_menu_state: str

        self.screen = self.variables.screen
        self.screen_x: int = self.variables.screen_x
        self.screen_y: int = self.variables.screen_y

        self.image = resource_path("images/Menu/Main_Menu.png")
        self.original_image = pygame.image.load(self.image).convert()
        self.main_menu_image = pygame.transform.scale(self.original_image, (self.variables.screen_x, self.variables.screen_y))

        self.main_main = [
            create_button(self.screen_x // 2 - menu_images["Play"].get_width() // 2, self.screen_y // 3, menu_images["Play"], 1),
            create_button(self.screen_x // 2 - menu_images["Settings"].get_width() // 2, self.screen_y // 2, menu_images["Settings"], 1),
            create_button(self.screen_x - menu_images["Store"].get_width() // 1.3, self.screen_y // 1.1, menu_images["Store"], 1),
            create_button(self.screen_x // 2 - menu_images["Quit"].get_width() // 2, self.screen_y // 1.5, menu_images["Quit"], 1),
        ]

        self.main_settings = [
            create_button(self.screen_x // 2 - menu_images["Graphics"].get_width() // 2, self.screen_y // 6, menu_images["Graphics"], 1),
            create_button(self.screen_x // 2 - menu_images["Audio"].get_width() // 2, self.screen_y // 3, menu_images["Audio"], 1),
            create_button(self.screen_x // 2 - menu_images["Controls"].get_width() // 2, self.screen_y // 2, menu_images["Controls"], 1),
            create_button(self.screen_x // 2 - menu_images["Back"].get_width() // 2, self.screen_y // 1.5, menu_images["Back"], 1),
        ]

        self.main_store = [
            create_button(self.screen_x // 2 - menu_images["Back"].get_width() // 2, self.screen_y // 6, menu_images["Back"], 1),
        ]

        self.main_graphics = [
            create_button(self.screen_x // 2 - menu_images["Back"].get_width() // 2, self.screen_y // 6, menu_images["Back"], 1),
        ]

        self.main_audio = [
            create_button(self.screen_x // 2 - menu_images["Back"].get_width() // 2, self.screen_y // 3, menu_images["Back"], 1),
        ]

        self.main_controls = [
            create_button(self.screen_x // 2 - menu_images["Back"].get_width() // 2, self.screen_y // 2, menu_images["Back"], 1),
        ]

    def main_menu(self) -> None:
        """ See FUNC seadistab 'Main Menu'd.
        Täpsemalt: Siit saab muuta nuppude
        funktsioone ja ülejäänud menu loogikat. """

        self.screen.blit(self.main_menu_image, (0, 0))

        if self.game_menu_state == "main":
            if self.main_main[0].draw(self.screen):  # Main menu
                self.game_state = False  # Paneb mängu tööle

            if self.main_main[1].draw(self.screen):  # Settings
                self.game_menu_state = "settings"

            if self.main_main[2].draw(self.screen):  # Store
                self.game_menu_state = "store"

            if self.main_main[3].draw(self.screen):  # Quit
                pygame.quit()
                sys.exit()

        # Sub-Menu -- Main / Store
        elif self.game_menu_state == "store":
            if self.main_store[0].draw(self.screen):  # Main menu
                self.game_menu_state = "main"

        # Sub-Menu -- Main / Settings
        elif self.game_menu_state == "settings":
            if self.main_settings[0].draw(self.screen):  # Graphics
                self.game_menu_state = "graphics"

            if self.main_settings[1].draw(self.screen):  # Audio
                self.game_menu_state = "audio"

            if self.main_settings[2].draw(self.screen):  # Controls
                self.game_menu_state = "controls"

            if self.main_settings[3].draw(self.screen):  # Main menu
                self.game_menu_state = "main"

        # Sub-Menu -- Main / Settings / Graphics
        elif self.game_menu_state == "graphics":
            if self.main_graphics[0].draw(self.screen):  # Settings
                self.game_menu_state = "settings"

        # Sub-Menu -- Main / Settings / Audio
        elif self.game_menu_state == "audio":
            if self.main_audio[0].draw(self.screen):  # Settings
                self.game_menu_state = "settings"

        # Sub-Menu -- Main / Settings / Controls
        elif self.game_menu_state == "controls":
            if self.main_controls[0].draw(self.screen):  # Settings
                self.game_menu_state = "settings"

        pygame.display.update()


class PauseMenu:
    def __init__(self, variables):
        self.variables = variables

        self.game_paused = False
        self.screenshot = None
        self.pause_menu_state: str

        self.screen = self.variables.screen
        self.screen_x: int = self.variables.screen_x
        self.screen_y: int = self.variables.screen_y

        # Semi-transparent hall pilt
        self.semi_transparent_color = pygame.Surface((self.screen_x, self.screen_y), pygame.SRCALPHA)
        self.transparency_level = 150  # 0 - 255 // väiksem seda paremini läbi näha
        self.semi_transparent_color.fill((20, 20, 20, self.transparency_level))

        self.pause_main = [
            create_button(self.screen_x // 2 - menu_images["Resume"].get_width() // 2, self.screen_y // 6, menu_images["Resume"], 1),
            create_button(self.screen_x // 2 - menu_images["Settings"].get_width() // 2, self.screen_y // 3, menu_images["Settings"], 1),
            create_button(self.screen_x // 2 - menu_images["Save_&_Menu"].get_width() // 2, self.screen_y // 2, menu_images["Save_&_Menu"], 1),
            create_button(self.screen_x // 2 - menu_images["Save_&_Quit"].get_width() // 2, self.screen_y // 1.5, menu_images["Save_&_Quit"], 1),
        ]

        self.pause_settings = [
            create_button(self.screen_x // 2 - menu_images["Graphics"].get_width() // 2, self.screen_y // 6, menu_images["Graphics"], 1),
            create_button(self.screen_x // 2 - menu_images["Audio"].get_width() // 2, self.screen_y // 3, menu_images["Audio"], 1),
            create_button(self.screen_x // 2 - menu_images["Controls"].get_width() // 2, self.screen_y // 2, menu_images["Controls"], 1),
            create_button(self.screen_x // 2 - menu_images["Back"].get_width() // 2, self.screen_y // 1.5, menu_images["Back"], 1),
        ]

        self.pause_graphics = [
            create_button(self.screen_x // 2 - menu_images["Back"].get_width() // 2, self.screen_y // 6, menu_images["Back"], 1),
        ]

        self.pause_audio = [
            create_button(self.screen_x // 2 - menu_images["Back"].get_width() // 2, self.screen_y // 3, menu_images["Back"], 1),

        ]

        self.pause_controls = [
            create_button(self.screen_x // 2 - menu_images["Back"].get_width() // 2, self.screen_y // 2, menu_images["Back"], 1),

        ]

    def settings_menu(self) -> None:
        """ See FUNC seadistab 'Pause Menu'd.
        Täpsemalt: Siit saab muuta nuppude
        funktsioone ja ülejäänud menu loogikat. """
        if self.pause_menu_state == "main":

            # Kaotab muud buttonid ära
            if not self.screenshot:
                self.screenshot = pygame.display.get_surface().copy()
            self.screen.blit(self.screenshot, (0, 0))
            self.screen.blit(self.semi_transparent_color, (0, 0))

            if self.pause_main[0].draw(self.screen):  # Resume
                self.game_paused = False
                self.screenshot = None

            if self.pause_main[1].draw(self.screen):  # Settings
                self.pause_menu_state = "settings"

            if self.pause_main[2].draw(self.screen):  # Save & Menu

                # TODO: Save game
                # Player data - cords, inv, stats(health,hunger, ...)
                # World data - Glade, Maze, placed blocks, Time, Weather, ...
                # Entity data

                self.game_paused = False
                Menu.game_state = True

            if self.pause_main[3].draw(self.screen):  # Save & Quit
                # TODO: Save game
                # Player data - coords, inv, stats(health,hunger, ...)
                # World data - Glade, Maze, placed blocks, Time, Weather, ...
                # Entity data

                pygame.quit()
                sys.exit()

        # Sub-Menu -- Main / Settings
        elif self.pause_menu_state == "settings":
            self.screen.blit(self.screenshot, (0, 0))
            self.screen.blit(self.semi_transparent_color, (0, 0))

            if self.pause_settings[0].draw(self.screen):  # Graphics
                self.pause_menu_state = "graphics"

            if self.pause_settings[1].draw(self.screen):  # Audio
                self.pause_menu_state = "audio"

            if self.pause_settings[2].draw(self.screen):  # Controls
                self.pause_menu_state = "controls"

            if self.pause_settings[3].draw(self.screen):  # Main menu
                self.pause_menu_state = "main"

        # Sub-Menu -- Main / Settings / Graphics
        elif self.pause_menu_state == "graphics":
            self.screen.blit(self.screenshot, (0, 0))
            self.screen.blit(self.semi_transparent_color, (0, 0))

            if self.pause_graphics[0].draw(self.screen):  # Settings
                self.pause_menu_state = "settings"

        # Sub-Menu -- Main / Settings / Audio
        elif self.pause_menu_state == "audio":
            self.screen.blit(self.screenshot, (0, 0))
            self.screen.blit(self.semi_transparent_color, (0, 0))

            if self.pause_audio[0].draw(self.screen):  # Settings
                self.pause_menu_state = "settings"

        # Sub-Menu -- Main / Settings / Controls
        elif self.pause_menu_state == "controls":
            self.screen.blit(self.screenshot, (0, 0))
            self.screen.blit(self.semi_transparent_color, (0, 0))

            if self.pause_controls[0].draw(self.screen):  # Settings
                self.pause_menu_state = "settings"

        pygame.display.update()