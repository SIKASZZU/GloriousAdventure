import pygame
from variables import UniversalVariables
from text import Fading_text

class Camera:

    screen = UniversalVariables.screen
    camera_borders = {'left': 450, 'right': 450, 'top': 276, 'bottom': 326}
    l: int = camera_borders['left']
    t: int = camera_borders['top']
    w: int = screen.get_size()[0] - (camera_borders['left'] + camera_borders['right'])
    h: int = screen.get_size()[1] - (camera_borders['top'] + camera_borders['bottom'])
    camera_rect = pygame.Rect(l, t, w, h)

    player_window_x: int = None
    player_window_y: int = None
    click_x: int = None
    click_y: int = None
    click_info_available = False  # for printing func

    right_player_window_x: int = None
    right_player_window_y: int = None
    right_click_x: int = None
    right_click_y: int = None
    right_click_info_available = False  # for printing func

    def box_target_camera(self):
        '''Teeb boxi, kui minna sellele vastu, siis liigub kaamera'''

        if self.player_rect.left < Camera.camera_rect.left:
            Camera.camera_rect.left = self.player_rect.left

        if self.player_rect.right > Camera.camera_rect.right:
            Camera.camera_rect.right = self.player_rect.right

        if self.player_rect.top < Camera.camera_rect.top:
            Camera.camera_rect.top = self.player_rect.top

        if self.player_rect.bottom > Camera.camera_rect.bottom:
            Camera.camera_rect.bottom = self.player_rect.bottom

        UniversalVariables.offset_x = Camera.camera_borders['left'] - Camera.camera_rect.left
        UniversalVariables.offset_y = Camera.camera_borders['top'] - Camera.camera_rect.top

        Camera.player_window_x = self.player_rect.left - Camera.camera_rect.left + Camera.camera_borders['left'] - UniversalVariables.player_hitbox_offset_x  # Playeri x koordinaat windowi järgi
        Camera.player_window_y = self.player_rect.top - Camera.camera_rect.top + Camera.camera_borders['top'] - UniversalVariables.player_hitbox_offset_y  # Playeri y koordinaat windowi järgi

    @staticmethod
    def is_within_player_range(click_window_x, click_window_y) -> bool:
        player_range = UniversalVariables.player_range or 0  # Kui player_range = None ---> player_range = 0

        # Vaatab, kas player on click on player range'is
        return abs(click_window_x) < player_range and abs(click_window_y) < player_range

    @staticmethod
    def click_on_screen_to_grid(click_x: float, click_y: float) -> tuple[int | None, int | None]:
        if not click_x or not click_y:
            UniversalVariables.print_debug_text('click_y or click_x ---> is invalid')
            return None, None

        return click_y // UniversalVariables.block_size, click_x // UniversalVariables.block_size

    ### FIXME: Camera.click_x ja Camera.click_y ei tohiks läbi invi saada
    def left_click_on_screen(self) -> tuple[int | None, int | None]:
        if not self.click_position:
            return None, None

        if not isinstance(self.click_position, tuple) or not len(self.click_position) == 2:
            UniversalVariables.print_debug_text('Click_position ---> Not tuple or len() > 2')
            return None, None

        if None in self.click_position:
            UniversalVariables.print_debug_text('Click_position ---> is None')
            return None, None

        if not Camera.player_window_x or not Camera.player_window_y:
            UniversalVariables.print_debug_text('Camera.player_window_x or Camera.player_window_y ---> is None')
            return None, None

        self.click_window_x = self.click_position[0] - Camera.player_window_x  # Click relative to player (window)
        self.click_window_y = self.click_position[1] - Camera.player_window_y  # Click relative to player (window)

        if Camera.is_within_player_range(self.click_window_x, self.click_window_y):
            Camera.click_x, Camera.click_y = round(UniversalVariables.player_x + self.click_window_x), round(UniversalVariables.player_y + self.click_window_y)
            Camera.click_info_available = True
        else:
            Camera.click_x, Camera.click_y = None, None

        if UniversalVariables.debug_mode:
            grid_click = Camera.click_on_screen_to_grid(Camera.click_x, Camera.click_y)
            Fading_text.re_display_fading_text(f"Clicked item: {grid_click}", debug=True)

        return Camera.click_x, Camera.click_y

    ### FIXME: Camera.click_x ja Camera.click_y ei tohiks läbi invi saada
    def right_click_on_screen(self):
        if not self.right_click_position:
            return None, None

        self.right_click_window_x = self.right_click_position[0] - Camera.player_window_x
        self.right_click_window_y = self.right_click_position[1] - Camera.player_window_y

        if Camera.is_within_player_range(self.right_click_window_x, self.right_click_window_y):
            Camera.right_click_x = round(UniversalVariables.player_x + self.right_click_window_x)
            Camera.right_click_y = round(UniversalVariables.player_y + self.right_click_window_y)
            Camera.right_click_info_available = True
        else:
            Camera.right_click_x, Camera.right_click_y = None, None

        if UniversalVariables.debug_mode:
            grid_click = Camera.click_on_screen_to_grid(Camera.right_click_x, Camera.right_click_y)
            Fading_text.re_display_fading_text(f"Clicked item: {grid_click}", debug=True)

        return Camera.right_click_x, Camera.right_click_y


    def reset_clicks(self):
        # self.click_position: tuple[int, int] = ()  # ei pea resettima self.click_positioni, vist ikka peab
        if self.click_window_x and self.click_window_y:
            self.click_window_x = None
            self.click_window_y = None


    def print_clicks(self):
        """ Prints out the user's click information relative to terrain coordinates and screen."""

        if Camera.click_info_available:
            print(f"Click is within player's reach. \n   Click terrain x,y: ({Camera.click_x, Camera.click_y}) \n   Click window x,y: {self.click_position}")
            Camera.click_info_available = False  # reset loop
