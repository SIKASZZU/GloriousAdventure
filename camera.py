import pygame

class Camera:
    def __init__(self, screen, click_tuple, terrain_data, player_update, fading_text, variables):
        self.click_position = click_tuple[0]
        self.click_window_x = click_tuple[1]
        self.click_window_y = click_tuple[2]

        self.right_click_position = click_tuple[3]
        self.right_click_window_x = click_tuple[4]
        self.right_click_window_y = click_tuple[5]

        self.terrain_data = terrain_data
        self.player_update = player_update
        self.fading_text = fading_text
        self.variables = variables

        self.screen = screen
        self.camera_borders = {'left': 450, 'right': 450, 'top': 274, 'bottom': 326}

        self.l, self.t = self.camera_borders['left'], self.camera_borders['top']
        self.w = self.screen.get_width() - (self.camera_borders['left'] + self.camera_borders['right'])
        self.h = self.screen.get_height() - (self.camera_borders['top'] + self.camera_borders['bottom'])

        self.camera_rect = pygame.Rect(self.l, self.t, self.w, self.h)
        self.click_info_available = False

        self.player_window_x = self.player_update.player_rect.left - self.camera_rect.left + self.camera_borders['left'] - self.variables.player_hitbox_offset_x
        self.player_window_y = self.player_update.player_rect.top - self.camera_rect.top + self.camera_borders['top'] - self.variables.player_hitbox_offset_y

        self.click_x = None
        self.click_y = None

        self.right_click_window_x = None
        self.right_click_window_y = None
        self.right_click_x = None
        self.right_click_y = None
        self.right_click_info_available = False

    def box_target_camera(self, player_rect):
        '''Moves the camera when the player hits the borders.'''
        if player_rect.left < self.camera_rect.left:
            self.camera_rect.left = player_rect.left

        if player_rect.right > self.camera_rect.right:
            self.camera_rect.right = player_rect.right

        if player_rect.top < self.camera_rect.top:
            self.camera_rect.top = player_rect.top

        if player_rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = player_rect.bottom

        self.variables.offset_x = self.camera_borders['left'] - self.camera_rect.left
        self.variables.offset_y = self.camera_borders['top'] - self.camera_rect.top

        self.player_window_x = player_rect.left - self.camera_rect.left + self.camera_borders['left'] - self.variables.player_hitbox_offset_x
        self.player_window_y = player_rect.top - self.camera_rect.top + self.camera_borders['top'] - self.variables.player_hitbox_offset_y

    @staticmethod
    def is_click_within_player_range(click_window_x, click_window_y) -> bool:
        player_range = self.variables.player_range or 0
        return abs(click_window_x) < player_range and abs(click_window_y) < player_range

    @staticmethod
    def click_on_screen_to_grid(click_x: float, click_y: float) -> tuple[None, None] | tuple[float, float]:
        if not click_x or not click_y:
            self.variables.print_debug_text('click_y or click_x ---> is invalid')
            return None, None

        return click_y // self.variables.block_size, click_x // self.variables.block_size

    def left_click_on_screen(self, click_position) -> None | tuple[None, None] | tuple[int, int]:
        if type(self.click_position) is not tuple:
            return

        self.click_position = click_position


        if not self.click_position or len(self.click_position) != 2 or None in self.click_position or not self.player_window_x or not self.player_window_y:
            self.variables.print_debug_text(f'Invalid click position or player window coordinates. {self.click_position}')
            return None, None

        self.click_window_x = self.click_position[0] - self.player_window_x
        self.click_window_y = self.click_position[1] - self.player_window_y

        if self.is_click_within_player_range(self.click_window_x, self.click_window_y):
            self.click_x = round(self.variables.player_x + self.click_window_x)
            self.click_y = round(self.variables.player_y + self.click_window_y)
            self.click_info_available = True

        else:
            self.click_x, self.click_y = None, None

        if self.variables.debug_mode:
            grid_click = self.click_on_screen_to_grid(self.click_x, self.click_y)
            try:  self.variables.print_debug_text(f"Click Terrain Value = {self.terrain_data[grid_click[0]][grid_click[1]]} <- Camera.left_click_screen()")
            except:  self.fading_text.re_display_fading_text(f"Clicked item: {grid_click}", debug=True)
        return self.click_x, self.click_y

    def right_click_on_screen(self, right_click_position):

        if not right_click_position:
            return None, None

        self.right_click_position = right_click_position

        self.right_click_window_x = self.right_click_position[0] - self.player_window_x
        self.right_click_window_y = self.right_click_position[1] - self.player_window_y

        if self.is_click_within_player_range(self.right_click_window_x, self.right_click_window_y):
            self.right_click_x = round(self.variables.player_x + self.right_click_window_x)
            self.right_click_y = round(self.variables.player_y + self.right_click_window_y)
            self.right_click_info_available = True
        else:
            self.right_click_x, self.right_click_y = None, None

        if self.variables.debug_mode:
            grid_click = self.click_on_screen_to_grid(self.right_click_x, self.right_click_y)
            self.fading_text.re_display_fading_text(f"Clicked item: {grid_click}", debug=True)

        return self.right_click_x, self.right_click_y

    def reset_clicks(self):
        self.click_window_x = self.click_window_y = None
        self.click_x = self.click_y = None

        self.right_click_window_x = self.right_click_window_y = None
        self.right_click_x = self.right_click_y = None

        self.click_position = None
        self.right_click_position = None


    def print_clicks(self):
        if self.click_info_available:
            print(f"Click is within player's reach. \n   Click terrain x,y: ({self.click_x, self.click_y}) \n   Click window x,y: {self.click_position}")
            self.click_info_available = False
