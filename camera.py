def box_target_camera(self):
    '''Teeb boxi, kui minna sellele vastu, siis liigub kaamera'''

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