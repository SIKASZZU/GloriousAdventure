import pygame
from variables import UniversalVariables

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

    @staticmethod
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

        if self.click_position:
            self.click_window_x = self.click_position[0] - Camera.player_window_x
            self.click_window_y = self.click_position[1] - Camera.player_window_y
            Camera.click_x, Camera.click_y = round(UniversalVariables.player_x + self.click_window_x), round(UniversalVariables.player_y + self.click_window_y)

