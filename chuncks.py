import pygame

#def render_grid(self):
#    grid_size = self.block_size  # Yks grid on self.block_size * self.block_size
#    player_grid_x = (self.player_x + self.offset_x) // grid_size * grid_size
#    player_grid_y = (self.player_y + self.offset_y) // grid_size * grid_size
#
#    Xmin,Xmax,Ymin,Ymax = int(player_grid_x - 2 * grid_size), int(player_grid_x + 3 * grid_size), int(player_grid_y - 2 * grid_size), int(player_grid_y + 3 * grid_size)
#
#    rects = []
#
#    for x in range(Xmin, Xmax, grid_size):
#        for y in range(Ymin, Ymax, grid_size):
#            rect = pygame.Rect(x, y, grid_size, grid_size)
#            rects.append(rect)
#
#    render_rect = rects[0].unionall(rects[1:])


def render_grid(self):
    x = 100
    left = self.player_x - x
    top = self.player_y - x
    width = 3 * x
    height = 3 * x

    render_rect = pygame.Rect(left,top,width,height)
    #self.render_rect = pygame.Rect(self.player_x, self.player_y, self.block_size * 0.6, self.block_size * 0.75)
    return render_rect  # Rect

