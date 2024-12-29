import pygame
from variables import UniversalVariables
from text import Fading_text

class Camera:

    def __init__(self, screen):
        self.screen = screen
        self.camera_borders = {'left': 450, 'right': 450, 'top': 274, 'bottom': 326}
        
        self.l: int = self.camera_borders['left']
        self.t: int = self.camera_borders['top']
        self.w: int = self.screen.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        self.h: int = self.screen.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        
        self.camera_rect = pygame.Rect(self.l, self.t, self.w, self.h)
        self.player_window_x: int = None
        self.player_window_y: int = None
        self.click_x: int = None
        self.click_y: int = None
        
        self.click_info_available = False  # for printing func
        self.right_player_window_x: int = None
        self.right_player_window_y: int = None
        self.right_click_x: int = None
        self.right_click_y: int = None
        self.right_click_info_available = False  # for printing func

    def box_target_camera(self, player_rect):
        '''Teeb boxi, kui minna sellele vastu, siis liigub kaamera'''

        if player_rect.left < self.camera_rect.left:
            self.camera_rect.left = player_rect.left

        if player_rect.right > self.camera_rect.right:
            self.camera_rect.right = player_rect.right

        if player_rect.top < self.camera_rect.top:
            self.camera_rect.top = player_rect.top

        if player_rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = player_rect.bottom

        UniversalVariables.offset_x = self.camera_borders['left'] - self.camera_rect.left
        UniversalVariables.offset_y = self.camera_borders['top'] - self.camera_rect.top

        self.player_window_x = player_rect.left - self.camera_rect.left + self.camera_borders['left'] - UniversalVariables.player_hitbox_offset_x  # Playeri x koordinaat windowi järgi
        self.player_window_y = player_rect.top - self.camera_rect.top + self.camera_borders['top'] - UniversalVariables.player_hitbox_offset_y  # Playeri y koordinaat windowi järgi

    @staticmethod
    def is_click_within_player_range(click_window_x, click_window_y) -> bool:
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

        if not self.camera.player_window_x or not self.camera.player_window_y:
            UniversalVariables.print_debug_text('self.camera.player_window_x or self.camera.player_window_y ---> is None')
            return None, None

        self.click_window_x = self.click_position[0] - self.camera.player_window_x  # Click relative to player (window)
        self.click_window_y = self.click_position[1] - self.camera.player_window_y  # Click relative to player (window)

        if Camera.is_click_within_player_range(self.click_window_x, self.click_window_y):
            self.camera.click_x, self.camera.click_y = round(UniversalVariables.player_x + self.click_window_x), round(UniversalVariables.player_y + self.click_window_y)
            self.camera.click_info_available = True
        else:
            self.camera.click_x, self.camera.click_y = None, None

        if UniversalVariables.debug_mode:
            grid_click = Camera.click_on_screen_to_grid(self.camera.click_x, self.camera.click_y)
            UniversalVariables.print_debug_text(f"Click Terrain Value = {self.terrain_data[grid_click[0]][grid_click[1]]} <- Camera.left_click_screen()")
            Fading_text.re_display_fading_text(f"Clicked item: {grid_click}", debug=True)

        return self.camera.click_x, self.camera.click_y

    ### FIXME: Camera.click_x ja Camera.click_y ei tohiks läbi invi saada
    def right_click_on_screen(self):
        if not self.right_click_position:
            return None, None

        self.right_click_window_x = self.right_click_position[0] - self.camera.player_window_x
        self.right_click_window_y = self.right_click_position[1] - self.camera.player_window_y

        if Camera.is_click_within_player_range(self.right_click_window_x, self.right_click_window_y):
            self.camera.right_click_x = round(UniversalVariables.player_x + self.right_click_window_x)
            self.camera.right_click_y = round(UniversalVariables.player_y + self.right_click_window_y)
            self.camera.right_click_info_available = True
        else:
            self.camera.right_click_x, self.camera.right_click_y = None, None

        if UniversalVariables.debug_mode:
            grid_click = Camera.click_on_screen_to_grid(self.camera.right_click_x, self.camera.right_click_y)
            Fading_text.re_display_fading_text(f"Clicked item: {grid_click}", debug=True)

        return self.camera.right_click_x, self.camera.right_click_y


    def reset_clicks(self):
        # self.click_position: tuple[int, int] = ()  # ei pea resettima self.click_positioni, vist ikka peab
        if self.click_window_x and self.click_window_y:
            self.click_window_x = None
            self.click_window_y = None


    def print_clicks(self):
        """ Prints out the user's click information relative to terrain coordinates and screen."""

        if self.camera.click_info_available:
            print(f"Click is within player's reach. \n   Click terrain x,y: ({self.camera.click_x, self.camera.click_y}) \n   Click window x,y: {self.click_position}")
            self.camera.click_info_available = False  # reset loop
