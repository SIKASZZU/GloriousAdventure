import pygame

# Teeb boxi, kui minna sellele vastu, siis liigub kaamera
    # Teeb boxi, kui minna sellele vastu, siis liigub kaamera
def box_target_camera(self):
    # camera stuff
    self.camera_borders = {'left': 100, 'right': 100, 'top': 100, 'bottom': 100}
    l = self.camera_borders['left']
    t = self.camera_borders['top']
    w = self.screen.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
    h = self.screen.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
    self.camera_rect = pygame.Rect(l, t, w, h)

    # camera offset
    self.offset_x = 0
    self.offset_y = 0

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