import pygame

def chunck_loader(self):
# playeri ymbruse m2rgistamine
    self.player_x + 1000
    self.player_y + 1000
    # rect, mis peaks olema alati loaded:
    render_rect_top = self.player_y + 1000
    render_rect_left = self.player_x - 1000
    render_rect_width = 2000
    render_rect_height = 2000
    
    render_rect = pygame.Rect(render_rect_left,
                            render_rect_top, 
                            render_rect_width,
                            render_rect_height
                        )
    
    # gridiks 
    render_rect_top_grid = render_rect_top / self.block_size + self.offset_y
    render_rect_left_grid = render_rect_left / self.block_size + self.offset_x
    render_rect_width_grid = render_rect_width / self.block_size + self.offset_x
    render_rect_height_grid = render_rect_height / self.block_size + self.offset_y