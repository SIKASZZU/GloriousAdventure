import pygame
from variables import UniversalVariables


def is_click_inside_player_rect(self):
        if self.click_position != ():
            print(self.player_rect, self.click_position)
            click_within_x = self.player_rect[0] < self.click_position[0] and self.click_position[0] < self.player_rect[0] + self.player_rect[2]
            click_within_y = self.player_rect[1] < self.click_position[1] and self.click_position[1] < self.player_rect[1] + self.player_rect[3]
            print(click_within_x, click_within_y)
            if click_within_x and click_within_y:
                return True
            else:
                return False
        else:  
            return False

def current_equipped(self):
    """ Argument on item, mille funktsiooni kutsutakse. """

    #if item == 'Flashlight':
    #    new_player_cone_light_strenght = -70
    #    return new_player_cone_light_strenght
    
    #if item == 'Bread': ...
    #print('calling func')
    grid_y, grid_x = UniversalVariables.player_y // UniversalVariables.block_size, UniversalVariables.player_x // UniversalVariables.block_size 
    print(is_click_inside_player_rect(self))
    if is_click_inside_player_rect(self):
        print('found click')
        if UniversalVariables.current_equipped_item == 'Glowstick':
            print(grid_y, grid_x)
            self.terrain_data[grid_y][grid_x] = 34
    self.click_position = ()
             
             


    #if item == 'String':
    #    def draw_string(screen, start_pos, end_pos, color):  pygame.draw.line(screen, color, start_pos, end_pos, 2)
    #    is_click_inside_player_rect
    #    
    #    draw_string(UniversalVariables.screen, 'gray', self.self.terrain_data[grid_y][grid_x] = 34.center, self.player_rect.center)