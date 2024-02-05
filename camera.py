import pygame
from variables import UniversalVariables

class Camera:

    screen = UniversalVariables.screen
    camera_borders = {'left': 250, 'right': 250, 'top': 200, 'bottom': 200}
    l: int = camera_borders['left']
    t: int = camera_borders['top']
    w: int = screen.get_size()[0] - (camera_borders['left'] + camera_borders['right'])
    h: int = screen.get_size()[1] - (camera_borders['top'] + camera_borders['bottom'])
    camera_rect = pygame.Rect(l, t, w, h)

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
        