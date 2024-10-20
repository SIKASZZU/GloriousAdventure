import pygame
from variables import UniversalVariables
from text import Fading_text

class Camera:

    screen = UniversalVariables.screen
    camera_borders = {'left': 450, 'right': 450, 'top': 450, 'bottom': 450}    
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


        Camera.player_window_x = self.player_rect.left - Camera.camera_rect.left + 450 - UniversalVariables.player_hitbox_offset_x  # Playeri x koordinaat windowi järgi
        Camera.player_window_y = self.player_rect.top - Camera.camera_rect.top + 450 - UniversalVariables.player_hitbox_offset_y  # Playeri y koordinaat windowi järgi

    def click_on_screen_to_grid(self):
        if Camera.click_y and Camera.click_x:
            return Camera.click_y // UniversalVariables.block_size, Camera.click_x // UniversalVariables.block_size


    def click_on_screen(self):
        if not self.click_position:
            return
        try:
            self.click_window_x = self.click_position[0] - Camera.player_window_x  # Click playerist (window)
            self.click_window_y = self.click_position[1] - Camera.player_window_y  # Click playerist (window)
        except TypeError:
            print('Click too fast and crash. All gucci my G'); return  # Armas comment <3
 
        if not UniversalVariables.player_range:
            player_range = 0
        else:
            player_range = UniversalVariables.player_range

        if abs(self.click_window_x) < player_range and abs(self.click_window_y) < player_range:
            Camera.click_x, Camera.click_y = round(UniversalVariables.player_x + self.click_window_x), round(UniversalVariables.player_y + self.click_window_y)
            Camera.click_info_available = True
        else:

            Camera.click_x, Camera.click_y = None, None

        if UniversalVariables.debug_mode:
            try:
                text = f"Clicked item : {Camera.click_on_screen_to_grid(self)}"
                Fading_text.re_display_fading_text(text)
            except IndexError:
                return
        ### FIXME: Camera.click_x ja Camera.click_y ei tohiks läbi invi saada
        return Camera.click_x, Camera.click_y

    def right_click_on_screen(self):
        try:
            if self.right_click_position:
                self.right_click_window_x = self.right_click_position[0] - Camera.player_window_x
                self.right_click_window_y = self.right_click_position[1] - Camera.player_window_y

                if not UniversalVariables.player_range:
                    player_range = 0
                else:
                    player_range = UniversalVariables.player_range


                if abs(self.right_click_window_x) < player_range and abs(self.right_click_window_y) < player_range:
                    Camera.right_click_x, Camera.right_click_y = round(UniversalVariables.player_x + self.right_click_window_x), round(UniversalVariables.player_y + self.right_click_window_y)
                    Camera.right_click_info_available = True
                else:

                    Camera.right_click_x, Camera.right_click_y = None, None

                if UniversalVariables.debug_mode:
                    try:
                        text = f"Clicked item : {self.terrain_data[int(Camera.right_click_y // UniversalVariables.block_size)][int(Camera.right_click_x // UniversalVariables.block_size)]}"
                        if text in Fading_text.shown_texts:
                            Fading_text.shown_texts.remove(text)
                        UniversalVariables.ui_elements.append(text)
                    except IndexError:
                        return
                ### FIXME: Camera.click_x ja Camera.click_y ei tohiks läbi invi saada
                return Camera.right_click_x, Camera.right_click_y
            return
        except TypeError:
            return


    def reset_clicks(self):
        if self.click_window_x and self.click_window_y:
        # self.click_position: tuple[int, int] = ()  # ei pea resettima self.click_positioni, vist ikka peab
            self.click_window_x = None
            self.click_window_y = None


    def print_clicks(self):
        """ Prints out the user's click information relative to terrain coordinates and screen."""

        if Camera.click_info_available:
            print(f"Click is within player's reach. \n   Click terrain x,y: ({Camera.click_x, Camera.click_y}) \n   Click window x,y: {self.click_position}")
            Camera.click_info_available = False  # reset loop
