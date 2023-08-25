import pygame

class Camera:

    # Teeb boxi, kui minna sellele vastu, siis liigub kaamera
    def box_target_camera(self):

        # camera stuff
        self.camera_borders = {'left': 100, 'right': 100, 'top': 100, 'bottom': 100}
        self.l = self.camera_borders['left']
        self.t = self.camera_borders['top']
        self.w = self.screen.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        self.h = self.screen.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(self.l, self.t, self.w, self.h)

        if self.player_rect.left < self.camera_rect.left:
            self.camera_rect.left = self.player_rect.left

        if self.player_rect.right > self.camera_rect.right:
            self.camera_rect.right = self.player_rect.right

        if self.player_rect.top < self.camera_rect.top:
            self.camera_rect.top = self.player_rect.top

        if self.player_rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = self.player_rect.bottom

        self.offset_x = self.camera_borders['left'] - self.camera_rect.left
        self.offset_y = self.camera_borders['top'] - self.camera_rect.top